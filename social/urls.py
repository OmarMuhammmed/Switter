from django.urls import path
from .import views

urlpatterns = [

   
    path('',views.PostsView.as_view(), name='posts'),
    path('post/<int:pk>/',views.PostDetailView.as_view(), name='post_detail'),
    path('accounts/profile/',views.profile, name='profile'),

]
