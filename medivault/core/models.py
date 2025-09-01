from django.db import models
from accounts.models import Profile
from django.contrib.auth.hashers import make_password,check_password
import uuid
import qrcode
from django.urls import reverse
import os 
from django.conf import settings
class Vault(models.Model):
    name=models.CharField(max_length=30)
    owner=models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='vaults')
    vault_password=models.CharField(max_length=255)
    qr_secret=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)


    def set_password(self,raw_password):
        self.vault_password=make_password(raw_password)

    def check_password(self,raw_password):
        return check_password(raw_password,self.vault_password)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Generate internal path (not full domain)
        qr_url_path = reverse('access_vault_by_qr', args=[str(self.qr_secret)])

        
        qr_img = qrcode.make(qr_url_path)

        # Save QR image to media/qr/
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr')
        os.makedirs(qr_dir, exist_ok=True)
        qr_filename = f"vault_qr_{self.owner.pk}.png"
        qr_path = os.path.join(qr_dir, qr_filename)
        qr_img.save(qr_path)

    def __str__(self):
        return f'{self.owner.user.username} created {self.name}'

    




class MedicalRecord(models.Model):
    RECORD_TYPE = [
    ('prescription', 'Prescription'),
    ('lab_report', 'Lab Report'),
    ('scan', 'Scan/Imaging'),
    ('discharge', 'Discharge Summary'),
    ('other', 'Others') 
]
    # profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='medical_records')
    # filename=models.CharField(max_length=300,blank=False,null=False) 
    vault=models.ForeignKey(Vault,on_delete=models.CASCADE,related_name='medical_records',null=True)     
    file=models.FileField(upload_to='medical_docs/')
    title=models.CharField(max_length=300,blank=True,null=True)
    record_type=models.CharField(max_length=50,choices=RECORD_TYPE,default='other')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    processed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.vault.owner.user.username}"
    
    def filename(self):
        return os.path.basename(self.file.name)
  
    