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

class EngagementStatus(Choices):
	PENDING = ('Pending', 'Pending')
	ACCEPTED = ('Accepted', 'Accepted')
	DECLINED = ('Declined', 'Declined')






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
	phone_number = PhoneField(blank=True, null=True, help_text='Phone Number')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


	objects = UserManager()


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
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
	property_title = models.CharField(max_length=10, blank=True, null=True)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	is_available = models.BooleanField(default=True, null=False, blank=False)
	other_details = models.TextField(blank=True, null=True)
	
	objects = PropertyEntryManager()
	
	class Meta:
		verbose_name_plural = "Property Entries"



	def get_absolute_url(self):
		return reverse('mainapp:list-inside', kwargs={'id':self.id})


	@property
	def comments(self):
		property_entry = self
		from comments.models import Comment
		qs = Comment.objects.filter(property_entry=property_entry)
		return qs

	def __str__(self):
		retstr = str(self.pk) + "-" + str(self.seller) + "-" + str(self.location)
		return retstr

	def save(self, *args, **kwargs):
		#automatically generate plot number
		no_of_bedrooms = self.no_of_bedrooms
		property_type = self.property_type
		location = self.location
		property_title_str = "{} BR {} in {}".format(no_of_bedrooms, property_type, location)
		self.property_title = property_title_str
		super(PropertyEntry, self).save(*args, **kwargs)






class PropertyEntryImage(models.Model):
	property_entry = models.OneToOneField(PropertyEntry, on_delete=models.CASCADE)
	image1 = models.ImageField(blank=True, null=True)
	image2 = models.ImageField(blank=True, null=True)
	image3 = models.ImageField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "Property Entry Images"


class RequestManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(RequestManager, self).filter(is_active=True)


class Request(BasePropertyDetailModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	request_status = models.CharField(max_length=20, choices=HouseRequestStatus.CHOICES, default=HouseRequestStatus.PENDING)
	

	objects = RequestManager()

	def __str__(self):
		retstr = str(self.pk) + "-" + str(self.buyer) + "-" + str(self.location)
		return retstr

	@property
	def valid_match_count(self):		
		match_count = Match.objects.filter(buyer_request=self, is_valid=True).count()
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

	def __str__(self):
		return str(self.buyer_request)



def update_matches_seller(sender, instance, created, **kwargs):
	if created:
		for r in Request.objects.all():
			if r.location == instance.location:
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

	else:
		try:
			ms = Match.objects.filter(property_entry=instance)
			for m in ms:
				#if either the request or property is inactive, the match is invalid
				#and vice versa
				if instance.is_available and m.buyer_request:
					m.is_valid = True
				else:
					m.is_valid = False
				m.save()
		except:
			pass
		

post_save.connect(update_matches_seller, sender=PropertyEntry)


def update_matches_buyer(sender, instance, created, **kwargs):
	if created:
		for p in PropertyEntry.objects.all():
			if p.location == instance.location:
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
	else:
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



class Favourite(BaseDateModel):
	buyer = models.OneToOneField(User, on_delete=models.CASCADE)
	property_entries = models.ManyToManyField(PropertyEntry)

	def get_favourites(self):
		return "\n".join([str(p) for p in self.property_entry.all()])

	def __str__(self):
		return str(self.buyer)