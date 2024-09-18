from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustomUser as User
from django.views import View
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html',{})


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        userinfo = User.objects.get(username= request.user)
        posts = Post.objects.all().order_by('-created_at')
        print(userinfo)
        print(posts)
        return render(request, 'home.html',{
            "posts":posts,
            "userinfo" : userinfo,
        })

def profile(request):
    
    userinfo = User.objects.get(username=request.user)
    print(userinfo)

    return render(request, 'profile.html',{"userinfo":userinfo})