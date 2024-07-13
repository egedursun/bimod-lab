
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
        sample_conn = DocumentKnowledgeBaseConnection.objects.first()
        executor = KnowledgeBaseSystemDecoder.get(sample_conn)
        executor.index_documents([
            "apps/datasource_knowledge_base/developers/test.csv",
        ])
        ##################################################
        return context

        """
        "apps/datasource_knowledge_base/developers/test.docx",
        "apps/datasource_knowledge_base/developers/test.html",
        "apps/datasource_knowledge_base/developers/test.ipynb",
        "apps/datasource_knowledge_base/developers/test.json",
        "apps/datasource_knowledge_base/developers/test.md",
        "apps/datasource_knowledge_base/developers/test.odt",
        "apps/datasource_knowledge_base/developers/test.pdf",
        "apps/datasource_knowledge_base/developers/test.pptx",
        "apps/datasource_knowledge_base/developers/test.rtf",
        "apps/datasource_knowledge_base/developers/test.txt",
        "apps/datasource_knowledge_base/developers/test.xls",
        "apps/datasource_knowledge_base/developers/test.xlsx",
        "apps/datasource_knowledge_base/developers/test.xml",
        """
