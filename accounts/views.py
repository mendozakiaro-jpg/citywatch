from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Profile


def admin_check(user):
    return user.is_staff or user.is_superuser


def landing_view(request):
    from reports.models import Report

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('analytics_dashboard')
        else:
            return redirect('resident_dashboard')

    recent_reports = Report.objects.all().order_by('-date_submitted')[:6]
    total_reports = Report.objects.count()
    resolved_count = Report.objects.filter(status='resolved').count()

    return render(request, 'accounts/landing.html', {
        'recent_reports': recent_reports,
        'total_reports': total_reports,
        'resolved_count': resolved_count,
    })


def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        barangay = request.POST.get('barangay')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        if full_name:
            name_parts = full_name.strip().split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
            user.save()

        Profile.objects.create(user=user, role='resident', phone_number=phone, barangay=barangay)

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('analytics_dashboard')
            else:
                return redirect('resident_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.barangay = request.POST.get('barangay')
        profile.save()
        messages.success(request, 'Profile updated successfully')
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
@user_passes_test(admin_check)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(admin_check)
def toggle_staff(request, user_id):
    target_user = User.objects.get(id=user_id)
    if request.method == 'POST' and target_user != request.user:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
        messages.success(request, f'Updated staff status for {target_user.username}.')
    return redirect('user_list')