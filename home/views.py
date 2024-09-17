from django.shortcuts import render
from accounts.models import CustomUser as User
# Create your views here.

def home(request):
    
    return render(request, 'home.html',{})


def profile(request):
    
    info = User.objects.all()

    return render(request, 'profile.html',{"info":info})