import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        first_name='Test',
        last_name='User',
        email='test@example.com'
    )
    return user

@pytest.fixture
def post(db, test_user):
    from social.models import Post
    post = Post.objects.create(user=test_user, body='Test post')
    return post