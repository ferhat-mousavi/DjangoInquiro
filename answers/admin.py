from django.contrib import admin
from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'question', 'score', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
