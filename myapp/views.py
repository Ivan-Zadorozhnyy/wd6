from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Entity
import os
from django.conf import settings

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
