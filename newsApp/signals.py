from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatHistory

@receiver(post_save, sender=ChatHistory)
def handle_chat_saved(sender, instance, created, **kwargs):
    if created:
        print("✅ New chat saved:", instance.user, "->", instance.ai)
