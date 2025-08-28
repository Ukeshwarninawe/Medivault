from django.db import models
from accounts.models import Profile
# Create your models here.





class Agent(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='agent')
