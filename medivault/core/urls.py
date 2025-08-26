from. import views
from django.urls import path
from django.urls import include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("my_vault/",view=views.my_vault,name='my_vault'),
    path("upload_record/",view=views.upload_record,name='upload_record'),
    path("delete_record/<int:record_id>",view=views.delete_record,name='delete_record'),
    path('record/view/<int:record_id>/', views.view_record, name='view_record'),


]
  