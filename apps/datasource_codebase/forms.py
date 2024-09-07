from django import forms

from apps.datasource_codebase.models import CodeRepositoryStorageConnection


class CodeRepositoryStorageForm(forms.ModelForm):
    class Meta:
        model = CodeRepositoryStorageConnection
        fields = [
            'provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'description', 'vectorizer',
            'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap', 'search_instance_retrieval_limit'
        ]
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}
