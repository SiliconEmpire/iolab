from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Subscription(models.Model):
	subscription_types = models.CharField(max_length=120)
	subscription_price = models.IntegerField(default = 0)
	duration = models.IntegerField(default = 0)

	def __str__(self):
		return self.subscription_types

class UserMembership(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=14)
	subscription_type = models.ForeignKey(Subscription, blank=True, null=True, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	subscription_date = models.DateTimeField(default = timezone.now)
	exp_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return f'{self.user.username} Profile'