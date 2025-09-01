from django.contrib import admin
from .models import HumanAIConversation,Message
# Register your models here.

admin.site.register(Message)
admin.site.register(HumanAIConversation)