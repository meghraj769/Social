from cProfile import Profile
from django import forms
from .models import *

class PostForm(forms.ModelForm):

    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Say something...',
        })
    )

    class Meta:
        model = Post
        fields = ['body']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['followers']
        
class CommentForm(forms.ModelForm):

    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Add your opinion!',
        })
    )

    class Meta:
        model = Comment
        fields = ['comment']
        