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
from django.core.cache import cache

class HomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        userinfo = Profile.objects.get(user=request.user)
        posts = self.get_posts()
        followers_count, following_count = self.get_follow_counts(request)
        recommended_followers = self.get_recommended_followers(request)
        
        form = PostForm()
 
        return render(request, 'home.html', {
            "posts": posts,
            "userinfo": userinfo,
            "form": form,
            "followers_count": followers_count,
            "following_count": following_count,
            "recommended_followers": recommended_followers,
        })

    def get_follow_counts(self, request):
        current_user_profile = request.user.profile
        followers_count = current_user_profile.followers.count()
        following_count = current_user_profile.following.count()
        return followers_count, following_count
    
    def get_posts(self):
        return Post.objects.annotate(
            count_comments=Count('comment'),
            count_reactions=Count('reaction'),
            count_shares=Count('shares')
        ).order_by('-created_at')
    
    def get_recommended_followers(self, request):
        current_user_profile = request.user.profile
        current_user_followers = current_user_profile.followers.all()
        current_user_following = current_user_profile.following.all()
       
        recommended_followers_with_repetition = []
        
        for follower in current_user_followers:
            if follower != current_user_profile and follower not in current_user_following:
                recommended_followers_with_repetition.append({
                    'frist_name': follower.user.first_name,
                    'last_name': follower.user.last_name,
                    'username': follower.user.username,
                   'profile_image_url': follower.image.url if follower.image else None,  
                    'profile_link': reverse('profile', args=[follower.user.username])
                })

        for i_follow in current_user_following:
            for mutual_follower in i_follow.followers.all():
                if mutual_follower != current_user_profile and  mutual_follower not in current_user_following:
                    recommended_followers_with_repetition.append({
                        'frist_name': mutual_follower.user.first_name,
                        'last_name': mutual_follower.user.last_name,
                        'username': mutual_follower.user.username,
                        'profile_image_url': mutual_follower.image.url if mutual_follower.image else None,
                        'profile_link': reverse('profile', args=[mutual_follower.user.username])  
                })
                    
        recommended_followers = [dict(t) 
                                for t in {tuple(d.items()) 
                                for d in recommended_followers_with_repetition}
                                ]
        return recommended_followers
            
    def post(self, request, *args, **kwargs):
        # add post 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user 
            new_post.save()
            
            # Update only profile page cache
            profile_posts_key = f'user_posts_{request.user.username}'
            user_posts = Post.objects.filter(user=request.user).annotate(
                count_comments=Count('comment'),
                count_reactions=Count('reaction'),
                count_shares=Count('shares')
            ).order_by('-created_at')
            cache.set(profile_posts_key, user_posts, timeout=300)
            
            messages.success(request,'Your Added Post Successfully..')
            return redirect('home')
        action = request.POST.get('action')
        if action == 'follow':
            self.follow_from_recommendation(request)
            return redirect('home')
        
    def follow_from_recommendation(self, request):
        username_to_follow = request.POST.get('username')  
        user_profile = Profile.objects.filter(user__username=username_to_follow).first()
        if user_profile and user_profile != request.user.profile:
            user_profile.followers.add(request.user.profile)
            messages.success(request, 'You follow @{}'.format(user_profile.user.username))
    

