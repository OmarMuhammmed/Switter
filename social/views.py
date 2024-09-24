from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser as User
from django.views import View
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count



class PostsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        userinfo = User.objects.get(username=request.user)
        # posts = Post.objects.all().order_by('-created_at')
        posts = Post.objects.annotate(count_comments=Count('comments')).order_by('-created_at')
        # count_comments = Comment.objects.count()
        form = PostForm()

        return render(request, 'home.html',{
            "posts":posts,
            "userinfo" : userinfo,
            "form": form ,
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user 
            new_post.save()
            messages.success(request,'Your Added Post Successfully..')
            return redirect('posts')
            
        return render(request, 'home.html',{"form":form})


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post,pk=pk)
        comment = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        count_comments = Comment.objects.filter(post=post).count()
        return render(request, 'post_detail.html', {
            'post': post,
            'comment' : comment,
            'comments' : comments ,
            'count_comments' : count_comments
            })

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post,pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            add_comment = comment_form.save(commit=False)
            add_comment.user = request.user
            add_comment.post = post
            add_comment.save()
            messages.success(request,'Your comment was added successfully.')
            return redirect('post_detail',pk=pk)
        
        return render(request, 'post_detail.html', {
            'post': post,
            'comment' : add_comment ,
            })
     
    


def profile(request):
    
    userinfo = User.objects.get(username=request.user)

    return render(request, 'profile.html',{"userinfo":userinfo})