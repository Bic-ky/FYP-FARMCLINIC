from django.urls import path, include
from . import views


urlpatterns = [
    path('expert_detail/', views.expert_detail, name='expert_detail'),
    path('experts/', views.experts, name='experts'),
]