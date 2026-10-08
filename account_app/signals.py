from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""       
User créé
post_save est déclenché
created == True
Profile.objects.create(...)
Profile créé automatiquement
"""
