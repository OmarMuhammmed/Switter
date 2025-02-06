from django.contrib.auth import get_user_model
from social.models import Post, Comment, Reaction
import pytest

User = get_user_model()

@pytest.mark.django_db
def test_post_model():
    
    user = User.objects.create(first_name ="test",last_name="user",username='testuser', password='password')
    post = Post.objects.create(
        user=user,
        body="This is a test post."
    )
    
   
    assert post.user == user
    assert post.body == "This is a test post."
    

@pytest.mark.django_db
def test_comment_model():
    user = User.objects.create(username='testuser')
    post = Post.objects.create(user=user, body="Test post")
    comment = Comment.objects.create(
        user=user,
        post=post,
        body="Test comment"
    )
    
    assert comment.post == post
    assert comment.post.user == user


@pytest.mark.django_db
def test_reaction_model():
    user = User.objects.create(username='testuser')
    post = Post.objects.create(user=user, body="Test post")
    reaction = Reaction.objects.create(user=user, post=post)
    
    assert reaction.post == post
    assert reaction.user == user
