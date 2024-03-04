from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # Define choices for the role field based on the User model
    ROLE_CHOICES = User.ROLE_CHOICES

    # Create the ChoiceField for role
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['phone_number', 'role', 'full_name', 'email', 'password']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add form control attributes to the fields
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})