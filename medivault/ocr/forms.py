from .models import OCRDocument
from django import forms

class OCRDocumentForm(forms.ModelForm):
    class Meta:
        model=OCRDocument
        fields=['file']


