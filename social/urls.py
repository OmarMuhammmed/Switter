from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/',views.post_detail, name='post_detail'),
    path('post/update/<int:pk>/',views.post_update, name='post_update'),
    path('post/<int:pk>/delete/',views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/',views.add_comment, name='add_comment'),
    path('post/<int:pk>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/reply/',views.add_reply, name='add_reply'),
    path('post/<int:pk>/react/',views.manage_reatcions, name='manage_reatcions'),
    path('post/<int:pk>/share/',views.share_post, name='share_post'),
    path('accounts/profile/<slug:slug>/',views.profile, name='profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
