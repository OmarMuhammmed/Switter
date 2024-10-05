from django import forms
from .models import Post, Comment, ReplyComment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body','image']
        labels = {
            'body': 'What’s on your mind?', 
            'image' : ''
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'What are you thinking about?',  
                'style': 'background-color: #192734; color: white; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box;',  # Dark background and styles
                'rows': 5, 
            }),
            'image': forms.ClearableFileInput(attrs={
                'style': 'display: none;',  
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': '',  
        }
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Your comment .. ',  
                'style': 'background-color: #192734; color: white; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box; margin-top:10px ;',  # Dark background and styles
                'rows': 5, 
            }),
        }

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ['body']
        labels = {
            'body': '',  
        }
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Your reply .. ',  
                'style': 'background-color: #192734; color: white; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box; margin-top:10px ;',  # Dark background and styles
                
            }),
        }
