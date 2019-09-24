from django import forms
from .models import Comment
from django.contrib import messages


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']


