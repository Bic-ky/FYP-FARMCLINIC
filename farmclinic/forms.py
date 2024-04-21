from account.models import Enquiry
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter your name',
            'email': 'Enter email address',
            'phone': 'Enter phone number',
            'message': 'Enter message',
        }
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, ''),
            })
