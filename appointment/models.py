from django.db import models

from account.models import User
from farmclinic import settings


class Expert(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qualifications = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    documents = models.FileField(upload_to='expert_documents/', blank=True)

    passport_photo = models.ImageField(
        upload_to='users/passport_photo', blank=True, null=True)
    citizenship_front = models.ImageField(
        upload_to='users/citicenship_photo', blank=True, null=True)
    citizenship_back = models.ImageField(
        upload_to='users/citicenship_photo', blank=True, null=True)
    citizenship_back = models.ImageField(
        upload_to='users/license', blank=True, null=True)
    
    specialty = models.CharField(max_length=100, blank=True)

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name




class Appointment(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_appointments')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='expert_appointments')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Appointment with {self.expert.user.full_name} on {self.sent_date}"

    class Meta:
        ordering = ["-sent_date"]