from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('signup/',view=views.signup_user,name='signup'),
    path('login/',view=views.login_user,name='login'),
    path('logout/',view=views.login_user,name='logout'),
      path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/setup/', views.setup_profile, name='setup_profile'),
]
  