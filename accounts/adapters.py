from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from .models import Profile

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        profile = Profile.objects.get(user=request.user)
        if not profile.slug:
            return reverse('home') 
        return reverse('profile', kwargs={'slug': profile.slug})
    
    def get_signup_redirect_url(self, request):
        profile = Profile.objects.get(user=request.user)
        if not profile.slug:
            return reverse('home') 
        return reverse('profile', kwargs={'slug': profile.slug})
