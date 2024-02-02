from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm

from django.contrib import messages

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignupForm()
        
    return render(request, 'reglog/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            
    else:
        form = LoginForm()
    return render(request, 'reglog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')