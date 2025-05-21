from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=14,blank=True,null=True)
    image=models.ImageField(upload_to='profile_images/',blank=True)
    birthdate=models.DateField(blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    facebook_profile=models.URLField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
