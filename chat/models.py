from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model): # room contains 2 or more users
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at   =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"
    

class Message(models.Model):
    conversation = models.ForeignKey(
                                    Conversation, 
                                    related_name='messages', 
                                    on_delete=models.CASCADE
                                    )
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.content[:20]} from {self.sender}"
    