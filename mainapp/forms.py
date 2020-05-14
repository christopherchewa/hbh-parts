from django import forms
from django.contrib.auth import (
	authenticate, 
	get_user_model,
	login,
	logout)
from django.contrib.auth.forms import UserCreationForm
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column

from .models import User, PropertyEntry, PropertyEntryImage, PropertyType, Request

class UserLoginForm(forms.Form):

	# def __init__(self, *args, **kwargs):
	# 	super(UserLoginForm, self).__init__(*args, **kwargs)

	# 	for field_name in self.fields:
	# 		field = self.fields.get(field_name)
	# 		field_name_new = field_name[0].upper()+field_name[1:]
	# 		field.widget.attrs['placeholder'] = field_name_new
	# 		field.label = ''
	# 		field_class = "form-control"

	# email = forms.EmailField(max_length=255, required=True)
	email = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': "form-control"}), )
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), max_length=255, required=True)
	# password = forms.CharField(max_length=255, required=True)

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get("email")

		password = self.cleaned_data.get("password")
		user = authenticate(username=email, password=password)
		print(self.cleaned_data)
		

		if not user or not user.is_active:
			raise forms.ValidationError("Sorry. Invalid Credentials, Try Again")
		return self.cleaned_data

	def login(self, request):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		user = authenticate(username=email, password=password)
		return user


class UserSignUpForm(UserCreationForm):

			
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), max_length=255, required=False)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), max_length=255, required=False)
	
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
	
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError("Passwords Must Match")

		return password1

	def clean_email(self):
		email = self.cleaned_data.get('email')

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("The Email Entered Has Already Been Registered")

		return email


CHOICES = (
('Apartment', 'Flat/Apartment'),
('Mansion', 'Town House/Mansionnette'),
('Bungalow', 'Bungalow'),
)

class PropertyEntryForm(forms.ModelForm):
	# property_number = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	location = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	property_type = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=CHOICES)
	price = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	no_of_bedrooms = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'min':"1"}), required=True)
	no_of_bathrooms = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'min':"1"}), required=True)
	dsq = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'id':"materialChecked6"}), required=False)
	other_details = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), max_length=255, required=False)

	class Meta:
		model = PropertyEntry
		exclude = ('created_at', 'updated_at', 'seller', 'property_title', 'favourites', 'is_available')


	def __init__(self, data, **kwargs):
		initial = kwargs.get('initial', {})
		super().__init__(data, **kwargs)
		print(initial)
		try:
			self.initial['location']
			self.fields["location"].widget.attrs["readonly"]=True
		except:
			pass
			

class PropertyEntryImagesForm(forms.ModelForm):

	class Meta:
		model = PropertyEntryImage
		fields = ('image1','image2','image3','image4','image5')

class RequestEntryForm(forms.ModelForm):
	location = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	property_type = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=CHOICES)
	price = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	no_of_bedrooms = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'min':"1"}), required=True)
	no_of_bathrooms = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'min':"1"}), required=True)
	dsq = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'id':"materialChecked6"}), required=False)

	class Meta:
		model = Request
		exclude = ('created_at', 'updated_at', 'buyer', 'request_status', 'is_active')

	

class UserAccountForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	# password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), max_length=255, required=False)
	# password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), max_length=255, required=False)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'phone_number')
			# , 'password1', 'password2')

	

	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			user_obj = User.objects.get(email=email)
			if email != self.initial["email"]:
				raise forms.ValidationError("This User Already Exists")
		except:
			user_obj = None
		return email


		

		
