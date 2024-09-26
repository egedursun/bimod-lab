from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.blog_app.models import BlogPost
from web_project import TemplateLayout


class BlogPostDetailView(LoginRequiredMixin, TemplateView):
    """
    Displays the details of a specific blog post.

    The view fetches a blog post based on its slug and displays its content.
    Additionally, it retrieves and displays a list of related posts based on shared tags.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(BlogPost, slug=post_slug, status='published')
        context['post'] = post

        # Fetch SEO metadata if available
        if hasattr(post, 'seo_meta'):
            context['seo_meta'] = post.seo_meta

        # for related posts, get posts with the same tags
        related_posts = BlogPost.objects.filter(tags__in=post.tags.all()).exclude(id=post.id).distinct()[:3]
        context['related_posts'] = related_posts
        return context
