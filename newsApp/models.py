from django.db import models

class News(models.Model):
    NEWS_TYPE_CHOICES = [
        ('world', 'World News'),
        ('local', 'Local News'),
    ]

    heading = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=100, default='news_hub_author')
    file = models.FileField(upload_to='newsFiles/', blank=True, null=True)

    news_type = models.CharField(
        max_length=10,
        choices=NEWS_TYPE_CHOICES,
        default='world',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

from django.db import models

class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

from django.db import models
from django.utils import timezone
from datetime import timedelta

class ChatHistory(models.Model):
    user_message = models.TextField()
    ai_response = models.TextField()
    category = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Check if the message is older than 30 minutes"""
        return timezone.now() > self.created_at + timedelta(minutes=30)

    def __str__(self):
        return f"{self.user_message[:50]}..."
