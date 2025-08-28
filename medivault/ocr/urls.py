from django.urls import path
from ocr import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('my_uploads/', views.my_uploads, name='my_uploads'),
    path('uploads/view/<int:document_id>/', views.view_uploads, name='view_uploads'),
    path('uploads/delete/<int:document_id>/',view=views.delete_uploads,name='delete_uploads')
]
