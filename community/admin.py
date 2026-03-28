from django.contrib import admin
from .models import Tag, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['pets']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'pet', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'pet__name', 'text']
