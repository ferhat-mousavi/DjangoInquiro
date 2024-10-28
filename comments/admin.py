from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'question', 'answer', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
