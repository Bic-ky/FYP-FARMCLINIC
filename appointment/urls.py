from django.urls import path, include
from . import views


urlpatterns = [
    path('expert_detail/', views.expert_detail, name='expert_detail'),
    path('experts/', views.experts, name='experts'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('appointment_date/', views.appointment_date, name='appointment_date'),
    path('appointments/', views.appointment_list, name='appointment_list'),
]