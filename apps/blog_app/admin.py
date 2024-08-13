from django.contrib import admin

from .models import BlogPost, BlogSEOMeta, BlogTag


# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'published_at', 'created_at', 'updated_at']
    list_filter = ['status', 'published_at', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(BlogSEOMeta)
class BlogSEOMetaAdmin(admin.ModelAdmin):
    list_display = ['post', 'meta_title', 'meta_description', 'meta_keywords']
    list_filter = ['meta_title', 'meta_description', 'meta_keywords']
    search_fields = ['post']
    ordering = ['post']
