from django.contrib import admin
from .models import MedicalRecord,Vault
# Register your models here.
admin.site.register(Vault)
admin.site.register(MedicalRecord)