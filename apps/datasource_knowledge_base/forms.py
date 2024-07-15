

from django import forms
from .models import DocumentKnowledgeBaseConnection, KnowledgeBaseDocument


class DocumentKnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = DocumentKnowledgeBaseConnection
        fields = [
            'provider',
            'host_url',
            'provider_api_key',
            'assistant',
            'name',
            'description',
            'vectorizer',
            'vectorizer_api_key',
            'embedding_chunk_size',
            'embedding_chunk_overlap',
            'search_instance_retrieval_limit'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


############################################################################################################


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DocumentUploadForm(forms.Form):
    document_files = MultipleFileField(label='Select Documents to Upload', required=True)

    class Meta:
        pass
