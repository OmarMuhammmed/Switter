from allauth.account.forms import SignupForm
from django import forms
from . models import Profile
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)
        labels = {
            'bio': '',  
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Add Your Bio .. ',  
                'style': 'background-color: #192734; color: white; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box; margin-top:10px ;',  # Dark background and styles
                'rows': 5, 
            }),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image",)
   
