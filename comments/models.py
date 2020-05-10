from django.db import models
from django.urls import reverse



from mainapp.models import PropertyEntry, User

import math

# Create your models here.
class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	class Meta:
		abstract = True


class Comment(BaseModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	property_entry = models.ForeignKey(PropertyEntry, on_delete=models.CASCADE)
	content = models.TextField(null=True, blank=True, max_length=255)

	# def get_comment_short(self):
	# 	retstr = str(self.content)[:15] + "..."
	# 	return retstr


		


class Review(BaseModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
	content = models.TextField(null=True, blank=True, max_length=255)
	rating = models.PositiveIntegerField(default=1)

	class Meta:
		unique_together = ['buyer', 'seller']
	
	@property
	def average_rating(self):
		total_count = 0
		reviews_qs = Review.objects.filter(seller=self.seller)
		for review in reviews_qs:
			total_count += review.rating
		total_count = total_count / reviews_qs.count()

		return math.ceil(total_count)

