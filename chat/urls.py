from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('message/', views.messages_page , name="message" ),
]
