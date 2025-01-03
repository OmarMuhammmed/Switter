from django.urls import path
from . import views



urlpatterns = [
    path('', views.users_chat_list, name='users_chat_list'),
    path('chat_room/<int:user_id>/', views.chat_room, name='chat_room'),
]    