from django.contrib import admin
from .models import AIAnalysis


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'summary', 'is_latest', 'created_at', 'updated_at')
    list_filter = ('is_latest', 'created_at', 'user')
    search_fields = ('user__email', 'summary', 'analysis_text')
    readonly_fields = ('created_at', 'updated_at')
