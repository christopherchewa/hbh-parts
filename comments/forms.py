from django import forms
from .models import Comment

class CommentForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add Your Comment'}), max_length=255, required=True)
