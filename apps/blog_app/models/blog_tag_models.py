from django.db import models
from slugify import slugify


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
