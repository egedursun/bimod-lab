from django.db import models


class PermissionNames:
    ######################################################
    ADD_LLM_CORES = 'add_llm_cores'
    UPDATE_LLM_CORES = 'update_llm_cores'
    LIST_LLM_CORES = 'list_llm_cores'
    DELETE_LLM_CORES = 'delete_llm_cores'
    ######################################################
    ADD_ORGANIZATIONS = 'add_organizations'
    UPDATE_ORGANIZATIONS = 'update_organizations'
    LIST_ORGANIZATIONS = 'list_organizations'
    DELETE_ORGANIZATIONS = 'delete_organizations'
    ######################################################
    LIST_TRANSACTIONS = 'list_transactions'
    ######################################################
    ADD_USERS = 'add_users'
    UPDATE_USERS = 'update_users'
    LIST_USERS = 'list_users'
    DELETE_USERS = 'delete_users'
    ######################################################
    MODIFY_USER_PERMISSIONS = 'modify_user_permissions'
    LIST_USER_PERMISSIONS = 'list_user_permissions'
    ######################################################
    ADD_ASSISTANTS = 'add_assistants'
    UPDATE_ASSISTANTS = 'update_assistants'
    LIST_ASSISTANTS = 'list_assistants'
    DELETE_ASSISTANTS = 'delete_assistants'
    ######################################################
    CREATE_AND_USE_CHATS = 'create_and_use_chats'
    REMOVE_CHATS = 'remove_chats'
    ######################################################
    ADD_ASSISTANT_MEMORIES = 'add_assistant_memories'
    UPDATE_ASSISTANT_MEMORIES = 'update_assistant_memories'
    LIST_ASSISTANT_MEMORIES = 'list_assistant_memories'
    DELETE_ASSISTANT_MEMORIES = 'delete_assistant_memories'
    ######################################################
    ADD_EXPORT_ASSISTANT = 'add_export_assistant'
    UPDATE_EXPORT_ASSIST = 'update_export_assistant'
    LIST_EXPORT_ASSISTANT = 'list_export_assistant'
    DELETE_EXPORT_ASSISTANT = 'delete_export_assistant'
    ######################################################
    ADD_ORCHESTRATIONS = 'add_orchestrations'
    UPDATE_ORCHESTRATIONS = 'update_orchestrations'
    LIST_ORCHESTRATIONS = 'list_orchestrations'
    DELETE_ORCHESTRATIONS = 'delete_orchestrations'
    ######################################################
    ADD_FILE_SYSTEMS = 'add_file_systems'
    UPDATE_FILE_SYSTEMS = 'update_file_systems'
    LIST_FILE_SYSTEMS = 'list_file_systems'
    DELETE_FILE_SYSTEMS = 'delete_file_systems'
    ######################################################
    ADD_WEB_BROWSERS = 'add_web_browsers'
    UPDATE_WEB_BROWSERS = 'update_web_browsers'
    LIST_WEB_BROWSERS = 'list_web_browsers'
    DELETE_WEB_BROWSERS = 'delete_web_browsers'
    ######################################################
    ADD_SQL_DATABASES = 'add_sql_databases'
    UPDATE_SQL_DATABASES = 'update_sql_databases'
    LIST_SQL_DATABASES = 'list_sql_databases'
    DELETE_SQL_DATABASES = 'delete_sql_databases'
    ######################################################
    ADD_NOSQL_DATABASES = 'add_nosql_databases'
    UPDATE_NOSQL_DATABASES = 'update_nosql_databases'
    LIST_NOSQL_DATABASES = 'list_nosql_databases'
    DELETE_NOSQL_DATABASES = 'delete_nosql_databases'
    ######################################################
    ADD_KNOWLEDGE_BASES = 'add_knowledge_bases'
    UPDATE_KNOWLEDGE_BASES = 'update_knowledge_bases'
    LIST_KNOWLEDGE_BASES = 'list_knowledge_bases'
    DELETE_KNOWLEDGE_BASES = 'delete_knowledge_bases'
    ######################################################
    ADD_MEDIA_STORAGES = 'add_media_storages'
    UPDATE_MEDIA_STORAGES = 'update_media_storages'
    LIST_MEDIA_STORAGES = 'list_media_storages'
    DELETE_MEDIA_STORAGES = 'delete_media_storages'
    ######################################################
    ADD_ML_MODEL_CONNECTIONS = 'add_ml_model_connections'
    UPDATE_ML_MODEL_CONNECTIONS = 'update_ml_model_connections'
    LIST_ML_MODEL_CONNECTIONS = 'list_ml_model_connections'
    DELETE_ML_MODEL_CONNECTIONS = 'delete_ml_model_connections'
    ######################################################
    ADD_FUNCTIONS = 'add_functions'
    UPDATE_FUNCTIONS = 'update_functions'
    LIST_FUNCTIONS = 'list_functions'
    DELETE_FUNCTIONS = 'delete_functions'
    ######################################################
    ADD_APIS = 'add_apis'
    UPDATE_APIS = 'update_apis'
    LIST_APIS = 'list_apis'
    DELETE_APIS = 'delete_apis'
    ######################################################
    ADD_SCRIPTS = 'add_scripts'
    UPDATE_SCRIPTS = 'update_scripts'
    LIST_SCRIPTS = 'list_scripts'
    DELETE_SCRIPTS = 'delete_scripts'
    ######################################################
    ADD_SCHEDULED_JOBS = 'add_scheduled_jobs'
    UPDATE_SCHEDULED_JOBS = 'update_scheduled_jobs'
    LIST_SCHEDULED_JOBS = 'list_scheduled_jobs'
    DELETE_SCHEDULED_JOBS = 'delete_scheduled_jobs'
    ######################################################
    ADD_TRIGGERS = 'add_triggers'
    UPDATE_TRIGGERS = 'update_triggers'
    LIST_TRIGGERS = 'list_triggers'
    DELETE_TRIGGERS = 'delete_triggers'
    ######################################################
    CAN_GENERATE_IMAGES = 'can_generate_images'
    ######################################################
    CAN_GENERATE_AUDIO = 'can_generate_audio'
    ######################################################
    ADD_INTEGRATIONS = 'add_integrations'
    UPDATE_INTEGRATIONS = 'update_integrations'
    LIST_INTEGRATIONS = 'list_integrations'
    DELETE_INTEGRATIONS = 'delete_integrations'
    ######################################################
    ADD_META_INTEGRATIONS = 'add_meta_integrations'
    UPDATE_META_INTEGRATIONS = 'update_meta_integrations'
    LIST_META_INTEGRATIONS = 'list_meta_integrations'
    DELETE_META_INTEGRATIONS = 'delete_meta_integrations'
    ######################################################
    # ...
    ######################################################
    ADD_STARRED_MESSAGES = 'add_starred_messages'
    LIST_STARRED_MESSAGES = 'list_starred_messages'
    REMOVE_STARRED_MESSAGES = 'remove_starred_messages'
    ######################################################
    ADD_TEMPLATE_MESSAGES = 'add_template_messages'
    LIST_TEMPLATE_MESSAGES = 'list_template_messages'
    UPDATE_TEMPLATE_MESSAGES = 'update_template_messages'
    REMOVE_TEMPLATE_MESSAGES = 'remove_template_messages'


