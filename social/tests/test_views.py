import pytest
from django.urls import reverse
from social.models import Reaction

@pytest.mark.django_db
def test_home_page(client, test_user):
    
    client.force_login(test_user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'posts' in response.context


@pytest.mark.django_db
def test_add_reaction(client, post, test_user):
    """ اختبار إضافة reaction لأول مرة """
    url = reverse("manage_reactions", args=[post.id])  # استبدل باسم الـ URL المناسب
    response = client.post(url)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["loved"] is True
    assert Reaction.objects.filter(post=post, user=test_user).exists()
    assert json_data["reactions_count"] == 1

@pytest.mark.django_db
def test_remove_reaction(authenticated_client, post, test_user):
    """ اختبار إزالة reaction عند الضغط عليه مرة أخرى """
    # إضافة reaction أولاً
    Reaction.objects.create(post=post, user=test_user)
    
    url = reverse("manage_reactions", args=[post.id])
    response = authenticated_client.post(url)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["loved"] is False
    assert not Reaction.objects.filter(post=post, user=test_user).exists()
    assert json_data["reactions_count"] == 0

@pytest.mark.django_db
def test_anonymous_user_cannot_react(client, post):
    """ اختبار عدم السماح للمستخدم غير المسجل بعمل reaction """
    url = reverse("manage_reactions", args=[post.id])
    response = client.post(url)

    assert response.status_code == 302  # مفترض يعيد التوجيه إلى تسجيل الدخول
    assert Reaction.objects.count() == 0  # لا يتم إضافة أي Reaction
