from django.urls import path
from . import views  


urlpatterns = [
     path('login_redirect/', views.login_redirect, name='login_redirect'),
]