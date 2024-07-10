from django.db import models

from apps.assistants.utils import generate_random_string


ASSISTANT_RESPONSE_LANGUAGES = [
    # User's question language
    ("auto", "Auto (Detect)"),

    ("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German"), ("it", "Italian"),
    ("pt", "Portuguese"), ("nl", "Dutch"), ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
    ("zh", "Chinese"), ("ar", "Arabic"), ("tr", "Turkish"), ("pl", "Polish"), ("sv", "Swedish"),
    ("da", "Danish"), ("fi", "Finnish"), ("no", "Norwegian"), ("he", "Hebrew"), ("id", "Indonesian"),
    ("ms", "Malay"), ("th", "Thai"), ("hi", "Hindi"), ("hu", "Hungarian"), ("cs", "Czech"),
    ("sk", "Slovak"), ("uk", "Ukrainian"), ("ro", "Romanian"), ("bg", "Bulgarian"), ("el", "Greek"),
    ("fi", "Finnish"), ("et", "Estonian"), ("lv", "Latvian"), ("lt", "Lithuanian"), ("hr", "Croatian"),
    ("sr", "Serbian"), ("sl", "Slovenian"), ("mk", "Macedonian"), ("sq", "Albanian"), ("bs", "Bosnian"),
    ("is", "Icelandic"), ("cy", "Welsh"), ("ga", "Irish"),
]
ASSISTANT_RESPONSE_LANGUAGES = [ASSISTANT_RESPONSE_LANGUAGES[0]] + sorted(ASSISTANT_RESPONSE_LANGUAGES[1:], key=lambda x: x[1])


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
    response_language = models.CharField(max_length=10, choices=ASSISTANT_RESPONSE_LANGUAGES, default="auto")
    max_retry_count = models.IntegerField(default=3)

    time_awareness = models.BooleanField(default=True)
    place_awareness = models.BooleanField(default=True)

    # assistant image
    assistant_image_save_path = 'assistant_images/%Y/%m/%d/' + generate_random_string()
    assistant_image = models.ImageField(upload_to=assistant_image_save_path, blank=True, max_length=1000,
                                           null=True)

    memories = models.ManyToManyField("memories.AssistantMemory", related_name='assistants',
                                      blank=True)

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
