import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        instance.save()
