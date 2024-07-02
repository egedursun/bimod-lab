from django.db import models


class PermissionNames:
    ADD_LLM_CORES = 'add_llm_cores'
    UPDATE_LLM_CORES = 'update_llm_cores'
    LIST_LLM_CORES = 'list_llm_cores'
    DELETE_LLM_CORES = 'delete_llm_cores'

    ADD_ORGANIZATIONS = 'add_organizations'
    UPDATE_ORGANIZATIONS = 'update_organizations'
    LIST_ORGANIZATIONS = 'list_organizations'
    DELETE_ORGANIZATIONS = 'delete_organizations'

    LIST_TRANSACTIONS = 'list_transactions'

    ADD_USERS = 'add_users'
    UPDATE_USERS = 'update_users'
    LIST_USERS = 'list_users'
    DELETE_USERS = 'delete_users'

    MODIFY_USER_PERMISSIONS = 'modify_user_permissions'
    LIST_USER_PERMISSIONS = 'list_user_permissions'

    ADD_ASSISTANTS = 'add_assistants'
    UPDATE_ASSISTANTS = 'update_assistants'
    LIST_ASSISTANTS = 'list_assistants'
    DELETE_ASSISTANTS = 'delete_assistants'

    CREATE_AND_USE_CHATS = 'create_and_use_chats'
    REMOVE_CHATS = 'remove_chats'

    ADD_ASSISTANT_MEMORIES = 'add_assistant_memories'
    UPDATE_ASSISTANT_MEMORIES = 'update_assistant_memories'
    LIST_ASSISTANT_MEMORIES = 'list_assistant_memories'
    DELETE_ASSISTANT_MEMORIES = 'delete_assistant_memories'

    EXPORT_ASSISTANT = 'export_assistant'

    ADD_ORCHESTRATIONS = 'add_orchestrations'
    UPDATE_ORCHESTRATIONS = 'update_orchestrations'
    LIST_ORCHESTRATIONS = 'list_orchestrations'
    DELETE_ORCHESTRATIONS = 'delete_orchestrations'

    ADD_FILE_SYSTEMS = 'add_file_systems'
    UPDATE_FILE_SYSTEMS = 'update_file_systems'
    LIST_FILE_SYSTEMS = 'list_file_systems'
    DELETE_FILE_SYSTEMS = 'delete_file_systems'

    ADD_WEB_BROWSERS = 'add_web_browsers'
    UPDATE_WEB_BROWSERS = 'update_web_browsers'
    LIST_WEB_BROWSERS = 'list_web_browsers'
    DELETE_WEB_BROWSERS = 'delete_web_browsers'

    ADD_SQL_DATABASES = 'add_sql_databases'
    UPDATE_SQL_DATABASES = 'update_sql_databases'
    LIST_SQL_DATABASES = 'list_sql_databases'
    DELETE_SQL_DATABASES = 'delete_sql_databases'

    ADD_NOSQL_DATABASES = 'add_nosql_databases'
    UPDATE_NOSQL_DATABASES = 'update_nosql_databases'
    LIST_NOSQL_DATABASES = 'list_nosql_databases'
    DELETE_NOSQL_DATABASES = 'delete_nosql_databases'

    ADD_KNOWLEDGE_BASES = 'add_knowledge_bases'
    UPDATE_KNOWLEDGE_BASES = 'update_knowledge_bases'
    LIST_KNOWLEDGE_BASES = 'list_knowledge_bases'
    DELETE_KNOWLEDGE_BASES = 'delete_knowledge_bases'

    ADD_IMAGE_STORAGES = 'add_image_storages'
    UPDATE_IMAGE_STORAGES = 'update_image_storages'
    LIST_IMAGE_STORAGES = 'list_image_storages'
    DELETE_IMAGE_STORAGES = 'delete_image_storages'

    ADD_VIDEO_STORAGES = 'add_video_storages'
    UPDATE_VIDEO_STORAGES = 'update_video_storages'
    LIST_VIDEO_STORAGES = 'list_video_storages'
    DELETE_VIDEO_STORAGES = 'delete_video_storages'

    ADD_AUDIO_STORAGES = 'add_audio_storages'
    UPDATE_AUDIO_STORAGES = 'update_audio_storages'
    LIST_AUDIO_STORAGES = 'list_audio_storages'
    DELETE_AUDIO_STORAGES = 'delete_audio_storages'

    ADD_FUNCTIONS = 'add_functions'
    UPDATE_FUNCTIONS = 'update_functions'
    LIST_FUNCTIONS = 'list_functions'
    DELETE_FUNCTIONS = 'delete_functions'

    ADD_APIS = 'add_apis'
    UPDATE_APIS = 'update_apis'
    LIST_APIS = 'list_apis'
    DELETE_APIS = 'delete_apis'

    ADD_SCHEDULED_JOBS = 'add_scheduled_jobs'
    UPDATE_SCHEDULED_JOBS = 'update_scheduled_jobs'
    LIST_SCHEDULED_JOBS = 'list_scheduled_jobs'
    DELETE_SCHEDULED_JOBS = 'delete_scheduled_jobs'

    ADD_TRIGGERS = 'add_triggers'
    UPDATE_TRIGGERS = 'update_triggers'
    LIST_TRIGGERS = 'list_triggers'
    DELETE_TRIGGERS = 'delete_triggers'

    CAN_GENERATE_IMAGES = 'can_generate_images'

    CAN_GENERATE_AUDIO = 'can_generate_audio'

    ADD_INTEGRATIONS = 'add_integrations'
    UPDATE_INTEGRATIONS = 'update_integrations'
    LIST_INTEGRATIONS = 'list_integrations'
    DELETE_INTEGRATIONS = 'delete_integrations'

    ADD_META_INTEGRATIONS = 'add_meta_integrations'
    UPDATE_META_INTEGRATIONS = 'update_meta_integrations'
    LIST_META_INTEGRATIONS = 'list_meta_integrations'
    DELETE_META_INTEGRATIONS = 'delete_meta_integrations'


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
