from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser as User
from django.views import View
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def home(request):
    return render(request, 'home.html',{})


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        userinfo = User.objects.get(username=request.user)
        posts = Post.objects.all().order_by('-created_at')

        form = PostForm()
        if form.is_valid():
            form.save()

        return render(request, 'home.html',{
            "posts":posts,
            "userinfo" : userinfo,
            "form": form , 
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)

            # link posts to user loggend In 
            new_post.user = request.user 

            new_post.save()
            messages.success(request,'Your Added Post Successfully..')
            return redirect('posts')
            
        return render(request, 'home.html',{"form":form})


def profile(request):
    
    userinfo = User.objects.get(username=request.user)
    print(userinfo)

    return render(request, 'profile.html',{"userinfo":userinfo})