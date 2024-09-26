from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.community_forum.models import ForumCategory
from web_project import TemplateLayout


class ForumCategoryListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of forum categories with support for pagination.
    """

    def get_context_data(self, **kwargs):
        """
        Retrieves and returns the context data for rendering the template.

        Returns:
            dict: Context data containing the paginated categories.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')

        # Filter categories based on the search query
        if search_query:
            categories = ForumCategory.objects.filter(threads__title__icontains=search_query).order_by("created_at")
        else:
            categories = ForumCategory.objects.all().order_by("created_at")

        # Paginate categories, 20 per page
        paginator = Paginator(categories, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['categories'] = page_obj
        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context
