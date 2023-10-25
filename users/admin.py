from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'created_at']
	ordering = ['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_at']
    ordering = ['-created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp']
    ordering = ['-timestamp']