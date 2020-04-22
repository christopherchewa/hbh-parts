from django.db import models
from mainapp.models import PropertyEntry, User

# Create your models here.
class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	class Meta:
		abstract = True


class Comment(BaseModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	property_entry = models.ForeignKey(PropertyEntry, on_delete=models.CASCADE)
	content = models.TextField(null=False, blank=False, max_length=255)

	def get_comment(self):
		retstr = str(self.content)[:15] + "..."
		return retstr

	# def __str__(self):
	# 	return self.buyer


class Review(BaseModel):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
	content = models.TextField(null=False, blank=False, max_length=255)
	rating = models.PositiveIntegerField(default=1)

	class Meta:
		unique_together = ['buyer', 'seller']

	def __str__(self):
		retstr = "Review by :" + str(self.buyer) + " on " + str(self.seller)
		return retstr