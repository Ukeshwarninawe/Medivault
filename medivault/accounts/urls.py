from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('signup/',view=views.signup_user,name='signup'),
    path('login/',view=views.login_user,name='login'),
    # path('profile/',vie)
    path('logout/',view=views.login_user,name='logout'),
]
  