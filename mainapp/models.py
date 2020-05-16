from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from phone_field import PhoneField
from modelchoices import Choices

import uuid
# Create your models here.






# value for the database and a user readable value, which could also be translation object
class UserType(Choices):
	BUYER = ('Buyer', 'Buyer')
	SELLER = ('Seller', 'Seller')

class PropertyType(Choices):
	APARTMENT = ('Apartment', 'Flat/Apartment') 
	MANSION = ('Mansion', 'Town House/Mansionnette',)
	BUNGALOW = ('Bungalow', 'Bungalow')

class HouseRequestStatus(Choices):
	PENDING = ('Pending', 'Pending')
	MATCHED = ('Matched', 'Matched')
	DECLINED = ('Declined', 'Declined')
	ARCHIVED = ('Archived', 'Archived')

class EngagementStatus(Choices):
	PENDING = ('Pending', 'Pending')
	ACCEPTED = ('Accepted', 'Accepted')
	DECLINED = ('Declined', 'Declined')
	COMPLETED = ('Completed', 'Completed')
	ARCHIVED = ('Archived', 'Archived')



class UserManager(BaseUserManager):

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError("The email must be set")

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)


	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('SuperUser must have is_staff=True')

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('SuperUser must have is_superuser=True')

		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	phone_number = models.CharField(blank=True, null=True, max_length=20, help_text='Phone Number')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


	objects = UserManager()


	@property
	def get_full_names(self):
		first_name = self.first_name
		last_name = self.last_name
		full_names = "{} {}".format(first_name, last_name)
		return full_names

	def clean_email(self):

		email = self.cleaned_data.get(email)
		email_exists = True
		try:
			email = User.objects.get(email=email)
		except:
			email_exists = False

		if email_exists:
			raise forms.ValidationError("Email Already Exists")

		return email

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(blank=True, null=True)
	# phone_number = PhoneField(blank=False, null=False, help_text='Phone Number')
	user_type = models.CharField(max_length=6, choices=UserType.CHOICES)
	signup_confirmation = models.BooleanField(default=False)


	def __str__(self):
		retstr = str(self.user.email) + " - " + str(self.user_type)
		return retstr


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class BaseDateModel(models.Model):
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	class Meta:
		abstract = True


class BasePropertyDetailModel(BaseDateModel):
	property_type = models.CharField(max_length=20, choices=PropertyType.CHOICES, null=True, blank=True)
	no_of_bedrooms = models.PositiveIntegerField(default=1, null=False, blank=False)
	no_of_bathrooms = models.PositiveIntegerField(default=1, null=False, blank=False)
	location = models.CharField(max_length=255, null=True, blank=True)
	price = models.PositiveIntegerField(default=1000, null=False, blank=False)
	dsq = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		abstract = True

class PropertyEntryManager(models.Manager):
	def available(self, *args, **kwargs):
		return super(PropertyEntryManager, self).filter(is_available=True)


class PropertyEntry(BasePropertyDetailModel):
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	property_title = models.CharField(max_length=50, blank=True, null=True)
	is_available = models.BooleanField(default=True, null=False, blank=False)
	other_details = models.TextField(blank=True, null=True)
	favourites = models.ManyToManyField(User, related_name='favourites', blank=True)

	objects = PropertyEntryManager()
	
	class Meta:
		verbose_name_plural = "Property Entries"
		ordering = ['-created_at']
	
	def __str__(self):
		return "{}-{}".format(self.seller.get_full_names, self.location)


	def get_absolute_url(self):
		return reverse('mainapp:list-inside', kwargs={'id':self.id})

	def get_absolute_edit_url(self):
		return reverse('mainapp:edit-listing', kwargs={'id':self.id})


	def get_absolute_url_allprops(self):
		return reverse('mainapp:all-properties-inside', kwargs={'id':self.id})

	def get_comments_absolute_url(self):
		return reverse('comments:property-comments', kwargs={'id':self.id})

	def get_seller_reviews_absolute_url(self):
		return reverse('comments:seller-reviews', kwargs={'id':self.id})



	@property
	def kshs_price(self):
		from .utils import kshs_formatter
		price = kshs_formatter(self.price)
		return price

	@property
	def comments(self):
		property_entry = self
		from comments.models import Comment
		qs = Comment.objects.filter(property_entry=property_entry)
		return qs


	@property
	def total_favourites(self):
		return self.favourites.count()

	# @property
	def is_favourite(self, request):
		user = request.user
		if self.favourites.filter(id=user.id).exists():
			is_favourite_property = True
		else:
			is_favourite_property = False

		return is_favourite_property

	@property
	def property_valid_match_count(self):		
		match_count = Match.objects.valid_matches().filter(property_entry=self).count()
		return match_count

	@property
	def property_valid_matches(self):
		property_matches = Match.objects.valid_matches().filter(property_entry=self)
		return property_matches


	def save(self, *args, **kwargs):
		#automatically generate plot title
		no_of_bedrooms = self.no_of_bedrooms
		property_type = self.property_type
		location = self.location
		property_title_str = "{} BR {} in {}".format(no_of_bedrooms, property_type, location)
		self.property_title = property_title_str
		super(PropertyEntry, self).save(*args, **kwargs)


