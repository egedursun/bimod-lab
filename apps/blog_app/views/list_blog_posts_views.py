from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
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
