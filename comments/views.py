from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
# Create your views here.
from mainapp.models import PropertyEntry
from mainapp.views import get_manual_field_add_listing
from .forms import ReviewForm
from .models import Comment, Review

User = get_user_model()




@login_required
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
	


@login_required
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


@login_required
def property_comments(request, id=None, template_name="property-comments.html"):
	context = dict()

	property_entry = get_object_or_404(PropertyEntry, id=id)
	comments_qs = Comment.objects.filter(property_entry=property_entry)
	context["property"] = property_entry
	context["comments"] = comments_qs

	return render(request, template_name, context)


@login_required
def seller_reviews(request, id=None, template_name="user-reviews.html"):
	context = dict()
	property_entry = get_object_or_404(PropertyEntry, id=id)
	seller = get_object_or_404(User, id=property_entry.seller.id)

	seller_reviews_qs = Review.objects.filter(seller=seller, content__isnull=False)
	context["property"] = property_entry
	context["seller_reviews"] = seller_reviews_qs



	return render(request, template_name, context)