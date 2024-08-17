from django.db import models

from apps.assistants.models import ASSISTANT_RESPONSE_LANGUAGES
from apps.assistants.utils import generate_random_string


ORCHESTRATION_QUERY_LOG_TYPES = [
    ("info", "Info"),
    ("error", "Error"),
    ("worker_request", "Worker Request"),
    ("worker_response", "Worker Response"),
    ("maestro_answer", "Maestro Answer"),
]


class OrchestrationQueryLogTypesNames:
    INFO = "info"
    ERROR = "error"
    WORKER_REQUEST = "worker_request"
    WORKER_RESPONSE = "worker_response"
    MAESTRO_ANSWER = "maestro_answer"

    @staticmethod
    def as_list():
        return [OrchestrationQueryLogTypesNames.INFO, OrchestrationQueryLogTypesNames.ERROR,
                OrchestrationQueryLogTypesNames.WORKER_REQUEST, OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
                OrchestrationQueryLogTypesNames.MAESTRO_ANSWER]


class Maestro(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='maestros')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='maestros')
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)

    instructions = models.TextField(default="", blank=True)
    workflow_step_guide = models.TextField(default="", blank=True)
    maximum_assistant_limits = models.IntegerField(default=10)

    response_template = models.TextField(default="", blank=True)
    audience = models.CharField(max_length=1000)
    tone = models.CharField(max_length=1000)
    response_language = models.CharField(max_length=10, choices=ASSISTANT_RESPONSE_LANGUAGES, default="auto")

    maestro_image_save_path = 'maestro_images/%Y/%m/%d/' + generate_random_string()
    maestro_image = models.ImageField(upload_to=maestro_image_save_path, blank=True, max_length=5000, null=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='maestros_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='maestros_last_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ########################################
    # ORCHESTRATION WORKERS
    ########################################

    workers = models.ManyToManyField('assistants.Assistant', related_name='maestros', blank=True)

    def __str__(self):
        return self.name + " - " + self.organization.name + " - " + self.llm_model.name

    class Meta:
        verbose_name = "Maestro"
        verbose_name_plural = "Maestros"
        indexes = [
            # Single-field indexes
            models.Index(fields=["organization"]),
            models.Index(fields=["llm_model"]),
            models.Index(fields=["name"]),
            models.Index(fields=["response_language"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

            # Two-field composite indexes
            models.Index(fields=["organization", "llm_model"]),
            models.Index(fields=["organization", "name"]),
            models.Index(fields=["organization", "created_by_user"]),
            models.Index(fields=["organization", "last_updated_by_user"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["organization", "updated_at"]),
            models.Index(fields=["llm_model", "name"]),
            models.Index(fields=["llm_model", "created_by_user"]),
            models.Index(fields=["llm_model", "last_updated_by_user"]),
            models.Index(fields=["llm_model", "created_at"]),
            models.Index(fields=["llm_model", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["organization", "llm_model", "name"]),
            models.Index(fields=["organization", "llm_model", "created_by_user"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user"]),
            models.Index(fields=["organization", "llm_model", "created_at"]),
            models.Index(fields=["organization", "llm_model", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at"]),
            models.Index(fields=["organization", "name", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at"]),
            models.Index(fields=["llm_model", "name", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),

            # Four-field composite indexes
            models.Index(fields=["organization", "llm_model", "name", "created_at"]),
            models.Index(fields=["organization", "llm_model", "name", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at", "updated_at"]),
        ]
        unique_together = [["organization", "llm_model", "name"]]


class OrchestrationQuery(models.Model):
    maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='orchestration_queries_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='orchestration_queries_last_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.query_text + " - " + self.maestro.name + " - " + self.maestro.organization.name

    class Meta:
        verbose_name = "Orchestration Query"
        verbose_name_plural = "Orchestration Queries"
        indexes = [
            # Single-field indexes
            models.Index(fields=["maestro"]),
            models.Index(fields=["query_text"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),

            # Two-field composite indexes
            models.Index(fields=["maestro", "query_text"]),
            models.Index(fields=["maestro", "created_by_user"]),
            models.Index(fields=["maestro", "last_updated_by_user"]),
            models.Index(fields=["maestro", "created_at"]),
            models.Index(fields=["maestro", "updated_at"]),
            models.Index(fields=["query_text", "created_at"]),
            models.Index(fields=["query_text", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),

            # Three-field composite indexes
            models.Index(fields=["maestro", "query_text", "created_at"]),
            models.Index(fields=["maestro", "query_text", "updated_at"]),
            models.Index(fields=["maestro", "created_by_user", "created_at"]),
            models.Index(fields=["maestro", "created_by_user", "updated_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "created_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["query_text", "created_at", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),

            # Four-field composite indexes
            models.Index(fields=["maestro", "query_text", "created_at", "updated_at"]),
            models.Index(fields=["maestro", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["maestro", "last_updated_by_user", "created_at", "updated_at"]),
        ]
        unique_together = [["maestro", "query_text"]]


class OrchestrationQueryLog(models.Model):
    orchestration_query = models.ForeignKey(OrchestrationQuery, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=100, choices=ORCHESTRATION_QUERY_LOG_TYPES, default="info")

    log_text_content = models.TextField()
    log_image_contents = models.JSONField(default=list, blank=True, null=True)
    log_file_contents = models.JSONField(default=list, blank=True, null=True)
    log_audio_contents = models.JSONField(default=list, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orchestration_query.query_text + " - " + self.orchestration_query.maestro.name + " - " + self.orchestration_query.maestro.organization.name

    class Meta:
        verbose_name = "Orchestration Query Log"
        verbose_name_plural = "Orchestration Query Logs"
        indexes = [
            # Single-field indexes
            models.Index(fields=["orchestration_query"]),
            models.Index(fields=["created_at"]),

            # Two-field composite indexes
            models.Index(fields=["orchestration_query", "created_at"]),
        ]
        unique_together = [["orchestration_query", "created_at"]]
