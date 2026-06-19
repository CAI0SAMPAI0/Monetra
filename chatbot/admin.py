from django.contrib import admin
from .models import ChatbotAnalysis, ChatMessage


@admin.register(ChatbotAnalysis)
class ChatbotAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'summary', 'is_latest', 'created_at', 'updated_at')
    list_filter = ('is_latest', 'created_at', 'user')
    search_fields = ('user__email', 'summary', 'analysis_text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_text', 'is_from_bot', 'created_at')
    list_filter = ('is_from_bot', 'created_at', 'user')
    search_fields = ('user__email', 'message_text')
    readonly_fields = ('created_at',)
