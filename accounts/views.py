from django.shortcuts import render
from .models import Profile 
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.



def get_profile_redirect_url(user):
  
    profile = Profile.objects.get(user=user)
  
    return reverse('profile', kwargs={'slug': profile.slug})