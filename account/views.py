from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

from .models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import AppointmentForm, CustomPasswordChangeForm, LoginForm, RegistrationForm
from django.shortcuts import render, redirect
from .forms import LoginForm

import json
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
import sys
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page
def check_role_expert(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
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
            return redirect('account:myAccount')
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

    
#Logout
def logout(request):
   auth.logout(request)
   messages.info(request, 'You are logged out.')
   return redirect('account:login')


def profile(request):
    return render(request , 'profile.html')


#forgot Password Link
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            
            user =  User.objects.get(email=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'emails/reset_password_email.html'
            # send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('account:forgot_password')
    return render(request, 'forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
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
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('account:reset_password')
    return render(request, 'reset_password.html')


def farmer_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('account:farmerdashboard')
    else:
        # Pass user=request.user to initialize the form with the user's data
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def expert_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('account:expertdashboard')
    else:
        # Pass user=request.user to initialize the form with the user's data
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def expertdashboard(request):
    return render(request , 'expertdashboard.html')


@user_passes_test(check_role_farmer)
def farmerdashboard(request):
    user = request.user
    city = user.city
    country = user.country
    try: 
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}%20%2C%20{country}?unitGroup=metric&include=days%2Calerts&key=F7QME3Z9QPNC9CF24E95EY3QH&contentType=json"

        ResultBytes = urllib.request.urlopen(url)
        
        # Parse the results as JSON
        jsonData = json.load(ResultBytes)

        # Pass the JSON data to the template
        context = {
            "jsonData": jsonData
        }

        return render(request , "farmerdashboard.html", context)

    except urllib.error.HTTPError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        
    except urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        
    return render(request , 'farmerdashboard.html', context)


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
            
            # You can then save the data to your database or perform any other actions
            
            # Redirect to a success page or return a response
            # For example:
            return render(request, 'success.html', {'form': form})
    else:
        form = AppointmentForm()
   
    return render(request , 'appointment.html', {'form': form})



        






    



        
    





