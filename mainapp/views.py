from django.contrib.auth import (
	authenticate, 
	get_user_model,
	login,
	logout)

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


from .models import User, UserProfile, PropertyEntry, Request, Match
from .tokens import account_activation_token

from .forms import UserLoginForm, UserSignUpForm, PropertyEntryForm, UserAccountForm, RequestEntryForm

from comments.forms import CommentForm
from comments.models import Comment
# Create your views here.


# using choices field:
# userprofile = UserProfile()
# userprofile.user_type = CharityType.BUYER
# userprofile.save()


# Decorators
# login required 



def get_manual_field_add_listing(context, form, form_type):

	property_type = "property_type" 
	no_of_bedrooms = "no_of_bedrooms"
	no_of_bathrooms = "no_of_bathrooms"
	location = "location"
	price = "price"
	dsq = "dsq"
	other_details = "other_details"
	property_number = "property_number"

	first_name = 'first_name'
	last_name = 'last_name'
	email = 'email'
	phone_number = 'phone_number'
	password1 = 'password1'
	password2 = 'password2'

	content = "content"
	

	if form_type == "UserSignUpForm" or form_type == "UserAccountForm":
		

		context["first_name_field"] = form.fields[first_name].get_bound_field(form, first_name)
		context["last_name_field"] = form.fields[last_name].get_bound_field(form, last_name)
		context["email_field"] = form.fields[email].get_bound_field(form, email)
		context["phone_number_field"] = form.fields[phone_number].get_bound_field(form, phone_number)
		try:
			context["password1_field"] = form.fields[password1].get_bound_field(form, password1)
			context["password2_field"] = form.fields[password2].get_bound_field(form, password2)
		except:
			pass

	elif form_type == "PropertyEntryForm":


		context["property_type_field"] = form.fields[property_type].get_bound_field(form, property_type)
		context["no_of_bedrooms_field"] = form.fields[no_of_bedrooms].get_bound_field(form, no_of_bedrooms)
		context["no_of_bathrooms_field"] = form.fields[no_of_bathrooms].get_bound_field(form, no_of_bathrooms)
		context["location_field"] = form.fields[location].get_bound_field(form, location)
		context["price_field"] = form.fields[price].get_bound_field(form, price)
		context["dsq_field"] = form.fields[dsq].get_bound_field(form, dsq)
		context["other_details_field"] = form.fields[other_details].get_bound_field(form, other_details)
		context["property_number_field"] = form.fields[property_number].get_bound_field(form, property_number)
		context["other_details_field"] = form.fields[other_details].get_bound_field(form, other_details)

	elif form_type == "RequestEntryForm":
		context["property_type_field"] = form.fields[property_type].get_bound_field(form, property_type)
		context["no_of_bedrooms_field"] = form.fields[no_of_bedrooms].get_bound_field(form, no_of_bedrooms)
		context["no_of_bathrooms_field"] = form.fields[no_of_bathrooms].get_bound_field(form, no_of_bathrooms)
		context["location_field"] = form.fields[location].get_bound_field(form, location)
		context["price_field"] = form.fields[price].get_bound_field(form, price)
		context["dsq_field"] = form.fields[dsq].get_bound_field(form, dsq)

	elif form_type == "CommentForm":
		context["content_field"] = form.fields[content].get_bound_field(form, content)

	return context


def login_must(f):
	
	def login_inner(*args, **kwargs):
		account_owner = args[0].user
		if not account_owner.is_authenticated:
			raise PermissionDenied
		return f(*args, **kwargs)
	return login_inner

# ======================================================



def activation_sent_view(request, template_name="activation_sent.html"):
	return render(request, template_name)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.userprofile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('mainapp:account')
    else:
        return render(request, 'activation_invalid.html')


def sign_in(request):
	next = request.GET.get("next")
	form = UserLoginForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			user = form.login(request)
			if user:	
				login(request, user)
				if next:
					return redirect(next)
		else:
			return redirect('mainapp:home')
		return redirect('mainapp:account')
	
@login_must
def sign_out(request):
	logout(request)
	return redirect('mainapp:home')


def index(request, template_name="index.html"):
	context = dict()	
	current_url = request.path
	context['current_url'] = current_url

	if current_url == "/sell/" or current_url == "/buy/":
		autoplay = False
	else:
		autoplay = True

	context['autoplay'] = autoplay

	return render(request, template_name, context)

def select_type(request, user_type=None):

	if user_type == "buyer":
		request.session['user_type'] = 'buyer'
	elif user_type == "seller":
		request.session['user_type'] = 'seller'
	else:
		raise Http404
	return redirect('mainapp:register')
	



def register(request, template_name="registration.html"):
	context = dict()
	form = UserSignUpForm(request.POST or None)
	form_type = "UserSignUpForm"
	context = get_manual_field_add_listing(context, form, form_type)
	try:
		user_type = request.session.get("user_type")
		context["user_type"] = user_type
	except:
		raise Http404
	
	
	if request.method  == 'POST':
		form = UserSignUpForm(request.POST)

		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.userprofile.first_name = form.cleaned_data.get('first_name')
			user.userprofile.last_name = form.cleaned_data.get('last_name')
			user.userprofile.email = form.cleaned_data.get('email')
			user.userprofile.user_type = user_type
			# user can't login until link confirmed
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Please Activate Your Account'
			# load a template like get_template() 
			# and calls its render() method immediately.
			message = render_to_string('activation_request.html', {'user': user,
	'domain': current_site.domain,
	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
	# method will generate a hash value with user related data
	'token': account_activation_token.make_token(user),
	})

			to_email = form.cleaned_data.get('email')
			email = EmailMessage(subject, message, to=[to_email])
			email.send()
			return redirect('mainapp:activation_sent')
	# else:
	context["form"] = form

	
	return render(request, template_name, context)




