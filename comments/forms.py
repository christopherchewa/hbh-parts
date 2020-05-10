from django import forms
from .models import Comment

class CommentForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Leave a Comment'}), max_length=255, required=True)

	def clean_content(self):
		content = self.cleaned_data.get("content")
		if content is None:
			raise forms.ValidationError("Comment Cannot be Empty!")
		return self.content

class ReviewForm(forms.Form):
	seller_id = forms.IntegerField()
	property_entry_id = forms.IntegerField()
	review_content = forms.CharField(max_length=255, required=True)
	# ratings = forms.IntegerField(required=False)
