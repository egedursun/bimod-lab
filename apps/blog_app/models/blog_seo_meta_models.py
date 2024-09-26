from django.db import models


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
