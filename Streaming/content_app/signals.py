from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_student_group_and_profile(sender, instance, created, **kwargs):
    """Ensures every new user has the Estudante group and a profile."""
    if created:
        if not instance.is_superuser:
            group, _ = Group.objects.get_or_create(name="Estudante")
            instance.groups.add(group)
        UserProfile.objects.get_or_create(user=instance)