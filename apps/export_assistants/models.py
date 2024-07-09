from django.db import models
from django.utils import timezone

from apps.export_assistants.utils import generate_assistant_custom_api_key, generate_endpoint
from config.settings import EXPORT_API_BASE_URL, BASE_URL


# Create your models here.


class RequestLog(models.Model):
    export_assistant = models.ForeignKey('ExportAssistantAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class ExportAssistantAPI(models.Model):
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    request_limit_per_hour = models.IntegerField(default=1000)
    is_online = models.BooleanField(default=True)

    custom_api_key = models.CharField(max_length=1000, blank=True, null=True, unique=True)
    endpoint = models.CharField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='export_assistants_created_by_user')

    def __str__(self):
        return self.assistant.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # generate the endpoint for the exported assistant
        if not self.endpoint:
            self.endpoint = BASE_URL + "/" + EXPORT_API_BASE_URL + "/" + generate_endpoint(self.assistant)

        # generate the API key for non-public usage of the exported assistant
        if not self.custom_api_key and (not self.is_public):
            self.custom_api_key = generate_assistant_custom_api_key(self.assistant)
        super().save(force_insert, force_update, using, update_fields)

    def requests_in_last_hour(self):
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        return RequestLog.objects.filter(export_assistant=self, timestamp__gte=one_hour_ago).count()

    def requests_limit_reached(self):
        return self.requests_in_last_hour() >= self.request_limit_per_hour

    class Meta:
        verbose_name = "Export Assistant API"
        verbose_name_plural = "Export Assistant APIs"
        ordering = ['-created_at']
