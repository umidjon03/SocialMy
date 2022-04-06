from django.urls import path, include
from . import views

urlpatterns = [    
    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name= 'room'),


    path('browse-topics/', views.borwseTopics, name='browse-topics'),
    path('activities/', views.activities, name='activities'),
    
    
    path('create-room/', views.createroom, name = 'create-room'),
    path('update-room/<str:pk>', views.updateroom, name = 'update-room'),
    path('delete-room/<str:pk>', views.deleteroom, name = 'delete-room'),
    
    
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message')
]