from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserMembership
from .views import get_phone_number

@receiver(post_save, sender=User)
def create_usermembership(sender, instance, created, **kwargs):
    if created:
        UserMembership.objects.create(user=instance, phone_number = get_phone_number())

@receiver(post_save, sender=User)
def save_usermembership(sender, instance, **kwargs):
    instance.usermembership.save()