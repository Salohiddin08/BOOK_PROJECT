from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            print('salom')
            return redirect('home')
        else:
            print('alik')
            messages.warning(request, 'Invalid username or password')
            return render(request, 'login.html')
        
    else:
        return render(request, 'login.html')
    
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if confirm_password == password:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'You are now registered')
            return redirect('login')
        else:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')
    
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', context={'user': user})

@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('image')
        
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if image:
            user.image = image
        user.save()
        messages.success(request, 'Profile updated successfully') 
        return redirect('profile')
    return render(request, 'profile-edit.html', context={'user': user})