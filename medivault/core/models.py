from django.db import models
from accounts.models import Profile
# Create your models here.



class MedicalDocument(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='documents')
    filename=models.CharField(max_length=300,blank=False,null=False)      
    file=models.FieldFile(upload_to='medical_docs/')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    processed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.filename} by {self.profile.user.username}"