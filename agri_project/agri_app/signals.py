from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Farmer

@receiver(post_save, sender=Farmer)
def assign_default_privileges(sender, instance, created, **kwargs):
    # Only run this if the user was just created
    if created:
        # Check if they provided essential info
        if instance.farm_name and instance.phone_number:
            group, _ = Group.objects.get_or_create(name='Verified Farmer')
            instance.groups.add(group)
        else:
            # Maybe assign to a 'Pending' group with limited access
            group, _ = Group.objects.get_or_create(name='Unverified User')
            instance.groups.add(group)