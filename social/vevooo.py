class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        userinfo = self.get_user_info(request)
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

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            self.add_post(form, request.user)
            messages.success(request, 'Your Added Post Successfully..')
            return redirect('home')

        action = request.POST.get('action')
        if action == 'follow':
            self.follow_user(request)

        return render(request, 'home.html', {"form": form})

    def get_user_info(self, request):
        """Retrieve the current user's profile information."""
        return Profile.objects.get(user=request.user)

    def get_posts(self):
        """Retrieve and annotate posts."""
        return Post.objects.annotate(
            count_comments=Count('comment'),
            count_reactions=Count('reaction'),
            count_shares=Count('shares')
        ).order_by('-created_at')

    def get_follow_counts(self, request):
        """Get counts of followers and following for the current user."""
        current_user_profile = request.user.profile
        followers_count = current_user_profile.followers.count()
        following_count = current_user_profile.following.count()
        return followers_count, following_count

    def get_recommended_followers(self, request):
        """Generate a list of recommended followers for the current user."""
        current_user_profile = request.user.profile
        current_user_followers = current_user_profile.followers.all()
        current_user_following = current_user_profile.following.all()

        recommended_followers_with_repetition = []
        
        for follower in current_user_followers:
            if follower != current_user_profile and follower not in current_user_following:
                recommended_followers_with_repetition.append(self.build_follower_dict(follower))

        for i_follow in current_user_following:
            for mutual_follower in i_follow.followers.all():
                if mutual_follower != current_user_profile and mutual_follower not in current_user_following:
                    recommended_followers_with_repetition.append(self.build_follower_dict(mutual_follower))
                    
        recommended_followers = [dict(t) for t in {tuple(d.items()) for d in recommended_followers_with_repetition}]
        return recommended_followers

    def build_follower_dict(self, follower):
        """Helper method to build a dictionary for a follower."""
        return {
            'frist_name': follower.user.first_name,
            'last_name': follower.user.last_name,
            'username': follower.user.username,
            'profile_image_url': follower.image.url if follower.image else None,
            'profile_link': reverse('profile', args=[follower.user.username])
        }

    def add_post(self, form, user):
        """Save a new post associated with the current user."""
        new_post = form.save(commit=False)
        new_post.user = user
        new_post.save()

    def follow_user(self, request):
        """Follow a user based on the username provided."""
        username_to_follow = request.POST.get('username')  
        user_profile = Profile.objects.filter(user__username=username_to_follow).first()
        if user_profile and user_profile != request.user.profile:
            user_profile.followers.add(request.user.profile)
            messages.success(request, 'You follow @{}'.format(user_profile.user.username))