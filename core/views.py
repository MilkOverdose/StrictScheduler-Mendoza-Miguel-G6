from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
from .models import Goal, Routine
from .forms import GoalForm, RoutineForm

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

def is_admin_user(user):
    role = str(getattr(user, 'role', '')).upper()
    return user.is_superuser or user.is_staff or role == 'ADMIN'


# ================= GOAL CRUD =================

@login_required
def goal_list(request):
    if is_admin_user(request.user):
        goals = Goal.objects.select_related('user').prefetch_related('routines').all()
    else:
        goals = Goal.objects.filter(user=request.user).prefetch_related('routines')
    return render(request, 'core/goal_list.html', {'goals': goals, 'is_admin': is_admin_user(request.user)})

@login_required
def goal_detail(request, pk):
    if is_admin_user(request.user):
        goal = get_object_or_404(Goal, pk=pk)
    else:
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
    routines = goal.routines.all().order_by('start_time')
    return render(request, 'core/goal_detail.html', {
        'goal': goal,
        'routines': routines,
        'is_admin': is_admin_user(request.user),
    })



@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal created successfully!")
            return redirect('goal_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()
    return render(request, 'core/goal_form.html', {'form': form, 'action': 'Create Goal'})


@login_required
def goal_update(request, pk):
    if is_admin_user(request.user):
        goal = get_object_or_404(Goal, pk=pk)
    else:
        goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated successfully!")
            return redirect('goal_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm(instance=goal)
    return render(request, 'core/goal_form.html', {'form': form, 'action': 'Edit Goal'})


@login_required
def goal_delete(request, pk):
    if is_admin_user(request.user):
        goal = get_object_or_404(Goal, pk=pk)
    else:
        goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.delete()
        messages.success(request, "Goal and its linked routines deleted.")
        return redirect('goal_list')
    return render(request, 'core/confirm_delete.html', {'object': goal, 'type': 'Goal', 'cancel_url': 'goal_list'})


# ================= ROUTINE CRUD =================

@login_required
def routine_list(request):
    if is_admin_user(request.user):
        routines = Routine.objects.select_related('user', 'goal').all()
    else:
        routines = Routine.objects.filter(user=request.user).select_related('goal')
    return render(request, 'core/routine_list.html', {'routines': routines, 'is_admin': is_admin_user(request.user)})


@login_required
def routine_create(request):
    if not Goal.objects.filter(user=request.user).exists():
        messages.error(request, "Create a Goal first before adding a Routine.")
        return redirect('goal_create')

    if request.method == 'POST':
        form = RoutineForm(request.POST, user=request.user)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.save()
            messages.success(request, "Routine created successfully!")
            return redirect('routine_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = RoutineForm(user=request.user)
    return render(request, 'core/routine_form.html', {'form': form, 'action': 'Create Routine'})


@login_required
def routine_update(request, pk):
    if is_admin_user(request.user):
        routine = get_object_or_404(Routine, pk=pk)
        form_user = routine.user
    else:
        routine = get_object_or_404(Routine, pk=pk, user=request.user)
        form_user = request.user

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine, user=form_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Routine updated successfully!")
            return redirect('routine_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = RoutineForm(instance=routine, user=form_user)
    return render(request, 'core/routine_form.html', {'form': form, 'action': 'Edit Routine'})


@login_required
def routine_delete(request, pk):
    if is_admin_user(request.user):
        routine = get_object_or_404(Routine, pk=pk)
    else:
        routine = get_object_or_404(Routine, pk=pk, user=request.user)

    if request.method == 'POST':
        routine.delete()
        messages.success(request, "Routine deleted successfully!")
        return redirect('routine_list')
    return render(request, 'core/confirm_delete.html', {'object': routine, 'type': 'Routine', 'cancel_url': 'routine_list'})
