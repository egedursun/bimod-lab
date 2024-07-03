from django.db import models

from apps.assistants.utils import generate_random_string


# Create your models here.

class Assistant(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='assistants')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='assistants')
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    # this description is for the users to see, not included in the API call for the LLM (e.g. OpenAI)
    instructions = models.TextField(default="", blank=True)
    response_template = models.TextField(default="", blank=True)
    audience = models.CharField(max_length=1000)
    tone = models.CharField(max_length=1000)

    # assistant image
    assistant_image_save_path = 'assistant_images/%Y/%m/%d/' + generate_random_string()
    assistant_image = models.ImageField(upload_to=assistant_image_save_path, blank=True, max_length=1000,
                                           null=True)

    ##############################
    # add the chat FK fields here
    ##############################
    # ...this will not be added now
    ##############################

    ##############################
    # add the data source FK fields here
    ##############################
    # ...this will not be added now
    ##############################

    ##############################
    # add the multi-modality tools FK fields here
    ##############################
    # ...this will not be added now
    ##############################

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='assistants_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='assistants_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Assistant"
        verbose_name_plural = "Assistants"
        ordering = ["-created_at"]