def upload_location(instance, filename):
    
    PropertyEntryImageModel = instance.__class__
    sellernames = "{}{}".format(instance.property_entry.seller.first_name, instance.property_entry.seller.last_name)
    location_str = instance.property_entry.location
    location = location_str.replace(" ", "")
    return "%s/%s/%s" %(sellernames, location, filename)

class PropertyEntryImage(models.Model):
	property_entry = models.OneToOneField(PropertyEntry, on_delete=models.CASCADE)
	image1 = models.ImageField(blank=True, null=True, upload_to=upload_location)
	image2 = models.ImageField(blank=True, null=True, upload_to=upload_location)
	image3 = models.ImageField(blank=True, null=True, upload_to=upload_location)
	image4 = models.ImageField(blank=True, null=True, upload_to=upload_location)
	image5 = models.ImageField(blank=True, null=True, upload_to=upload_location)

	def __str__(self):
		return "{} images".format(self.property_entry)
	
	class Meta:
		verbose_name_plural = "Property Entry Images"


class RequestManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(RequestManager, self).filter(is_active=True)


class Request(BasePropertyDetailModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	request_status = models.CharField(max_length=20, choices=HouseRequestStatus.CHOICES, default=HouseRequestStatus.PENDING, blank=False, null=False)
	
	class Meta:
		ordering = ['-created_at']

	objects = RequestManager()

	def __str__(self):
		retstr = str(self.pk) + "-" + str(self.buyer) + "-" + str(self.location)
		return retstr

	@property
	def kshs_price(self):
		from .utils import kshs_formatter
		price = kshs_formatter(self.price)
		return price

	@property
	def buyer_valid_match_count(self):		
		match_count = Match.objects.valid_matches().filter(buyer_request=self).count()
		return match_count

	


class MatchManager(models.Manager):
	def valid_matches(self, *args, **kwargs):
		return super(MatchManager, self).filter(is_valid=True)

	def invalid_matches(self, *args, **kwargs):
		return super(MatchManager, self).filter(is_valid=False)


class Match(BaseDateModel):
	buyer_request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
	property_entry = models.ForeignKey(PropertyEntry, on_delete=models.CASCADE, null=True)
	is_valid = models.BooleanField(default=True)
	engagement_status = models.CharField(max_length=20, choices=EngagementStatus.CHOICES, default=EngagementStatus.PENDING, blank=False, null=False)
	engagement_date = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
	is_paid = models.BooleanField(default=False)

	
	objects = MatchManager()

	class Meta:
		ordering = ['-updated_at']
		# unique_together = ['buyer_request', 'property_entry']

	def __str__(self):
		return str(self.buyer_request)




def update_matches_seller(sender, instance, created, **kwargs):
	if created:
		for r in Request.objects.all():
			if r.location == instance.location and r.price == instance.price:
				#only creates a match if property(instance) location matches request location
				m = Match.objects.create(buyer_request=r, property_entry=instance)
				
				if r.request_status == "Pending":
					r.request_status = "Matched"
					r.save()
				if not m.property_entry.is_available or not m.buyer_request.is_active:
					m.is_valid = False
				else:
					m.is_valid = True

				m.save()
				

			


	if not created:
		print("sjdhsjd")
		try:
			
			ms = Match.objects.filter(property_entry=instance)
			# ms = ms_qs.filter(Q(engagement_status="Pending") | Q(engagement_status="Accepted"))
			for m in ms:
				print(m)
				print("location:{}".format(m.buyer_request.location))
				print("location:{}".format(instance.location))
				
				#if either the request or property is inactive, the match is invalid
				#and vice versa
				if instance.is_available and m.buyer_request.is_active:
					m.is_valid = True
				else:
					m.is_valid = False
				m.save()

				
				if m.buyer_request.location == instance.location:
					if m.engagement_status == "Pending" or m.engagement_status == "Accepted" or m.engagement_status == "Declined":
						
						if m.buyer_request.price != instance.price:
							if m.buyer_request.request_status == "Matched":
								m.buyer_request.request_status = "Pending"
								m.buyer_request.save()
							
							m.delete()
					
						
		except:
			pass

		for r in Request.objects.filter(location=instance.location, price=instance.price, is_active=True):	
			print("request:{}".format(r.request_status))
			if r.request_status == "Pending":
				r.request_status = "Matched"
				r.save()
			m = Match.objects.get_or_create(buyer_request=r, property_entry=instance, is_valid=True)
			
		



		

post_save.connect(update_matches_seller, sender=PropertyEntry)


def update_matches_buyer(sender, instance, created, **kwargs):
	if created:
		for p in PropertyEntry.objects.all():
			if p.location == instance.location and p.price == instance.price:
				m = Match.objects.create(buyer_request=instance, property_entry=p)
				instance.is_active = True
				if instance.request_status == "Pending":
					instance.request_status = "Matched"
					instance.save()
				if not m.property_entry.is_available or not m.buyer_request.is_active:
					m.is_valid = False
				else:
					m.is_valid = True
				m.save()
	if not created:
		try:
			ms = Match.objects.filter(buyer_request=instance)
			for m in ms:
				if instance.is_active and m.property_entry.is_available:
					m.is_valid = True
				else:
					m.is_valid = False
				m.save()
		except:
			pass

post_save.connect(update_matches_buyer, sender=Request)


