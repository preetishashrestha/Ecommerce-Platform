"""
Authentication part
"""
import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm
def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password == password1:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request,'username is already exists')
                return redirect('register')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request,'email already exits')
                return redirect('register')
            

            if not re.search(r'[A-Z]',password):
                messages.error(request,'Your password does not contain at least one uppercase')
                return redirect('register')
            
            if not re.search(r"\d",password):
                messages.error(request,'Your password does not contain at least one digit!!')
                return redirect('register')
            
            try:
                validate_password(password)
                CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,'Account Created Sucessfully!!')
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                return redirect('register')
        else:
            messages.error(request,'Password and Confirm Password does not match!!')
            return redirect('register')

    return render(request, 'accounts/register.html')

def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me = request.POST.get('remember_me')


        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request,'username not register yet!!!')
            return redirect('log_in')

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(3600)
            else:
                request.session.set_expiry(0)
            next =request.POST.get('next','')

            return redirect(next if next else "index")
        else:
            messages.error(request,'Password in valid!!')
            return redirect('log_in')
        
    next=request.GET.get('next','')

    return render(request,'accounts/login.html',{'next':next})

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'accounts/password_change.html',{'form':form})
# profile
@login_required(login_url='log_in')
def profile_dashboard(request):
    return render(request, 'profile/dashboard.html')

@login_required(login_url='log_in')
def profile(request):
    profile,create= Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method=="POST":
        form=ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
    context={
        'form':form
    }
    return render(request, 'profile/profile.html', context)

