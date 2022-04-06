from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model   = Room
        fields  =  "__all__" #['name', 'topic'] #agar __all__ bolsa hamma Room fieldlari olinadi
        exclude = ['host', 'participants']



# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar', 'name', 'username', 'username', 'email', 'bio']



# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2']
