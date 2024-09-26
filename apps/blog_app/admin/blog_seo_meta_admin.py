from django.contrib import admin

from apps.blog_app.models import BlogSEOMeta


@admin.register(BlogSEOMeta)
class BlogSEOMetaAdmin(admin.ModelAdmin):
    list_display = ['post', 'meta_title', 'meta_description', 'meta_keywords']
    list_filter = ['meta_title', 'meta_description', 'meta_keywords']
    search_fields = ['post']
    ordering = ['post']