@login_must
def account(request, template_name="account.html"):
	context = dict()
	account_owner = request.user

	
	user_obj = User.objects.get(email=account_owner.email)
	form = UserAccountForm(request.POST or None, instance=user_obj)
	form_type = "UserAccountForm"
	context = get_manual_field_add_listing(context, form, form_type)

	if request.user.userprofile.user_type == "Seller":
		context["entries"] = PropertyEntry.objects.filter(seller=request.user)
		context["entries_count"] = PropertyEntry.objects.filter(seller=request.user).count()
	elif request.user.userprofile.user_type == "Buyer":
		context["entries"] = Request.objects.filter(buyer=request.user)
		context["entries_count"] = Request.objects.filter(buyer=request.user)
		context["matches"] = Match.objects.filter(buyer_request__buyer=request.user)
		context["matches_count"] = Match.objects.filter(buyer_request__buyer=request.user).count

	
	if request.method == "POST":
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data.get('email')
			user.save()
		else:
			print(form.errors)
	
	context["form"] = form
	context["owner"] = account_owner

	

	return render(request, template_name, context)


def add_listing(request, template_name="add-listing.html"):
	context = dict()
	
	if request.user.userprofile.user_type == "Seller":
		form = PropertyEntryForm(request.POST or None)
		form_type = "PropertyEntryForm"
		context = get_manual_field_add_listing(context, form, form_type)
		# context["form"] = seller_form
	elif request.user.userprofile.user_type == "Buyer":
		form = RequestEntryForm(request.POST or None)
		form_type = "RequestEntryForm"
		context = get_manual_field_add_listing(context, form, form_type)
	else:
		raise PermissionDenied()
		
	
	if request.method == "POST":
		if form.is_valid():
			if form_type == "PropertyEntryForm":
				property_entry = form.save(commit=False)
				property_entry.seller = request.user
				property_entry.is_available = True
				property_entry.save()
			elif form_type == "RequestEntryForm":
				request_entry = form.save(commit=False)
				request_entry.buyer = request.user
				request.request_status = "Pending"
				request_entry.save()
			
			return redirect('mainapp:account')
	context["form"] = form
	return render(request, template_name, context)


@login_must
def explore(request, template_name="explore.html"):
	context = dict()	

	if request.user.userprofile.user_type == "Buyer":
		matches_qs = Match.objects.valid_matches()
		matches = matches_qs.filter(buyer_request__buyer=request.user)
		context["entries"] = matches
		
	elif request.user.userprofile.user_type == "Seller":
		properties = PropertyEntry.objects.filter(seller=request.user)
		context["entries"] = properties

	else:
		raise PermissionDenied()



	return render(request, template_name, context)

@login_must
def all_requests(request, template_name="all-requests.html"):

	if request.user.userprofile.user_type == "Buyer":
		context = dict()
		context["all_requests"] = Request.objects.filter(buyer=request.user)
		return render(request, template_name, context)


	elif request.user.userprofile.user_type == "Seller":
		return redirect('mainapp:requests')

@login_must
def remove_request(request, id=None):

	buyer_request = get_object_or_404(Request, id=id)

	buyer_request.request_status = "Inactive"
	buyer_request.is_active = False
	buyer_request.save()

	return redirect('mainapp:all-requests')

@login_must
def activate_request(request, id=None):

	buyer_request = get_object_or_404(Request, id=id)

	buyer_request.is_active = True
	buyer_request.save()

	return redirect('mainapp:all-requests')



@login_must
def unmatched_requests(request, template_name="unmatched-requests.html"):
	context = dict()
	if request.user.userprofile.user_type == "Seller":
		context["unmatched_requests"] = Request.objects.filter(is_active=True).exclude(match__property_entry__seller=request.user)
	elif request.user.userprofile.user_type == "Buyer":
		unmatched_requests = Request.objects.filter(buyer=request.user, is_active=True, request_status="Pending").filter(match__isnull=True)
		context["unmatched_requests"] = unmatched_requests
	else:
		raise PermissionDenied()


	return render(request, template_name, context)


@login_must
def list_inside(request, id=None, template_name="list-inside.html"):

	context = dict()
	property_entry = get_object_or_404(PropertyEntry, id=id)

	context["property"] = property_entry


	comment_form = CommentForm(request.POST or None)
	form_type = "CommentForm"
	context = get_manual_field_add_listing(context, comment_form, form_type)
	
	if request.method == "POST":
		if comment_form.is_valid():
			content = comment_form.cleaned_data.get('content')
			
			new_comment, created = Comment.objects.get_or_create(
				buyer = request.user,
				property_entry = property_entry,
				content = content)
			print(new_comment)
			print(created)
			return HttpResponseRedirect(new_comment.property_entry.get_absolute_url()) 
	context["comments"] = property_entry.comments

	return render(request, template_name, context)


def faqs(request, template_name="faq.html"):

	return render(request, template_name)

def terms(request, template_name="terms.html"):

	return render(request, template_name)

def contact(request, template_name="contact.html"):

	return render(request, template_name)

def pricing(request, template_name="pricing.html"):

	return render(request, template_name)




def listings(request, template_name="listings.html"):

	return render(request, template_name)

def contact(request, template_name="contact.html"):

	return render(request, template_name)

