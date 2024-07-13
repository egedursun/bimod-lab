import os

from django.db import models

from apps.assistants.utils import generate_random_string
from slugify import slugify


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


CONTEXT_OVERFLOW_STRATEGY = [
    ("stop", "Stop Conversation"),
    ("forget", "Forget Oldest Messages"),
    ("vectorize", "Vectorize Oldest Messages"),
]


class ContextOverflowStrategyNames:
    STOP = "stop"
    FORGET = "forget"
    VECTORIZE = "vectorize"

    @staticmethod
    def as_dict():
        return { "stop": "Stop Conversation", "forget": "Forget Oldest Messages", "vectorize": "Vectorize Oldest Messages" }


VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class VectorizerNames:
    TEXT2VEC_OPENAI = "text2vec-openai"

    @staticmethod
    def as_dict():
        return { "text2vec-openai": "Text2Vec (OpenAI)" }


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

    tool_max_attempts_per_instance = models.IntegerField(default=3)
    tool_max_chains = models.IntegerField(default=3)

    time_awareness = models.BooleanField(default=True)
    place_awareness = models.BooleanField(default=True)

    # assistant image
    assistant_image_save_path = 'assistant_images/%Y/%m/%d/' + generate_random_string()
    assistant_image = models.ImageField(upload_to=assistant_image_save_path, blank=True, max_length=1000,
                                           null=True)

    memories = models.ManyToManyField("memories.AssistantMemory", related_name='assistants',
                                      blank=True)

    context_overflow_strategy = models.CharField(max_length=100, choices=CONTEXT_OVERFLOW_STRATEGY, default="forget")
    # in case of ->
    # - stop: stop the conversation after the limit is reached
    # - forget: forget oldest messages starting from the limit, start from oldest
    # - vectorize: store the messages overflowing the context in the vectorstore, in their relevant assistant/chat dir.
    max_context_messages = models.IntegerField(default=25)
    # only in case of -> vectorize
    vectorizer_name = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai",
                                       null=True, blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    document_base_directory = models.CharField(max_length=1000, null=True, blank=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='assistants_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='assistants_updated_by_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.document_base_directory is None:
            dir_name = f"media/documents/{slugify(self.organization.name)}/{slugify(self.llm_model.model_name)}/{slugify(self.name)}/"
            self.document_base_directory = dir_name
            os.system(f"mkdir -p {dir_name}")
            os.system(f"touch {dir_name}/__init__.py")

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Assistant"
        verbose_name_plural = "Assistants"
        ordering = ["-created_at"]
