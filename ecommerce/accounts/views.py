from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email,validate_integer
from django.contrib.auth.password_validation import validate_password
import re


# Create your views here.
def user_login(request):
    if request.method == "POST":  
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        messages.info(request,"Login Failed,please Try Again")
    return render(request,'accounts/login.html')
    




# def user_register(request):
#     if request.method == "POST":  
#         username=request.POST.get('username')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         confirm_password=request.POST.get('confirm_password')
#         phone=request.POST.get('phone_field')
#        # print(username,email)
#         if password == confirm_password:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,"username is already exists")
#                 return redirect('user_register')
#             else:
#                 if User.objects.filter(email=email).exists():
#                     messages.info(request,"email is already exists")
#                     return redirect('user_register')
#                 else:
#                     user = User.objects.create_user(username=username,email=email,password=password)
#                     user.save()
#                     data=Customer(user = user,phone_field=phone)
#                     data.save()
                    
#                     our_user=authenticate(username=username,password=password)
#                     if our_user is not None:
#                         login(request,user)
#                         return redirect('/')
#         else:
#             messages.info(request,"password and confirm password mismatch.!")
#         return redirect('user_register')
                
#     return render(request,'accounts/register.html')
def user_register(request):
    if request.method == "POST":  
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')

        # Password validation rules
        if (
            len(password) < 8 or             # Minimum length
            not re.search(r'\d', password) or   # At least one digit
            not re.search(r'[A-Za-z]', password) or  # At least one letter
            not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>/?]', password)  # At least one special character
        ):
            messages.info(request, "Password must be at least 8 characters long and include at least one digit, one letter, and one special character")
            return redirect('user_register')

        if password != confirm_password:
            messages.info(request, "Password and confirm password mismatch!")
            return redirect('user_register')

        try:
            # Validate email format
            validate_email(email)
        except ValidationError:
            messages.info(request, "Invalid email format")
            return redirect('user_register')

        # Validate phone number format
        if not re.match(r'^\+?1?\d{10}$', phone):
            messages.info(request, "Invalid phone number format")
            return redirect('user_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('user_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('user_register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            data = Customer(user=user, phone_field=phone)
            data.save()
            
            # Authenticate and login the user
            our_user = authenticate(username=username, password=password)
            if our_user is not None:
                login(request, user)
                return redirect('/')
                
    return render(request, 'accounts/register.html')





def user_logout(request):
    logout(request)
    return redirect('/')

