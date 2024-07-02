from django.db import models


# Create your models here.

class Assistant(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='assistants')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='assistants')
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)  # this description is for the users to see, not included
    # in the API call
    instructions = models.TextField(default="", blank=True)
    audience = models.CharField(max_length=255)
    tone = models.CharField(max_length=255)

    ##############################
    # add the chat FK fields here
    ##############################
    # ...
    ##############################

    ##############################
    # add the tool FK fields here
    ##############################
    # ...
    ##############################

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='assistants_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='assistants_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
