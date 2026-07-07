from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.views.generic import View

# token - mail confirmation import
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .form import RegisterCustomerForm



# register customer
def register_user(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.warning(request, 'User created')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('register_user')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'account_app/register_user.html', context)
    
    
# login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'account_app/login.html')

# logout
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

