from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from mainapp.models import PropertyEntry
from mainapp.views import get_manual_field_add_listing
from .forms import ReviewForm
from .models import Review

User = get_user_model()

def add_review(request):
	review_form = ReviewForm(request.POST or None)
	if request.method == "POST":
		if review_form.is_valid():
			property_entry_id = review_form.cleaned_data.get('property_entry_id')
			seller_id = review_form.cleaned_data.get('seller_id')
			seller = User.objects.get(id=seller_id)
			property_entry = PropertyEntry.objects.get(id=property_entry_id)
			content = review_form.cleaned_data.get('content')
			rating = review_form.cleaned_data.get('ratings')

			print(review_form.errors)
		return redirect('mainapp:explore')
	

def set_rating(request):
	data = dict()
	print("seting")
	seller_id = request.GET.get('seller_id')
	rating_value = request.GET.get("rating_value")

	seller = User.objects.get(id=int(seller_id))
	review, created = Review.objects.get_or_create(buyer=request.user,
		seller=seller)
	review.rating = int(rating_value)
	
	review.save() 
	
	return JsonResponse(data)