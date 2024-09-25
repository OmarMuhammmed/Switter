from django.urls import path
from .import views

urlpatterns = [

   
    path('',views.HomeView.as_view(), name='home'),
    # path('post/<int:pk>/',views.post_detail_view, name='post_detail'),
    path('post/<int:pk>/',views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment',views.add_comment, name='add_comment'),
    path('post/<int:pk>/reply',views.add_reply, name='add_reply'),
    path('accounts/profile/',views.profile, name='profile'),

]
