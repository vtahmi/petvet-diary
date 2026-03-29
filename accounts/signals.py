from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'owner':
            group, _ = Group.objects.get_or_create(name='Pet Owners')
            instance.groups.add(group)
        elif instance.user_type == 'vet':
            group, _ = Group.objects.get_or_create(name='Veterinarians')
            instance.groups.add(group)