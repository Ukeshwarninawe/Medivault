from django.db import models
from accounts.models import Profile
# Create your models here.
import os 


class MedicalRecord(models.Model):
    RECORD_TYPE = [
    ('prescription', 'Prescription'),
    ('lab_report', 'Lab Report'),
    ('scan', 'Scan/Imaging'),
    ('discharge', 'Discharge Summary'),
    ('other', 'Others') 
]
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='medical_records')
    # filename=models.CharField(max_length=300,blank=False,null=False)      
    file=models.FileField(upload_to='medical_docs/')
    title=models.CharField(max_length=300,blank=True,null=True)
    record_type=models.CharField(max_length=50,choices=RECORD_TYPE,default='other')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    processed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.profile.user.username}"
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    # def delete(self):
    #     if self.file:
    #         if os.path.isfile()

    