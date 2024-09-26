from django.contrib import admin

from apps.datasource_codebase.models import CodeBaseRepositoryChunk


@admin.register(CodeBaseRepositoryChunk)
class CodeBaseRepositoryChunkAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'repository', 'chunk_repository_uri', 'knowledge_base_uuid',
                    'repository_uuid', 'created_at']
    list_filter = ['repository', 'knowledge_base_uuid', 'repository_uuid', 'created_at']
    search_fields = ['repository', 'chunk_content', 'chunk_metadata', 'chunk_repository_uri',
                     'knowledge_base_uuid', 'created_at']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
