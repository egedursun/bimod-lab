from django import forms

from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


class DocumentKnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = DocumentKnowledgeBaseConnection
        fields = [
            'provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'description', 'vectorizer',
            'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap', 'search_instance_retrieval_limit'
        ]
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}
