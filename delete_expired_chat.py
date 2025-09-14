from django.core.management.base import BaseCommand
from django.utils import timezone
from newsApp.models import ChatHistory
from datetime import timedelta

class Command(BaseCommand):
    help = "Delete chat history older than 5 minutes"

    def handle(self, *args, **options):
        expired_chats = ChatHistory.objects.filter(
            created_at__lt=timezone.now() - timedelta(minutes=5)
        )
        count = expired_chats.count()
        expired_chats.delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {count} expired chat messages."))