PERMISSION_TYPES = [
    ######################################################
    # ORGANIZATION PERMISSIONS
    ('add_organizations', 'Add Organizations'),
    ('update_organizations', 'Update Organizations'),
    ('list_organizations', 'List Organizations'),
    ('delete_organizations', 'Delete Organizations'),
    ######################################################
    # LLM CORE PERMISSIONS
    ('add_llm_cores', 'Add LLM Cores'),
    ('update_llm_cores', 'Update LLM Cores'),
    ('list_llm_cores', 'List LLM Cores'),
    ('delete_llm_cores', 'Delete LLM Cores'),
    ######################################################
    # TRANSACTION PERMISSIONS
    ('list_transactions', 'List Transactions'),
    ######################################################
    # USER PERMISSIONS
    ('add_users', 'Add Users'),
    ('update_users', 'Update Users'),
    ('list_users', 'List Users'),
    ('delete_users', 'Delete Users'),
    ######################################################
    # USER ROLE MODIFICATION AND READ PERMISSIONS
    ('modify_user_permissions', 'Modify User Permissions'),
    ('list_user_permissions', 'List User Permissions'),
    ######################################################
    # ASSISTANT PERMISSIONS
    ('add_assistants', 'Add Assistants'),
    ('update_assistants', 'Update Assistants'),
    ('list_assistants', 'List Assistants'),
    ('delete_assistants', 'Delete Assistants'),
    ######################################################
    # CHAT PERMISSIONS
    ('create_and_use_chats', 'Create and Use Chats'),
    ('remove_chats', 'Remove Chats'),
    ######################################################
    # MEMORY PERMISSIONS
    ('add_assistant_memories', 'Add Assistant Memories'),
    ('update_assistant_memories', 'Update Assistant Memories'),
    ('list_assistant_memories', 'List Assistant Memories'),
    ('delete_assistant_memories', 'Delete Assistant Memories'),
    ######################################################
    # ASSISTANT EXPORTATION PERMISSIONS
    ('add_export_assistant', 'Add Export Assistant'),
    ('update_export_assistant', 'Update Export Assistant'),
    ('list_export_assistant', 'List Export Assistant'),
    ('delete_export_assistant', 'Delete Export Assistant'),
    ######################################################
    # ORCHESTRATION PERMISSIONS
    ('add_orchestrations', 'Add Orchestrations'),
    ('update_orchestrations', 'Update Orchestrations'),
    ('list_orchestrations', 'List Orchestrations'),
    ('delete_orchestrations', 'Delete Orchestrations'),
    ######################################################
    # FILE SYSTEM PERMISSIONS
    ('add_file_systems', 'Add File Systems'),
    ('update_file_systems', 'Update File Systems'),
    ('list_file_systems', 'List File Systems'),
    ('delete_file_systems', 'Delete File Systems'),
    ######################################################
    # WEB BROWSERS
    ('add_web_browsers', 'Add Web Browsers'),
    ('update_web_browsers', 'Update Web Browsers'),
    ('list_web_browsers', 'List Web Browsers'),
    ('delete_web_browsers', 'Delete Web Browsers'),
    ######################################################
    # SQL DATABASES
    ('add_sql_databases', 'Add SQL Databases'),
    ('update_sql_databases', 'Update SQL Databases'),
    ('list_sql_databases', 'List SQL Databases'),
    ('delete_sql_databases', 'Delete SQL Databases'),
    ######################################################
    # NOSQL DATABASES
    ('add_nosql_databases', 'Add NoSQL Databases'),
    ('update_nosql_databases', 'Update NoSQL Databases'),
    ('list_nosql_databases', 'List NoSQL Databases'),
    ('delete_nosql_databases', 'Delete NoSQL Databases'),
    ######################################################
    # KNOWLEDGE BASES
    ('add_knowledge_bases', 'Add Knowledge Bases'),
    ('update_knowledge_bases', 'Update Knowledge Bases'),
    ('list_knowledge_bases', 'List Knowledge Bases'),
    ('delete_knowledge_bases', 'Delete Knowledge Bases'),
    ######################################################
    # IMAGE STORAGES
    ('add_media_storages', 'Add Media Storages'),
    ('update_media_storages', 'Update Media Storages'),
    ('list_media_storages', 'List Media Storages'),
    ('delete_media_storages', 'Delete Media Storages'),
    ######################################################
    # ML MODEL CONNECTIONS
    ('add_ml_model_connections', 'Add ML Model Connections'),
    ('update_ml_model_connections', 'Update ML Model Connections'),
    ('list_ml_model_connections', 'List ML Model Connections'),
    ('delete_ml_model_connections', 'Delete ML Model Connections'),
    ######################################################
    # FUNCTIONS
    ('add_functions', 'Add Functions'),
    ('update_functions', 'Update Functions'),
    ('list_functions', 'List Functions'),
    ('delete_functions', 'Delete Functions'),
    ######################################################
    # APIS
    ('add_apis', 'Add APIs'),
    ('update_apis', 'Update APIs'),
    ('list_apis', 'List APIs'),
    ('delete_apis', 'Delete APIs'),
    ######################################################
    # SCRIPTS
    ('add_scripts', 'Add Scripts'),
    ('update_scripts', 'Update Scripts'),
    ('list_scripts', 'List Scripts'),
    ('delete_scripts', 'Delete Scripts'),
    ######################################################
    # SCHEDULED JOBS
    ('add_scheduled_jobs', 'Add Scheduled Jobs'),
    ('update_scheduled_jobs', 'Update Scheduled Jobs'),
    ('list_scheduled_jobs', 'List Scheduled Jobs'),
    ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),
    ######################################################
    # TRIGGERS
    ('add_triggers', 'Add Triggers'),
    ('update_triggers', 'Update Triggers'),
    ('list_triggers', 'List Triggers'),
    ('delete_triggers', 'Delete Triggers'),
    ######################################################
    # IMAGE GENERATION
    ('can_generate_images', 'Can Generate Images'),
    ######################################################
    # AUDIO GENERATION
    ('can_generate_audio', 'Can Generate Audio'),
    ######################################################
    # INTEGRATIONS
    ('add_integrations', 'Add Integrations'),
    ('update_integrations', 'Update Integrations'),
    ('list_integrations', 'List Integrations'),
    ('delete_integrations', 'Delete Integrations'),
    ######################################################
    # META INTEGRATIONS
    ('add_meta_integrations', 'Add Meta Integrations'),
    ('update_meta_integrations', 'Update Meta Integrations'),
    ('list_meta_integrations', 'List Meta Integrations'),
    ('delete_meta_integrations', 'Delete Meta Integrations'),
    ######################################################
    # ...
    ######################################################
    # STARRED MESSAGES
    ('add_starred_messages', 'Add Starred Messages'),
    ('list_starred_messages', 'List Starred Messages'),
    ('remove_starred_messages', 'Remove Starred Messages'),
    ######################################################
    # TEMPLATE MESSAGES
    ('add_template_messages', 'Add Template Messages'),
    ('list_template_messages', 'List Template Messages'),
    ('update_template_messages', 'Update Template Messages'),
    ('remove_template_messages', 'Remove Template Messages'),
]


class ActiveUserPermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UserPermission(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="permissions", default=1)
    permission_type = models.CharField(max_length=255, choices=PERMISSION_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    active_permissions = ActiveUserPermissionManager()  # Custom manager for active permissions.

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'permission_type'], name='unique_user_permission')
        ]
        indexes = [
            models.Index(fields=['user', 'permission_type']),
            models.Index(fields=['user', 'permission_type', 'is_active']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['permission_type', 'is_active']),
            models.Index(fields=['permission_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'is_active', 'created_at']),
            models.Index(fields=['user', 'is_active', 'created_at']),
            models.Index(fields=['permission_type', 'is_active', 'created_at']),
        ]

    def get_permission_type_name(self):
        return dict(PERMISSION_TYPES)[self.permission_type]

    def get_permission_type_code(self):
        return self.permission_type
