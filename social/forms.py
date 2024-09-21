from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body': 'What’s on your mind?',  
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'What are you thinking about?',  
                'style': 'background-color: #192734; color: white; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box;',  # Dark background and styles
                'rows': 5, 
            }),
        }
