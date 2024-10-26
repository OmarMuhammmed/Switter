from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser as User , Profile
from django.views import View
from .models import Post, Comment, ReplyComment, Reaction
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ReplyCommentForm
from accounts.forms import BioForm, ImageForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        userinfo = Profile.objects.get(user=request.user)
        posts = Post.objects.annotate(
            count_comments=Count('comment'), 
            count_reactions=Count('reaction'),
            count_shares=Count('shares')  
        ).order_by('-created_at')
        
        user_profile = request.user.profile
        followers_count = user_profile.followers.count()
        following_count = user_profile.following.count()
        
        form = PostForm()

        return render(request, 'home.html',{
            "posts":posts,
            "userinfo" : userinfo,
            "form": form ,
            "followers_count":followers_count,
            "following_count":following_count,
            

        })
    
    def post(self, request, *args, **kwargs):
        # add post 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user 
            new_post.save()
            messages.success(request,'Your Added Post Successfully..')
            return redirect('home')
            
        return render(request, 'home.html',{"form":form})

@login_required
def post_detail(request, pk, slug=None):      
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    count_comments = comments.count()
    replis = ReplyComment.objects.filter(post=post).count()
    total_comments_replis = count_comments + replis

    update_post_form = PostForm(instance=post)
    comment_form = CommentForm()
    reply_form = ReplyCommentForm()

    userinfo = Profile.objects.get(user=request.user)
    users_who_loved = post.reaction.values_list('user', flat=True)

    user_profile = request.user.profile
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()

    return render(request, 'post_detail.html', {
        'post': post,
        'comment': comment_form,
        'comments': comments,
        'count_comments': count_comments,
        'reply_form': reply_form,
        'update_post_form':update_post_form,
        'total_comments_replis' : total_comments_replis,
        'userinfo' : userinfo,
        'users_who_loved':users_who_loved,
        'followers_count' : followers_count, 
        'following_count' :following_count,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user :
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Your Post was Deleted successfully..')
            return redirect('home')
    else :
            messages.error(request, 'Your Denied to  Delete this Post ! ')
            return redirect('post_detail', pk=pk)            
        
        
    return render(request, 'post_detail.html',{'post':post})    

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        update_post_form = PostForm(request.POST,request.FILES ,instance=post)
        
        if post.user == request.user :
            if update_post_form.is_valid():
               
                update_post = update_post_form.save(commit=False)
                update_post.user = request.user
                created_at = timezone.now()
                update_post.created_at = created_at
                update_post.save()
                messages.success(request, 'Your Post was Updated successfully..')
                return redirect('post_detail', pk=pk)
            else :
                update_post_form = PostForm(request.FILES ,instance=post)
        else :
            messages.error(request, 'Your Denied to Edit  this Post ! ')
            return redirect('post_detail', pk=pk)          
            

    return render(request, 'post_detail.html',{
        'update_post_form':update_post_form,
        'post': post,
         })  
 
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.POST :
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            add_comment = comment_form.save(commit=False)
            add_comment.user = request.user
            add_comment.post = post
            add_comment.save()
            messages.success(request, 'Your comment was added successfully.')
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
        
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

@login_required
def delete_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    print('DELETE '*30)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this comment.')

    return redirect('post_detail', pk=pk)

@login_required
def add_reply(request, pk):
    if request.method == "POST":

        post = get_object_or_404(Post, pk=pk)
        reply_form = ReplyCommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        parent_reply = None

        if parent_id:
            parent_reply = get_object_or_404(ReplyComment, pk=parent_id)

        if reply_form.is_valid():
            parent_comment_id = request.POST.get('comment_id')
           
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

@login_required
def manage_reatcions(request, pk):
    post = get_object_or_404(Post, pk=pk)

    reaction = Reaction.objects.filter(post=post, user=request.user).first()

    if reaction:
        reaction.delete()
        loved = False
    else:
        Reaction.objects.create(post=post, user=request.user)
        loved = True
       
    return JsonResponse({
    'loved': loved,
    'reactions_count': post.reaction.count()
})

@login_required
def profile(request, slug):
    user_profile = get_object_or_404(Profile, slug=slug)
    posts = Post.objects.filter(user=user_profile.user).order_by('-created_at')

    if request.method == 'POST': 
        img_form = ImageForm(request.POST, request.FILES, instance=user_profile)
        bio_form = BioForm(request.POST, instance=user_profile)
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Your Added Post Successfully..')
            return redirect('profile', slug=slug)

        if bio_form.is_valid():
            bio_form.save()
        
        if img_form.is_valid():
            img_form.save()

        # Handle follow, unfollow actions
        action = request.POST.get('action')
        if action == 'follow':
            user_profile.followers.add(request.user.profile)
            messages.success(request, 'You follow @{}'.format(user_profile.user.username))
            return redirect('profile', slug=slug)

        elif action == 'unfollow':
            user_profile.followers.remove(request.user.profile)
            messages.success(request, 'You Unfollow @{}'.format(user_profile.user.username))
            return redirect('profile', slug=slug)

    else:
        img_form = ImageForm(instance=user_profile)
        bio_form = BioForm(instance=user_profile)
        post_form = PostForm()

   
    is_following = user_profile.followers.filter(user=request.user).exists()
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()
    following_users = user_profile.following.all()
    followers_users = user_profile.followers.all()

    return render(request, 'profile.html', {
        "userinfo": user_profile,
        'bio_form': bio_form,
        'img_form': img_form,
        'posts': posts,
        'post_form': post_form,
        'is_following': is_following,
        'followers_count': followers_count,
        "following_count" : following_count,
        "following_users": following_users,
        "followers_users":followers_users, 
    })


def share_post(request, pk):
    original_post = get_object_or_404(Post, pk=pk)
    shared_post = Post.objects.create(
        user=request.user, 
        shared_post=original_post,
        body=original_post.body,  
        image=original_post.image  
    )
    original_post.share_count += 1
    original_post.save()
    return redirect('home')
