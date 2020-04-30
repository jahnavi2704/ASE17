from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=12, blank=False)
    address = models.CharField(max_length=255, blank=False)
    card_no = models.CharField(max_length=16, blank=False)
    display_pic = models.ImageField(default='default.png', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'