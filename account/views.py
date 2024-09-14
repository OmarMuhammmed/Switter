from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser as User 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def home(request):
    # if not request.user.is_authenticated:
    #     return render(request,'login.html',{})
    return render(request,'home.html',{})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  
        if user is not None :
            login(request, user)  
            messages.success(request, 'Authenticated successfully')
            return redirect('home')
        else:
            messages.error(request, "Invalid login") 
            return redirect('/')
    
    return render(request,'login.html',{})
        

def user_singup(request):
    return render(request, 'signup.html',{})       


