from django.db import models
from django.conf import settings


class ChatbotAnalysis(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatbot_analyses'
    )
    session_id = models.CharField(max_length=100, default='default')
    analysis_text = models.TextField()
    summary = models.CharField(max_length=255)
    market_data_snapshot = models.JSONField(null=True, blank=True)
    is_latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_latest']),
        ]

    def __str__(self):
        return f'Analysis {self.pk} for {self.user.email} - {self.summary}'


class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatbot_messages'
    )
    session_id = models.CharField(max_length=100, default='default')
    message_text = models.TextField()
    is_from_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = 'Bot' if self.is_from_bot else 'User'
        return f'{sender}: {self.message_text[:30]}'

