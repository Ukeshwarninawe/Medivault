from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField 
from .models import Profile
class SignUpForm(UserCreationForm):
    # full_name = forms.CharField(
    #     max_length=100,
    #     required=True,
    #     help_text="Your full name"
    # )
    mobile_number = PhoneNumberField(
        region='IN',
        required=True,
        help_text="e.g. +91-9876543210"
    )
    email = forms.EmailField(
        required=True,
        help_text="A valid email address"
    )

    class Meta:
        model=User
        fields = ('username', 'mobile_number', 'email', 'password1', 'password2')

    
    def save(self, commit=True):
            
            """Save the User and create a linked Profile with extra fields."""
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                Profile.objects.create(
                user=user,
                # full_name=self.cleaned_data['full_name'],
                mobile_number=self.cleaned_data['mobile_number']
            )
            return user
    

class UsernameLoginForm(AuthenticationForm):
    """Same as Django’s built‑in form – it already uses 'username' field."""



