from django.contrib import admin

from apps.blog_app.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'published_at', 'created_at', 'updated_at']
    list_filter = ['status', 'published_at', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
