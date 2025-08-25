from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UsernameLoginForm
from .models import Profile
from django.shortcuts import get_object_or_404

# -------------------------------------------------
#  Sign‑up (creates User + Profile)
# -------------------------------------------------
def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()                       # creates User + Profile
            login(request, user)                     # log them in immediately
            messages.success(request, "Account created – you are now logged in.")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})



def signup_user(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request,user)
            Profile.objects.create(user=user)
            messages.success(request,"Account created...!")   
            return redirect("profile")
        else:
            messages.error(request,'Please fix errors')
    else:
        form=SignUpForm()
    
    return render(request,'accounts/signup.html',{"form": form})
# -------------------------------------------------
#  Login (username only)
# -------------------------------------------------
def login_user(request):
    if request.method == "POST":
        form = UsernameLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = UsernameLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

from django.shortcuts import get_object_or_404
from .models import Profile            

def setup_profile(request):
    profile=get_object_or_404(Profile,id=request.user.profile.id)
    if request.methos=="POST":
        profile.user=request.user
        profile.city=request.POST.get("city")
        profile.bio=request.POST.get("bio")

        
                
        
    return render(request,'accounts/profile.html')