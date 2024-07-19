from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import User, UserProfile


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    ROLE_CHOICES = User.ROLE_CHOICES

    # Create the ChoiceField for role
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['phone_number', 'role', 'full_name', 'email', 'password','address', 'country', 'city', 'latitude' , 'longitude']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})




class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add form control attributes to the fields
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})



class AppointmentForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    documents = forms.FileField(label='Documents', required=False)
    address = forms.CharField(label='Address', max_length=200, widget=forms.Textarea)
    contact = forms.CharField(label='Contact', max_length=20)
    date = forms.DateField(label='Date')
    experts = forms.CharField(label='Experts', max_length=200)

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})




class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}), required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "instagram",
            "twitter",
            "linkedin",
            "facebook"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "phone_number",
            "full_name",
            "email",
            "address",
            "city",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})