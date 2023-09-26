from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100,
                              choices=[('Male', 'male'), ('Female', 'female')], blank=True)
    product_lst = models.CharField(max_length=300, null=True, blank=True)
    product_lst_saving = models.CharField(
        max_length=300, null=True, blank=True)
    follow = models.ManyToManyField(
        'self', related_name='followers', blank=True, symmetrical=False)
    
class Avatar(models.Model):
    personality = models.CharField(max_length=100, null=True, blank=True)
    img_file = models.ImageField(null=True, blank=True, upload_to='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avatar')

class Personality(models.Model):
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)