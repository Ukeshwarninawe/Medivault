from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
  
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = PhoneNumberField(region='IN')  
    city=models.CharField(max_length=30)
    bio=models.TextField(max_length=200)

    def __str__(self):
        return f"{self.user.username} from {self.city} "

