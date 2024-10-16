from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from .models import Profile

class MyAccountAdapter(DefaultAccountAdapter):
    print("My Acocunt Adapter loaded")
    def get_login_redirect_url(self, request):
        print("$"*30)
        profile = Profile.objects.get(user=request.user)
        if not profile.slug:
            return reverse('home') 
        return reverse('profile', kwargs={'slug': profile.slug})
