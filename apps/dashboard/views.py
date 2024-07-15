
from django.views.generic import TemplateView

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from web_project import TemplateLayout


class DashboardMainView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        ##################################################
        # TEST ZONE
        ##################################################
        # ...
        ##################################################
        return context
