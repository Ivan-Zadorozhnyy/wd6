from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('entity/', views.entity_list, name='entity_list'),
    path('entity/<int:id>/', views.entity_detail, name='entity_detail'),
    path('entity/<int:id>/image/', views.entity_image, name='entity_image'),
    path('entity/', views.entity_create, name='entity_create'),
    path('entity/<int:id>/delete/', views.entity_delete, name='entity_delete'),
    path('get-csrf/', views.get_csrf, name='get_csrf'),
    # 1ieUQMjyB4eLJVsH80F06IGGpbkPiVTt
    path('cookie/set/', views.set_cookie_view, name='set_cookie'),
    path('cookie/get/<str:name>/', views.get_cookie_view, name='get_cookie'),
    path('header/set/', views.set_header_view, name='set_header'),
    path('header/get/<str:name>/', views.get_header_view, name='get_header'),
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:id>/', views.UserRetrieveUpdateDestroy.as_view(), name='user-retrieve-update-destroy'),
]

