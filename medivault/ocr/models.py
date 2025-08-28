from django.db import models
from accounts.models import Profile
# Create your models here.
class OCRDocument(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='ocr_uploads')
    file=models.FileField(upload_to='ocr_uploads')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    ocr_result=models.TextField(blank=True,null=True)
    processed=models.BooleanField(default=False)
    ai_response = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.profile.user.username} uploaded {self.uploaded_at}'
  