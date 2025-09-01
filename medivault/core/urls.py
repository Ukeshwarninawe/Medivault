from. import views
from django.urls import path
from django.urls import include

from django.urls import path
from core import views

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_vault, name='create_vault'),
    path('authenticate/', views.authenticate_vault, name='authenticate_vault'),
    path('', views.view_vault, name='view_vault'),  # Default vault page
    path('qr/<uuid:qr_secret>/', views.access_vault_by_qr, name='access_vault_by_qr'),
    path('show_qr/', views.show_qr, name='show_qr'),
    path('upload_record/', views.upload_record, name='upload_record'),
    path('record/<int:record_id>/', views.view_record, name='view_record'),
    path('record/<int:record_id>/delete/', views.delete_record, name='delete_record'),
    path('my_vault/', views.my_vault, name='my_vault'),
]
