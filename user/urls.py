from django.urls import  path
from . import views


urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('edit-user/', views.editUser, name='edit-user'),
    path('logout/', views.logoutUser, name='logout'),
    path('user-profile/<str:pk>', views.userProfile, name='user-profile'),
]