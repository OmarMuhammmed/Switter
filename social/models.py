from django.db import models
from django.utils import timezone
from accounts.models import CustomUser as User

class Post(models.Model):
    user = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/posts', height_field=None, width_field=None, max_length=None , blank=True,null=True)
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    # reaction

    def __str__(self):
        return str(self.id)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return str(f"{self.user}-{self.id}")
    # reaction 