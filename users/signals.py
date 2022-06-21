from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users


@receiver(post_save, sender=Users)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        user_token = Token.objects.create(user=instance)
        user_token.save()
