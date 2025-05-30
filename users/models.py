from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username  
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone=models.CharField(max_length=14,blank=True,null=True)
    image = models.ImageField(upload_to='profile_images', default='profile.png', blank=True, null=True)
    birthdate=models.DateField(blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    facebook_profile=models.URLField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
