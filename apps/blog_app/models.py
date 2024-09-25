"""
This module defines the data models for the blog application, including models for blog posts, tags, and SEO metadata.

Models:
    - BlogPost: Represents a blog post with attributes like title, slug, content, thumbnail image, and associated tags.
    - BlogTag: Represents a tag associated with blog posts.
    - BlogSEOMeta: Represents SEO metadata for a blog post, including meta title, description, and keywords.
"""

from django.db import models
from django.utils import timezone
from slugify import slugify

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class BlogPost(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the blog post.
        slug (str): The URL-friendly version of the blog post title.
        author (ForeignKey): The author of the blog post, linked to the auth.User model.
        content (str): The content of the blog post.
        thumbnail_image (ImageField): An optional image representing the blog post.
        created_at (datetime): The timestamp when the blog post was created.
        updated_at (datetime): The timestamp when the blog post was last updated.
        published_at (datetime): The timestamp when the blog post was published.
        status (str): The publication status of the blog post (draft or published).
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    thumbnail_image = models.ImageField(upload_to='blog_post_images/%Y/%m/%d/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + ' by ' + self.author.username if self.author else 'admin'

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['title', 'slug']),
            models.Index(fields=['title', 'status']),
            models.Index(fields=['title', 'status', 'published_at']),
            models.Index(fields=['title', 'status', 'created_at']),
            models.Index(fields=['title', 'status', 'updated_at']),
            models.Index(fields=['title', 'status', 'published_at', 'created_at']),
            models.Index(fields=['title', 'status', 'published_at', 'updated_at']),
            models.Index(fields=['title', 'status', 'created_at', 'updated_at']),
            models.Index(fields=['title', 'status', 'created_at', 'published_at']),
            models.Index(fields=['title', 'status', 'updated_at', 'published_at']),
        ]


class BlogTag(models.Model):
    """
    Represents a tag associated with blog posts.

    Attributes:
        name (str): The name of the tag.
        slug (str): The URL-friendly version of the tag name.
        created_at (datetime): The timestamp when the tag was created.
        updated_at (datetime): The timestamp when the tag was last updated.
    """
    blog_posts = models.ManyToManyField('BlogPost', related_name='tags', blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


class BlogSEOMeta(models.Model):
    """
    Represents SEO metadata for a blog post.

    Attributes:
        post (OneToOneField): The blog post associated with this SEO metadata.
        meta_title (str): The meta title for the blog post, used for SEO purposes.
        meta_description (str): The meta description for the blog post, used for SEO purposes.
        meta_keywords (str): The meta keywords for the blog post, used for SEO purposes.
    """

    post = models.OneToOneField("BlogPost", on_delete=models.CASCADE, related_name='seo_meta')
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.CharField(max_length=1000, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'SEO Meta for {self.post.title}'

    class Meta:
        verbose_name = 'Blog SEO Meta'
        verbose_name_plural = 'Blog SEO Meta'
        ordering = ['post']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['meta_title']),
            models.Index(fields=['meta_description']),
            models.Index(fields=['meta_keywords']),
            models.Index(fields=['post', 'meta_title']),
            models.Index(fields=['post', 'meta_description']),
            models.Index(fields=['post', 'meta_keywords']),
        ]
