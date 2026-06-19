from django.db import models
from django.conf import settings


class AIAnalysis(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_analyses'
    )
    analysis_text = models.TextField()
    summary = models.CharField(max_length=255)
    is_latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_latest']),
        ]

    def __str__(self):
        return f'AI Analysis {self.pk} for {self.user.email} - {self.summary}'
