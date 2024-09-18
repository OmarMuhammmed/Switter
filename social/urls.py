from django.urls import path
from .import views

urlpatterns = [

    path('home',views.home , name='home'),
    path('accounts/profile/',views.profile, name='profile'),
    path('',views.PostListView.as_view(), name='posts'),

]
