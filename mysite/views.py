from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .forms import RegisterForm, ProfileForm
from .models import Profile
import logging
from datetime import datetime, timedelta
from django.utils import timezone


logging.basicConfig(filename='user_activity.log', level=logging.INFO)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'mysite/register.html', {'form': form})

# Issue four: Security Logging and Monitoring Failures. We wish to see who logs into our system, from where and when so we can detect suspicious activity.
# You can see the logs in the root directory "user_activity.log"
# Fix: Uncomment the "logging" lines from within login_view.

# Issue five: Insecure design. We're preventing a user account from being accessed after too many failed logins in a short period of time to prevent bruteforces.
# Fix: Uncomment the set of lines I've marked as Issue Five.

MAX_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION = timedelta(seconds=30) # You can change this duration as you see fit, I've set this to 30 seconds for testing purposes. You can see the timer difference in console.

def login_view(request):
    username = request.POST.get('username') if request.method == "POST" else None
    client_ip = get_client_ip(request)
    user = User.objects.filter(username=username).first()

    # Uncomment this for fix! Issue five
    #if user and user.profile.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
    #    current_timestamp = timezone.now().timestamp()
    #    last_failed_timestamp = user.profile.last_failed_login.timestamp()
    #    time_difference_in_seconds = current_timestamp - last_failed_timestamp
    #    print("ConsoleLog: Too many attempts! Attempts: ",user.profile.failed_login_attempts," / ",time_difference_in_seconds)
    #    if time_difference_in_seconds < LOCKOUT_DURATION.total_seconds():
    #        return render(request, 'mysite/login.html', {'error': 'Too many failed attempts. Please wait.'})
    #    else:
    #        user.profile.failed_login_attempts = 0
    #        user.profile.save()

    if request.method == "POST":
        password = request.POST.get('password')
        authenticated_user = authenticate(request, username=username, password=password)
        
        if authenticated_user:
            if not hasattr(authenticated_user, 'profile'):
                Profile.objects.create(user=authenticated_user)
            login(request, authenticated_user)
            user.profile.failed_login_attempts = 0
            user.profile.save()
            #logging.info("[" + str(timezone.now()) + "] User '" + username + "' has logged in from IP address " + client_ip) # Uncomment for fix! Issue four
            return redirect('index')
        else:
            if user:
                user.profile.failed_login_attempts += 1
                user.profile.last_failed_login = timezone.now()
                user.profile.save()
                print("ConsoleLog: Failed login, attempts: ",user.profile.failed_login_attempts)
            #logging.info("[" + str(timezone.now()) + "] Failed login attempt for username: " + username + " from IP address " + client_ip) # Uncomment for fix! Issue four

    return render(request, 'mysite/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'mysite/index.html')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'mysite/profile.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    # Issue two: Broken access control, user is able to update bio of accounts that they aren't the owners of.
    # Fix: Uncomment the lines below

    #if user != request.user and request.method == 'POST':
    #    print("Requesting user is not same as the target: ",request.user," and ",user)
    #    return HttpResponseForbidden("You don't have permission to edit this profile.")

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=username)
    else:
        form = ProfileForm(instance=user.profile)
    
    context = {
        'form': form
    }
    return render(request, 'mysite/profile.html', context)




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip