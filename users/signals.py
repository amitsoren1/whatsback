from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User, Profile, Contact

# @receiver(pre_save, sender=Contact)
# def after(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile.objects.filter(owner__phone=instance.phone).first()
#         if profile:
#             instance.profile = profile
#             instance.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
