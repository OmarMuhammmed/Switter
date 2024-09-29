from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser as User
from django.views import View
from .models import Post, Comment, ReplyComment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ReplyCommentForm
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        userinfo = User.objects.get(username=request.user)
        posts = Post.objects.annotate(count_comments=Count('comment')).order_by('-created_at')
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
            return redirect('home')
            
        return render(request, 'home.html',{"form":form})

@login_required
def post_detail(request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    count_comments = comments.count()

    if request.method == "POST":
        return add_comment(request, pk)  
    
   
    update_post_form = PostForm(instance=post)
    comment_form = CommentForm()
    reply_form = ReplyCommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comment': comment_form,
        'comments': comments,
        'count_comments': count_comments,
        'reply_form': reply_form,
        'update_post_form':update_post_form
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your Post was Deleted successfully..')
        return redirect('home')
    
    return render(request, 'post_detail.html',{'post':post})    

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        update_post_form = PostForm(request.POST, instance=post)
        
        
        if update_post_form.is_valid():
            print('$'*200)
            update_post = update_post_form.save(commit=False)
            update_post.user = request.user
            created_at = timezone.now()
            update_post.created_at = created_at
            update_post.save()
            messages.success(request, 'Your Post was Updated successfully..')
            return redirect('post_detail', pk=pk)
        else :
            update_post_form = PostForm(instance=post)

    return render(request, 'post_detail.html',{
        'update_post_form':update_post_form,
        'post': post,
         })  
 
@login_required
def add_comment(request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            add_comment = comment_form.save(commit=False)
            add_comment.user = request.user
            add_comment.post = post
            add_comment.save()
            messages.success(request, 'Your comment was added successfully.')
            return redirect('post_detail', pk=pk)

        comments = Comment.objects.filter(post=post).order_by('-created_at')
        count_comments = comments.count()
        reply_form = ReplyCommentForm()
        
        return render(request, 'post_detail.html', {
            'post': post,
            'comment': comment_form,
            'comments': comments,
            'count_comments': count_comments,
            'reply_form': reply_form,
        })


class CommentView(LoginRequiredMixin, View):
    def post(request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            add_comment = comment_form.save(commit=False)
            add_comment.user = request.user
            add_comment.post = post
            add_comment.save()
            messages.success(request, 'Your comment was added successfully.')
            return redirect('post_detail', pk=pk)

        comments = Comment.objects.filter(post=post).order_by('-created_at')
        count_comments = comments.count()
        reply_form = ReplyCommentForm()
        
        return render(request, 'post_detail.html', {
            'post': post,
            'comment': comment_form,
            'comments': comments,
            'count_comments': count_comments,
            'reply_form': reply_form,
        })
    
    # def put(request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     comment_form = CommentForm(request.POST,instance=request.data)
    #     if comment_form.is_valid():
    #         comment_form.update()
    #         messages.success(request, 'Your comment was added successfully.')
    #         return redirect('post_detail', pk=pk)

    #     comments = Comment.objects.filter(post=post).order_by('-created_at')
    #     count_comments = comments.count()
    #     reply_form = ReplyCommentForm()


@login_required
def add_reply(request, pk):
    if request.method == "POST":
        print("POST data:", request.POST)  

        post = get_object_or_404(Post, pk=pk)
        reply_form = ReplyCommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        parent_reply = None

        if parent_id:
            parent_reply = get_object_or_404(ReplyComment, pk=parent_id)

        if reply_form.is_valid():
            parent_comment_id = request.POST.get('comment_id')
            print("Comment ID:", parent_comment_id)  
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            
            add_reply = reply_form.save(commit=False)
            add_reply.user = request.user
            add_reply.post = post
            add_reply.parent_comment = parent_comment
            add_reply.parent_reply = parent_reply
            add_reply.save()

            messages.success(request, 'Your reply was added successfully.')
            return redirect('post_detail', pk=pk)

    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post).prefetch_related('replies').order_by('-created_at')
    count_comments = comments.count()
    reply_form = ReplyCommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comment': comment_form,
        'comments': comments,
        'count_comments': count_comments,
        'reply_form': reply_form,
    })


def profile(request):
    
    userinfo = User.objects.get(username=request.user)

    return render(request, 'profile.html',{"userinfo":userinfo})