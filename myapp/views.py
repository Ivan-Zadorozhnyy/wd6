from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Entity, User
import os
from django.conf import settings
from .helpers.cookie_helper import set_cookie, get_cookie
from .helpers.header_helper import set_header, get_header
from rest_framework import generics
from .serializers import UserSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@csrf_exempt
def main_page(request):
    return render(request, 'main_page.html')

@csrf_exempt
def entity_list(request):
    entities = Entity.objects.all()
    return render(request, 'entity_list.html', {'entities': entities})

@csrf_exempt
def entity_detail(request, id):
    entity = get_object_or_404(Entity, pk=id)
    return render(request, 'entity_detail.html', {'entity': entity})

@csrf_exempt
def entity_image(request, id):
    entity = get_object_or_404(Entity, pk=id)
    image_filename = f'entity_{id}.jpg'
    image_path = os.path.join(settings.STATIC_URL, 'images', image_filename)

    return render(request, 'entity_image.html', {'entity': entity, 'image_path': image_path})

@csrf_exempt
def entity_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        entity = Entity.objects.create(name=name, description=description)
        entity.save()
        return JsonResponse({'id': entity.id, 'name': entity.name, 'description': entity.description})
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def entity_delete(request, id):
    entity = get_object_or_404(Entity, pk=id)
    entity.delete()
    return redirect(reverse('entity_list'))

def get_csrf(request):
    return render(request, 'get_csrf.html')

@csrf_exempt
def set_cookie_view(request):
    name = request.GET.get('name')
    value = request.GET.get('value')
    http_only = request.GET.get('httpOnly') == 'true'
    response = JsonResponse({'message': f'Set cookie {name} to {value}'})
    set_cookie(response, name, value, http_only)
    return response

@csrf_exempt
def get_cookie_view(request, name):
    value = get_cookie(request, name)
    return JsonResponse({name: value})

@csrf_exempt
def set_header_view(request):
    name = request.GET.get('name')
    value = request.GET.get('value')
    response = JsonResponse({'message': 'Header set'})
    set_header(response, name, value)
    return response

@csrf_exempt
def get_header_view(request, name):
    value = get_header(request, name)
    return JsonResponse({name: value})

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "user_notification",
                "message": {"detail": "New user created!", "user_data": serializer.data}
            }
        )

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
