"""
This module contains views related to user profile management and settings within the web project.

Views:
- `UserSettingsView`: Renders the user settings page, ensuring the user is authenticated.
- `UserProfileListView`: Displays the user's profile details, including personal information and saved credit cards, allowing updates to the profile and credit card information.
- `UserProfileResetPasswordView`: Handles the process of sending a password reset email to the user.
- `RemoveCardView`: Allows users to remove a saved credit card from their profile.

All views in this module require user authentication, enforced by the `LoginRequiredMixin`.

Note:
- These views rely on forms and utility functions from `apps.user_profile_management` for handling user-related data.
- The views make extensive use of the `TemplateLayout` for initializing and rendering templates.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_codebase.models import CodeRepositoryStorageConnection, CodeBaseRepository
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection, KnowledgeBaseDocument
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.datasource_sql.models import SQLDatabaseConnection, CustomSQLQuery
from apps.export_assistants.models import ExportAssistantAPI
from apps.leanmod.models import LeanAssistant, ExpertNetwork
from apps.llm_core.models import LLMCore
from apps.memories.models import AssistantMemory
from apps.message_templates.models import MessageTemplate
from apps.mm_apis.models import CustomAPI
from apps.mm_functions.models import CustomFunction
from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_scripts.models import CustomScript
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.multimodal_chat.models import MultimodalChat, MultimodalLeanChat
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class UserSettingsView(TemplateView, LoginRequiredMixin):
    """
    Displays and manages user settings.

    GET:
    - Renders the user settings page.
    - Provides necessary context data initialized by TemplateLayout.
    """
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DeleteAllOrganizationsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all organizations associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_organizations:Organization = Organization.objects.filter(users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ORGANIZATIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ORGANIZATIONS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to delete organizations.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for organization in user_organizations:
                organization.delete()
            messages.success(request, "All organizations associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting organizations: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllLLMModelsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all LLM models associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_llm_models = LLMCore.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL LLM MODELS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL LLM MODELS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LLM_CORES):
            messages.error(self.request, "You do not have permission to delete LLM models.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for llm_model in user_llm_models:
                llm_model.delete()
            messages.success(request, "All LLM models associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting LLM models: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllAssistantsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all assistants associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = Assistant.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ASSISTANTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANTS):
            messages.error(self.request, "You do not have permission to delete assistants.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting assistants: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllLeanAssistantsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all lean assistants associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = LeanAssistant.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL LEAN ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL LEAN ASSISTANTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to delete LeanMod assistants.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All lean assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting lean assistants: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllExpertNetworksView(View, LoginRequiredMixin):
    """
    Handles the deletion of expert networks associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = ExpertNetwork.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL EXPERT NETWORKS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL EXPERT NETWORKS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to delete expert networks.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All expert networks associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting expert networks: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllChatsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all chat messages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_chats = MultimodalChat.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL CHATS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CHATS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_CHATS):
            messages.error(self.request, "You do not have permission to delete chats.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for chat in user_chats:
                chat.delete()
            messages.success(request, "All chat messages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting chat messages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllLeanChatsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all LeanMod chat messages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_chats = MultimodalLeanChat.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL LEANMOD CHATS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL LEANMOD CHATS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_LEAN_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_LEAN_CHATS):
            messages.error(self.request, "You do not have permission to delete LeanMod chats.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for chat in user_chats:
                chat.delete()
            messages.success(request, "All LeanMod® chat messages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting LeanMod® chat messages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllStarredMessagesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all starred messages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_starred_messages = StarredMessage.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL STARRED MESSAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL STARRED MESSAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to remove starred messages.")
            return redirect('user_settings:settings')
        ##############################

        # [2] Delete ALL items in the queryset
        try:
            for starred_message in user_starred_messages:
                starred_message.delete()
            messages.success(request, "All starred messages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting starred messages: {e}")

        # [3] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMemoriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all memories associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_memories = AssistantMemory.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MEMORIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MEMORIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANT_MEMORIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANT_MEMORIES):
            messages.error(self.request, "You do not have permission to delete assistant memories.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for memory in user_memories:
                memory.delete()
            messages.success(request, "All memories associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting memories: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMessageTemplatesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all message templates associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_message_templates = MessageTemplate.objects.filter(user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MESSAGE TEMPLATES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MESSAGE TEMPLATES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - REMOVE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to delete message templates.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for message_template in user_message_templates:
                message_template.delete()
            messages.success(request, "All message templates associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting message templates: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllExportAssistantsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all exported assistants associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_exported_assistants = ExportAssistantAPI.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL EXPORTED ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL EXPORTED ASSISTANTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPORT_ASSISTANT):
            messages.error(self.request, "You do not have permission to delete exported assistants.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for exported_assistant in user_exported_assistants:
                exported_assistant.delete()
            messages.success(request, "All exported assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting exported assistants: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllOrchestrationsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all orchestrations associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_orchestrations = Maestro.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ORCHESTRATIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ORCHESTRATIONS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to delete orchestrations.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for orchestration in user_orchestrations:
                orchestration.delete()
            messages.success(request, "All orchestrations associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting orchestrations: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllFileSystemsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all file systems associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_file_systems = DataSourceFileSystem.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL FILE SYSTEMS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL FILE SYSTEMS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_FILE_SYSTEMS):
            messages.error(self.request, "You do not have permission to delete file systems.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for file_system in user_file_systems:
                file_system.delete()
            messages.success(request, "All file systems associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting file systems: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllWebBrowsersView(View, LoginRequiredMixin):
    """
    Handles the deletion of all web browsers associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_web_browsers = DataSourceBrowserConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL WEB BROWSERS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL WEB BROWSERS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_WEB_BROWSERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_WEB_BROWSERS):
            messages.error(self.request, "You do not have permission to delete web browsers.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for web_browser in user_web_browsers:
                web_browser.delete()
            messages.success(request, "All web browsers associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting web browsers: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllSQLDatabasesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all SQL databases associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_sql_databases = SQLDatabaseConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL SQL DATABASES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL SQL DATABASES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to delete SQL databases.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for sql_database in user_sql_databases:
                sql_database.delete()
            messages.success(request, "All SQL databases associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting SQL databases: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllCustomSQLQueriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all custom SQL queries associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_custom_sql_queries = CustomSQLQuery.objects.filter(
            database_connection__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL CUSTOM SQL QUERIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CUSTOM SQL QUERIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to delete custom SQL queries.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for custom_sql_query in user_custom_sql_queries:
                custom_sql_query.delete()
            messages.success(request, "All custom SQL queries associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting custom SQL queries: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllKnowledgeBasesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all knowledge bases associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL KNOWLEDGE BASES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL KNOWLEDGE BASES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASES):
            messages.error(self.request, "You do not have permission to delete knowledge bases.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for knowledge_base in user_knowledge_bases:
                knowledge_base.delete()
            messages.success(request, "All knowledge bases associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting knowledge bases: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllKnowledgeBaseDocumentsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all knowledge base documents associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_knowledge_base_documents = KnowledgeBaseDocument.objects.filter(
            knowledge_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL KNOWLEDGE BASE DOCUMENTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL KNOWLEDGE BASE DOCUMENTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to delete knowledge base documents.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for knowledge_base_document in user_knowledge_base_documents:
                knowledge_base_document.delete()
            messages.success(request, "All knowledge base documents associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting knowledge base documents: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllCodeStoragesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all code storages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_code_storages = CodeRepositoryStorageConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL CODE STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL CODE STORAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_BASE):
            messages.error(self.request, "You do not have permission to delete code base storages.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for code_storage in user_code_storages:
                code_storage.delete()
            messages.success(request, "All code storages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting code storages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllRepositoriesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all repositories associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_repositories = CodeBaseRepository.objects.filter(
            knowledge_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL REPOSITORIES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL REPOSITORIES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to delete code repositories.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for repository in user_repositories:
                repository.delete()
            messages.success(request, "All repositories associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting repositories: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMLModelStoragesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all ML model storages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_ml_model_storages = DataSourceMLModelConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ML MODEL STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ML MODEL STORAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to delete ML model storages.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for ml_model_storage in user_ml_model_storages:
                ml_model_storage.delete()
            messages.success(request, "All ML model storages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting ML model storages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMLModelsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all ML models associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_ml_models = DataSourceMLModelItem.objects.filter(
            ml_model_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ML MODELS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ML MODELS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML model files.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for ml_model in user_ml_models:
                ml_model.delete()
            messages.success(request, "All ML models associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting ML models: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMediaStoragesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all media storages associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_media_storages = DataSourceMediaStorageConnection.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MEDIA STORAGES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MEDIA STORAGES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to delete media storages.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for media_storage in user_media_storages:
                media_storage.delete()
            messages.success(request, "All media storages associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting media storages: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllMultimediaFilesView(View, LoginRequiredMixin):
    """
    Handles the deletion of all multimedia files associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_multimedia_files = DataSourceMediaStorageItem.objects.filter(
            storage_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL MULTIMEDIA FILES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL MULTIMEDIA FILES'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to delete multimedia files.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for multimedia_file in user_multimedia_files:
                multimedia_file.delete()
            messages.success(request, "All multimedia files associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting multimedia files: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllFunctionsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all functions associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_functions = CustomFunction.objects.filter(created_by_user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL FUNCTIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL FUNCTIONS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to delete custom functions.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for function in user_functions:
                function.delete()
            messages.success(request, "All functions associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting functions: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllAPIsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all APIs associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_apis = CustomAPI.objects.filter(created_by_user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL APIS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL APIS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_APIS):
            messages.error(self.request, "You do not have permission to delete custom APIs.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for api in user_apis:
                api.delete()
            messages.success(request, "All APIs associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting APIs: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllScriptsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all scripts associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_scripts = CustomScript.objects.filter(created_by_user=user).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL SCRIPTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL SCRIPTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCRIPTS):
            messages.error(self.request, "You do not have permission to delete custom Scripts.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for script in user_scripts:
                script.delete()
            messages.success(request, "All scripts associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting scripts: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllScheduledJobsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all scheduled jobs associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_scheduled_jobs = ScheduledJob.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL SCHEDULED JOBS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL SCHEDULED JOBS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to delete scheduled jobs.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for scheduled_job in user_scheduled_jobs:
                scheduled_job.delete()
            messages.success(request, "All scheduled jobs associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting scheduled jobs: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')


class DeleteAllTriggeredJobsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all triggered jobs associated with the user account.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        user_triggered_jobs = TriggeredJob.objects.filter(trigger_assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL TRIGGERED JOBS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL TRIGGERED JOBS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_TRIGGERS):
            messages.error(self.request, "You do not have permission to delete triggered jobs.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for triggered_job in user_triggered_jobs:
                triggered_job.delete()
            messages.success(request, "All triggered jobs associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting triggered jobs: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
