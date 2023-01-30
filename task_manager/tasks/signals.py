from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Project

User = get_user_model()


@receiver(post_save, sender=Project)
def create_token(sender, instance, created, **kwargs):
    if created:
        user = instance.owner

        instance.users.add(user)
