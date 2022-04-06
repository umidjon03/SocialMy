from django.db import models as m
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _



# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, profile_picture=None, gender=None, password=None, is_admin=False, is_staff=False, is_active=True):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not full_name:
#             raise ValueError("User must have a full name")

#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.full_name = full_name
#         user.set_password(password)  # change password to hash
#         # user.profile_picture = profile_picture
#         user.gender = gender
#         user.admin = is_admin
#         user.profile_picture = profile_picture
#         user.staff = is_staff
#         user.active = is_active
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, email, profile_picture, gender, full_name, password=None):
#         user = self.create_user(
#             email,
#             full_name,
#             profile_picture,
#             gender,
#             password=password,
#             is_staff=True,
#         )
#         return user

#     def create_superuser(self, email, profile_picture, gender, full_name, password=None):
#         user = self.create_user(
#             email,
#             full_name,
#             profile_picture,
#             gender,
#             password=password,
#             is_staff=True,
#             is_admin=True,
#         )
#         return user



class User(AbstractUser):
    name = m.CharField(max_length=30, null=True)
    email = m.EmailField(_('email adress'), unique=True, null=True)
    bio = m.TextField(max_length=300, null=True, blank=True)
    avatar = m.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']