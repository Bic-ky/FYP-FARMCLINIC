from django.urls import path, include
from . import views


app_name ='account'
urlpatterns =[
    path('', views.index , name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view , name="login"),
    path('logout/',views.logout, name='logout'),
    path('chat/',views.chat, name='chat'),
    path('appointment/',views.appointment, name='appointment'),

    path('expert_change_password/', views.expert_change_password, name='expert_change_password'),
    path('farmer_change_password/', views.farmer_change_password, name='farmer_change_password'),


    path('myAccount/',views.myAccount, name='myAccount'),
    path('profile/', views.profile , name='profile' ),
    path('expertdashboard/',views.expertdashboard, name='expertdashboard'),
    path('farmerdashboard/',views.farmerdashboard, name='farmerdashboard'),


    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

]