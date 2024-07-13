from django.urls import path

from apps.datasource_knowledge_base.views import DocumentKnowledgeBaseCreateView, DocumentKnowledgeBaseListView, \
    DocumentKnowledgeBaseUpdateView, DocumentKnowledgeBaseDeleteView

app_name = "datasource_knowledge_base"


urlpatterns = [
    path("create/", DocumentKnowledgeBaseCreateView.as_view(
        template_name="datasource_knowledge_base/base/create_knowledge_base.html"
    ), name="create"),
    path("list/", DocumentKnowledgeBaseListView.as_view(
        template_name="datasource_knowledge_base/base/list_knowledge_bases.html"
    ), name="list"),
    path("update/<int:pk>/", DocumentKnowledgeBaseUpdateView.as_view(
        template_name="datasource_knowledge_base/base/update_knowledge_base.html"
    ), name="update"),
    path("delete/<int:pk>/", DocumentKnowledgeBaseDeleteView.as_view(
        template_name="datasource_knowledge_base/base/confirm_delete_knowledge_base.html"
    ), name="delete"),
]
