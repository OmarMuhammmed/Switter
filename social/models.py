from django.db import models
from django.utils import timezone
from accounts.models import CustomUser as User

class Post(models.Model):
    user = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts', height_field=None, width_field=None, max_length=None , blank=True,null=True)
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    # reaction
    
    def __str__(self):
        return str(self.id)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return str(f"{self.user} : {self.body[:30]}")
   


class ReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_reply = models.ForeignKey('self', null=True, blank=True, related_name='child_replies', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comment, related_name='replies' , on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return str(f"{self.user} parent_comment: {self.parent_comment}: {self.body[:30]}")
    # reaction 
    class Meta:
        ordering = ['created_at']

    def is_child(self):
        return self.parent is not None    
    

class Reaction(models.Model):
    post = models.ForeignKey(Post, related_name='reaction', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  
    def __str__(self):
        return f"{self.user.username} loved {self.post.body[:30]}"    