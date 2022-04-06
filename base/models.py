from django.db.models.deletion import CASCADE, SET_NULL
from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser


# Create your models here.
# class User(AbstractUser):
#     name = models.CharField(max_length=50, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)
#     avatar = models.ImageField(null=True, default="avatar.svg")

#     # USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
from user.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host         = models.ForeignKey(User, on_delete=SET_NULL, null=True) # ForeignKEy da host o'zgaruvchining qiymati User modelidan olinadi. Ya'ni, host User modelidagi foydalanuvchilarning biri
    participants = models.ManyToManyField(User, related_name='participants', null=True)
    topic        = models.ForeignKey(Topic, on_delete=SET_NULL, null=True) #on_delete=SET_NULL bu qiymatda agar parent class (Topic) ochib ketsa ham topic ozgaruvchi qiymati saqlanib qoladi
    name         = models.CharField(max_length=200)
    description  = models.TextField(null=True, blank=True)
    updated      = models.DateTimeField(auto_now=True) #har safar yangilab turadi
    created      = models.DateTimeField(auto_now_add=True) # +=_add faqat yaratilgandagi vaqt
    class Meta:
        ordering = ['-updated', '-created'] #update va created boyicha ordering qiladi yani eng oxirgo yangilangan submodel birinchi bolib turadi aga - siz yozilsa eng oxiri boladi


    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    user    = models.ForeignKey(User, on_delete=CASCADE)
    room    = models.ForeignKey(Room, related_name='comment', on_delete=CASCADE) #agar qiymat cascade bo'lsa parent clas (Room) ma'lumotlari ochirilsa room o'zgaruvchi saqlagan qiymat ham o'chadi 
    body    = models.TextField()
    updated = models.DateTimeField(auto_now=True) #har safar yangilab turadi
    created = models.DateTimeField(auto_now_add=True) # +=_add faqat yaratilgandagi vaqt

    
    class Meta:
        ordering = ['-updated', '-created']
    

    def __str__(self):
        return self.body[:50]

    