@login_required
def post_detail(request, pk, slug=None):      
    # Delete cache first to ensure fresh data
    cache.delete(f"profile_data_{request.user.profile.slug}")
    
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
    if post.user == request.user:
        if request.method == 'POST':
            # Delete cache for the user's profile
            cache_key = f"profile_data_{post.user.profile.slug}"
            cache.delete(cache_key)
            
            # Delete the post
            post.delete()
            messages.success(request, 'Your Post was Deleted successfully..')
            return redirect('home')
    else:
        messages.error(request, 'Your Denied to Delete this Post!')
        return redirect('post_detail', pk=pk)            
    
    return render(request, 'post_detail.html',{'post':post})    

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        update_post_form = PostForm(request.POST,request.FILES ,instance=post)
        
        if post.user == request.user:
            if update_post_form.is_valid():
                update_post = update_post_form.save(commit=False)
                update_post.user = request.user
                created_at = timezone.now()
                update_post.created_at = created_at
                update_post.save()

                # Delete profile cache first
                cache.delete(f"profile_data_{post.user.profile.slug}")
                
                # Update profile page cache with fresh data
                profile_posts_key = f'user_posts_{post.user.username}'
                user_posts = Post.objects.filter(user=post.user).annotate(
                    count_comments=Count('comment'),
                    count_reactions=Count('reaction'),
                    count_shares=Count('shares')
                ).order_by('-created_at')
                cache.set(profile_posts_key, user_posts, timeout=300)
                
                messages.success(request, 'Your Post was Updated successfully..')
                return redirect('post_detail', pk=pk)
            else:
                update_post_form = PostForm(request.FILES ,instance=post)
        else:
            messages.error(request, 'Your Denied to Edit this Post!')
            return redirect('post_detail', pk=pk)          

    return render(request, 'post_detail.html', {
        'update_post_form': update_post_form,
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

class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request, slug):

        cache_key = f"profile_data_{slug}"

        
        data = cache.get(cache_key)

        
        if not data or not isinstance(data, dict) or "userinfo" not in data:
            user_profile = get_object_or_404(Profile, slug=slug)
            posts = Post.objects.filter(user=user_profile.user).select_related('user').order_by('-created_at')

            is_following = user_profile.followers.filter(user=request.user).exists()
            data = {
                "userinfo": user_profile,
                'posts': posts,
                'is_following': is_following,
                'followers_count': user_profile.followers.count(),
                "following_count": user_profile.following.count(),
                "following_users": user_profile.following.all(),
                "followers_users": user_profile.followers.all(),
            }

            
            cache.set(cache_key, data, 900)

            img_form = ImageForm(instance=data["userinfo"])
            bio_form = BioForm(instance=data["userinfo"])
            post_form = PostForm()

            data.update({
            'bio_form': bio_form,
            'img_form': img_form,
            'post_form': post_form,
            })
            
            return render(request, self.template_name, data)

        
        img_form = ImageForm(instance=data["userinfo"])
        bio_form = BioForm(instance=data["userinfo"])
        post_form = PostForm()

        data.update({
            'bio_form': bio_form,
            'img_form': img_form,
            'post_form': post_form,
        })

        return render(request, self.template_name, data)

    def post(self, request, slug):
        user_profile = get_object_or_404(Profile, slug=slug)

        img_form = ImageForm(request.POST, request.FILES, instance=user_profile)
        bio_form = BioForm(request.POST, instance=user_profile)
        post_form = PostForm(request.POST)

        cache_key = f"profile_data_{slug}"

      
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            cache.delete(cache_key)  
            messages.success(request, 'Your post was added successfully.')
            return redirect('profile', slug=slug)

       
        if bio_form.is_valid():
            bio_form.save()
            cache.delete(cache_key)  

        
        if img_form.is_valid():
            img_form.save()
            cache.delete(cache_key)  

       
        action = request.POST.get('action')
        if action == 'follow':
            user_profile.followers.add(request.user.profile)
            cache.delete(cache_key)  # Delete target user's cache
            cache.delete(f"profile_data_{request.user.profile.slug}")  # Delete current user's cache
            messages.success(request, f'You follow @{user_profile.user.username}')
            return redirect('profile', slug=slug)

        elif action == 'unfollow':
            user_profile.followers.remove(request.user.profile)
            cache.delete(cache_key)  # Delete target user's cache
            cache.delete(f"profile_data_{request.user.profile.slug}")  # Delete current user's cache
            messages.success(request, f'You unfollow @{user_profile.user.username}')
            return redirect('profile', slug=slug)


        return redirect('profile', slug=slug)

    @staticmethod
    def update_cache(user_profile, cache_key, is_following):
        data = {
            "userinfo": user_profile,
            'posts': Post.objects.filter(user=user_profile.user).select_related('user').order_by('-created_at'),
            'is_following': is_following,
            'followers_count': user_profile.followers.count(),
            "following_count": user_profile.following.count(),
            "following_users": user_profile.following.all(),
            "followers_users": user_profile.followers.all(),
        }
        cache.set(cache_key, data, 900)

@login_required
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
