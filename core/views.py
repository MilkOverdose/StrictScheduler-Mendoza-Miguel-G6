from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('member_dashboard')
    return render(request, 'core/admin_dashboard.html')

@login_required
def member_dashboard(request):
    if request.user.role != 'MEMBER':
        messages.error(request, 'Access denied. Members only.')
        return redirect('admin_dashboard')
    return render(request, 'core/member_dashboard.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})
