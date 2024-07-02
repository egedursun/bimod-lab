from django.db import models


PERMISSION_TYPES = [
    # ORGANIZATION PERMISSIONS
    ('add_organizations', 'Add Organizations'),
    ('update_organizations', 'Update Organizations'),
    ('list_organizations', 'List Organizations'),
    ('delete_organizations', 'Delete Organizations'),

    # LLM CORE PERMISSIONS
    ('add_llm_cores', 'Add LLM Cores'),
    ('update_llm_cores', 'Update LLM Cores'),
    ('list_llm_cores', 'List LLM Cores'),
    ('delete_llm_cores', 'Delete LLM Cores'),

    # TRANSACTION PERMISSIONS
    ('list_transactions', 'List Transactions'),

    # USER PERMISSIONS
    ('add_users', 'Add Users'),
    ('update_users', 'Update Users'),
    ('list_users', 'List Users'),
    ('delete_users', 'Delete Users'),

    # USER ROLE MODIFICATION AND READ PERMISSIONS
    ('modify_user_permissions', 'Modify User Permissions'),
    ('list_user_permissions', 'List User Permissions'),

    # ASSISTANT PERMISSIONS
    ('add_assistants', 'Add Assistants'),
    ('update_assistants', 'Update Assistants'),
    ('list_assistants', 'List Assistants'),
    ('delete_assistants', 'Delete Assistants'),

    # CHAT PERMISSIONS
    ('create_and_use_chats', 'Create and Use Chats'),
    ('remove_chats', 'Remove Chats'),

    # MEMORY PERMISSIONS
    ('add_assistant_memories', 'Add Assistant Memories'),
    ('update_assistant_memories', 'Update Assistant Memories'),
    ('list_assistant_memories', 'List Assistant Memories'),
    ('delete_assistant_memories', 'Delete Assistant Memories'),

    # ASSISTANT EXPORTATION PERMISSIONS
    ('export_assistant', 'Export Assistant'),

    # ORCHESTRATION PERMISSIONS
    ('add_orchestrations', 'Add Orchestrations'),
    ('update_orchestrations', 'Update Orchestrations'),
    ('list_orchestrations', 'List Orchestrations'),
    ('delete_orchestration', 'Delete Orchestrations'),

    # FILE SYSTEM PERMISSIONS
    ('add_file_systems', 'Add File Systems'),
    ('update_file_systems', 'Update File Systems'),
    ('list_file_systems', 'List File Systems'),
    ('delete_file_systems', 'Delete File Systems'),

    # WEB BROWSERS
    ('add_web_browsers', 'Add Web Browsers'),
    ('update_web_browsers', 'Update Web Browsers'),
    ('list_web_browsers', 'List Web Browsers'),
    ('delete_web_browsers', 'Delete Web Browsers'),

    # SQL DATABASES
    ('add_sql_databases', 'Add SQL Databases'),
    ('update_sql_databases', 'Update SQL Databases'),
    ('list_sql_databases', 'List SQL Databases'),
    ('delete_sql_databases', 'Delete SQL Databases'),

    # NOSQL DATABASES
    ('add_nosql_databases', 'Add NoSQL Databases'),
    ('update_nosql_databases', 'Update NoSQL Databases'),
    ('list_nosql_databases', 'List NoSQL Databases'),
    ('delete_nosql_databases', 'Delete NoSQL Databases'),

    # KNOWLEDGE BASES
    ('add_knowledge_bases', 'Add Knowledge Bases'),
    ('update_knowledge_bases', 'Update Knowledge Bases'),
    ('list_knowledge_bases', 'List Knowledge Bases'),
    ('delete_knowledge_bases', 'Delete Knowledge Bases'),

    # IMAGE STORAGES
    ('add_image_storages', 'Add Image Storages'),
    ('update_image_storages', 'Update Image Storages'),
    ('list_image_storages', 'List Image Storages'),
    ('delete_image_storages', 'Delete Image Storages'),

    # VIDEO STORAGES
    ('add_video_storages', 'Add Video Storages'),
    ('update_video_storages', 'Update Video Storages'),
    ('list_video_storages', 'List Video Storages'),
    ('delete_video_storages', 'Delete Video Storages'),

    # AUDIO STORAGES
    ('add_audio_storages', 'Add Audio Storages'),
    ('update_audio_storages', 'Update Audio Storages'),
    ('list_audio_storages', 'List Audio Storages'),
    ('delete_audio_storages', 'Delete Audio Storages'),

    # FUNCTIONS
    ('add_functions', 'Add Functions'),
    ('update_functions', 'Update Functions'),
    ('list_functions', 'List Functions'),
    ('delete_functions', 'Delete Functions'),

    # APIS
    ('add_apis', 'Add APIs'),
    ('update_apis', 'Update APIs'),
    ('list_apis', 'List APIs'),
    ('delete_apis', 'Delete APIs'),

    # SCHEDULED JOBS
    ('add_scheduled_jobs', 'Add Scheduled Jobs'),
    ('update_scheduled_jobs', 'Update Scheduled Jobs'),
    ('list_scheduled_jobs', 'List Scheduled Jobs'),
    ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),

    # TRIGGERS
    ('add_triggers', 'Add Triggers'),
    ('update_triggers', 'Update Triggers'),
    ('list_triggers', 'List Triggers'),
    ('delete_triggers', 'Delete Triggers'),

    # IMAGE GENERATION
    ('can_generate_images', 'Can Generate Images'),

    # AUDIO GENERATION
    ('can_generate_audio', 'Can Generate Audio'),

    # INTEGRATIONS
    ('add_integrations', 'Add Integrations'),
    ('update_integrations', 'Update Integrations'),
    ('list_integrations', 'List Integrations'),
    ('delete_integrations', 'Delete Integrations'),

    # META INTEGRATIONS
    ('add_meta_integrations', 'Add Meta Integrations'),
    ('update_meta_integrations', 'Update Meta Integrations'),
    ('list_meta_integrations', 'List Meta Integrations'),
    ('delete_meta_integrations', 'Delete Meta Integrations'),
]


# Create your models here.

class UserPermission(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="permissions", default=1)
    permission_type = models.CharField(max_length=255, choices=PERMISSION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'permission_type'], name='unique_user_permission')
        ]

    def get_permission_type_name(self):
        return dict(PERMISSION_TYPES)[self.permission_type]

    def get_permission_type_code(self):
        return self.permission_type
