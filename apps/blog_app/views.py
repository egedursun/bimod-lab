"""
This module defines the views for the blog application, including list and detail views for blog posts.

Views:
    - BlogPostListView: Displays a paginated list of blog posts with optional search functionality.
    - BlogPostDetailView: Displays the details of a specific blog post, including related posts based on tags.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.blog_app.models import BlogPost
from web_project import TemplateLayout


class BlogPostListView(LoginRequiredMixin, TemplateView):
    """
    Displays a paginated list of blog posts with optional search functionality.

    The view supports searching blog posts by title, content, or tags. If a search query is provided,
    the results are filtered based on the query. Otherwise, all published posts are displayed.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        search_query = self.request.GET.get('search', '')

        if search_query:
            posts = BlogPost.objects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query),
            ).order_by('-published_at')
        else:
            posts = BlogPost.objects.filter(status='published').order_by('-published_at')

        paginator = Paginator(posts, 9)  # 9 posts per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context


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
