from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import requests

from account.utils import send_verification_email
from farmclinic.settings import WEATHER_API , VISUALCROSSING_API 

from .models import User, UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import  CustomPasswordChangeForm, LoginForm, RegistrationForm, UserForm, UserProfileForm
from appointment.forms import AppointmentForm
from django.shortcuts import render, redirect
from .forms import LoginForm

import json
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
import sys
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


def check_role_expert(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def check_role_farmer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def detectUser(user):
    if user.role == User.EXPERT:
        return 'account:expertdashboard'
    elif user.role == User.FARMER:
        return 'account:farmerdashboard'
    else:
        return None


def myAccount(request):
    user = request.user
    if user.is_authenticated:
        redirect_url = detectUser(user)
        if redirect_url:
            return redirect(redirect_url)
        else:
            messages.error(request, 'Unable to determine dashboard for the user.')
            return redirect('account:login')
    else:
        messages.error(request, 'You need to log in to access your account.')
        return redirect('account:login')
    

def index(request):
    return render(request, 'index.html' )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('account:login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('account:myAccount')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('account:myAccount')
            else:
                # Debug output to help diagnose authentication failure
                print(f"Failed login attempt: Phone Number - {phone_number}, Password - {password}")
                messages.error(request, 'Authentication failed. Please check your credentials.')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

 
def logout(request):
   auth.logout(request)
   messages.info(request, 'You are logged out.')
   return redirect('account:login')

@login_required
def profile(request):
    return render(request , 'profile.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            
            user =  User.objects.get(email=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('account:login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('account:forgot_password')
    return render(request, 'forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('account:reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('account:myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('account:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('account:reset_password')
    return render(request, 'reset_password.html')

@login_required
@user_passes_test(check_role_farmer)
def farmer_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('account:farmerdashboard')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
@user_passes_test(check_role_expert)
def expert_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('account:expertdashboard')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})



import requests
import urllib.request
import json
from django.shortcuts import render
from django.contrib import messages


@login_required
@user_passes_test(check_role_expert)
def expertdashboard(request):
    user = request.user
    city = user.city
    country = user.country

    visualcrossing_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}%20%2C%20{country}?unitGroup=metric&include=days%2Calerts&key={VISUALCROSSING_API}&contentType=json"

    try:
        result_bytes = urllib.request.urlopen(visualcrossing_url)
        jsonData = json.load(result_bytes)
    except Exception as e:
        jsonData = {'error': str(e)}
        messages.error(request, "Error fetching data from VisualCrossing API.")

    api_key_weather = f'{WEATHER_API}'
    weatherapi_url = f'http://api.weatherapi.com/v1/current.json?key={api_key_weather}&q={city}'

    try:
        # Sending WeatherAPI request and getting response
        response = requests.get(weatherapi_url)
        data = response.json()

        # Extracting necessary information from the API response
        location = data['location']['name']
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind_speed = data['current']['wind_kph']

        weather_data = {
            'Temperature (°C)': data['current']['temp_c'],
            'Condition': data['current']['condition']['text'],
            'Wind Speed (km/h)': data['current']['wind_kph'],
            'Humidity (%)': data['current']['humidity'],
            'Pressure (mb)': data['current']['pressure_mb'],
            'UV Index': data['current']['uv']
        }

        # Sending data to the template
        context = {
            'weather_data' : weather_data ,
            'location': location,
            'temperature': temperature,
            'condition': condition,
            'wind_speed': wind_speed,
            'jsonData': jsonData
        }
    except Exception as e:
        messages.error(request, "Error fetching data from WeatherAPI.")
        context = {'error': str(e)}

    return render(request, 'expertdashboard.html', context)



@login_required
@user_passes_test(check_role_farmer)
def farmerdashboard(request):
    user = request.user
    city = user.city
    country = user.country
    lat = user.latitude
    lon = user.longitude
    try: 
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}%20%2C%20{country}?unitGroup=metric&include=days%2Calerts&key=F7QME3Z9QPNC9CF24E95EY3QH&contentType=json"

        ResultBytes = urllib.request.urlopen(url)
        jsonData = json.load(ResultBytes)

        access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODc1NzE5LCJpYXQiOjE3MTY4NzU0MTksImp0aSI6IjU5MGI1ZjkzNGVhNDQ2ZDhhZTYxMDQ4ZTJmOTc2NzVjIiwidXNlcl9pZCI6NTB9.cRan0kkbldicavT5pZkEWe5nROVhOe1jdSqaeGcYt4w' 
        
        url = f"https://soil.narc.gov.np/soil/soildata/?lon={lon}&lat={lat}"

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        
        response_data = response.json()
        print(response_data)


        experts = User.objects.filter(role=User.EXPERT)[:5]
        # Pass the JSON data to the template
        context = {
            "jsonData": jsonData ,
            "experts" : experts ,
            "response_data" : response_data
        }

        return render(request , "farmerdashboard.html", context)

    except urllib.error.HTTPError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        
    except urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        
    return render(request , 'farmerdashboard.html' )


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            # Here you can access form.cleaned_data to get the validated form data
            # For example:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            documents = form.cleaned_data['documents']
            address = form.cleaned_data['address']
            contact = form.cleaned_data['contact']
            date = form.cleaned_data['date']
            experts = form.cleaned_data['experts']

            return render(request, 'index.html', {'form': form})
    else:
        form = AppointmentForm()
   
    return render(request , 'appointment.html', {'form': form})



@login_required
def videocall(request):
    return render(request, 'video_call.html', {'name': request.user.full_name})



@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST.get('roomID') 
        if roomID:
            return redirect("/account/meeting/?roomID=" + roomID)
    return render(request, 'joinroom.html')
    


@login_required(login_url='login')
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)



def expert_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('account:expert_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)
        
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'experts/expert_profile.html', context)

        
    





