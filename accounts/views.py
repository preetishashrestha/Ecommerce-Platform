"""
Authentication part
"""
import re
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
def register(request):
    '''
    Authentication part for the register part
    '''
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            if CustomUser.objects.filter(username==username).exits():
                messages.error(request,'username is already taken!!')
                return redirect('register')
            if CustomUser.objects.filter(email==email).exists():
                messages.error(request,'email already exits')
                return redirect('register')
            if not re.search(r'[A-Z]',password):
                messages.error(request,'Your password should atleast contain one uppercase letter!! ]')
                return redirect('register')
            if not re.search(r'/d',password):
                messages.error(request,'Your password should contain atleast one digits')
                return redirect('register')
            try:
                validate_password(password)
                CustomUser.objects.create_user(fistn_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"Account created sucessfully!!")
                return redirect('register')
            except ValidationError as e:
                for i  in e.messages:
                    messages.error(request,i)
                return redirect('register')
        else:
            messages.error(request,"Password and confirm password do not match")
            return redirect('request')
    return render(request,'accounts/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username')
    return render(request,'login.html')


