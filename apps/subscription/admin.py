from django.contrib import admin

from apps.subscription.models import Subscription
from .models import SUBSCRIPTION_BALANCE_DISCOUNT_RATES, SUBSCRIPTION_LIMITS, SUBSCRIPTION_COSTS


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "user",

        ##############################
        "name_on_card",
        "card_number",
        "card_expiration_month",
        "card_expiration_year",
        "card_cvc",
        ##############################

        "subscription_plan",
        "max_number_of_llm_cores",
        "max_number_of_users",
        "max_number_of_assistants",
        "max_number_of_chats",
        "max_orchestrations",
        "max_providers",
        "max_file_systems",
        "max_web_browsers",
        "max_sql_databases",
        "max_knowledge_bases",
        "max_documents",
        "max_functions",
        "max_api",
        "max_scheduled_jobs",
        "max_triggers",
        "max_integrations",
        "max_meta_integrations",
        "allow_long_term_memory",
        "allow_image_storage",
        "allow_video_storage",
        "allow_audio_storage",
        "allow_image_gen_and_analysis",
        "allow_audio_gen_and_analysis",
        "renewal_day_of_month",
        "created_at",
        "updated_at",
        "created_by_user",
        "last_updated_by_user",
        "subscription_status",
        "next_renewal_date",
    ]
    list_filter = [
        "organization",
        "subscription_plan",
    ]
    search_fields = [
        "organization__name",
    ]
    date_hierarchy = "created_at"
    readonly_fields = [
        "max_number_of_llm_cores",
        "max_number_of_users",
        "max_number_of_assistants",
        "max_number_of_chats",
        "max_orchestrations",
        "max_providers",
        "max_file_systems",
        "max_web_browsers",
        "max_sql_databases",
        "max_knowledge_bases",
        "max_documents",
        "max_functions",
        "max_api",
        "max_scheduled_jobs",
        "max_triggers",
        "max_integrations",
        "max_meta_integrations",
        "allow_long_term_memory",
        "allow_image_storage",
        "allow_video_storage",
        "allow_audio_storage",
        "allow_image_gen_and_analysis",
        "allow_audio_gen_and_analysis",
        "subscription_cost",
        "subscription_balance_discount_rate",
        "subscription_status",
        "created_by_user",
        "last_updated_by_user",
        "created_at",
        "updated_at",
        "renewal_day_of_month",
        "next_renewal_date",
        "subscription_status",
    ]

    fieldsets = (
        (None, {
            "fields": (
                "organization",
                "user",
                "subscription_plan",

                ##############################
                "name_on_card",
                "card_number",
                "card_expiration_month",
                "card_expiration_year",
                "card_cvc",
                ##############################

                "max_number_of_llm_cores",
                "max_number_of_users",
                "max_number_of_assistants",
                "max_number_of_chats",
                "max_orchestrations",
                "max_providers",
                "max_file_systems",
                "max_web_browsers",
                "max_sql_databases",
                "max_knowledge_bases",
                "max_documents",
                "max_functions",
                "max_api",
                "max_scheduled_jobs",
                "max_triggers",
                "max_integrations",
                "max_meta_integrations",
                "allow_long_term_memory",
                "allow_image_storage",
                "allow_video_storage",
                "allow_audio_storage",
                "allow_image_gen_and_analysis",
                "allow_audio_gen_and_analysis",
                "renewal_day_of_month",
                "subscription_status",
                "next_renewal_date",
            )
        }),
        ("Metadata", {
            "fields": (
                "created_at",
                "updated_at",
                "created_by_user",
                "last_updated_by_user",
            )
        }),
    )

    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        # Calculate the subscription cost.
        obj.subscription_cost = SUBSCRIPTION_COSTS[obj.subscription_plan]
        obj.subscription_balance_discount_rate = SUBSCRIPTION_BALANCE_DISCOUNT_RATES[obj.subscription_plan]
        obj.max_number_of_llm_cores = SUBSCRIPTION_LIMITS[obj.subscription_plan]["max_number_of_llm_cores"]
        obj.max_number_of_users = SUBSCRIPTION_LIMITS[obj.subscription_plan]["max_number_of_users"]
        obj.max_number_of_assistants = SUBSCRIPTION_LIMITS[obj.subscription_plan]["max_number_of_assistants"]
        obj.max_number_of_chats = SUBSCRIPTION_LIMITS[obj.subscription_plan]["max_number_of_chats"]
        obj.max_orchestrations = SUBSCRIPTION_LIMITS[obj.subscription_plan]["orchestrations"]
        obj.max_providers = SUBSCRIPTION_LIMITS[obj.subscription_plan]["providers"]
        obj.max_file_systems = SUBSCRIPTION_LIMITS[obj.subscription_plan]["file_systems"]
        obj.max_web_browsers = SUBSCRIPTION_LIMITS[obj.subscription_plan]["web_browsers"]
        obj.max_sql_databases = SUBSCRIPTION_LIMITS[obj.subscription_plan]["sql_databases"]
        obj.max_knowledge_bases = SUBSCRIPTION_LIMITS[obj.subscription_plan]["knowledge_bases"]
        obj.max_documents = SUBSCRIPTION_LIMITS[obj.subscription_plan]["documents"]
        obj.max_functions = SUBSCRIPTION_LIMITS[obj.subscription_plan]["functions"]
        obj.max_api = SUBSCRIPTION_LIMITS[obj.subscription_plan]["api"]
        obj.max_scheduled_jobs = SUBSCRIPTION_LIMITS[obj.subscription_plan]["scheduled_jobs"]
        obj.max_triggers = SUBSCRIPTION_LIMITS[obj.subscription_plan]["triggers"]
        obj.max_integrations = SUBSCRIPTION_LIMITS[obj.subscription_plan]["integrations"]
        obj.max_meta_integrations = SUBSCRIPTION_LIMITS[obj.subscription_plan]["meta_integrations"]
        obj.allow_long_term_memory = SUBSCRIPTION_LIMITS[obj.subscription_plan]["long_term_memory"]
        obj.allow_image_storage = SUBSCRIPTION_LIMITS[obj.subscription_plan]["image_storage"]
        obj.allow_video_storage = SUBSCRIPTION_LIMITS[obj.subscription_plan]["video_storage"]
        obj.allow_audio_storage = SUBSCRIPTION_LIMITS[obj.subscription_plan]["audio_storage"]
        obj.allow_image_gen_and_analysis = SUBSCRIPTION_LIMITS[obj.subscription_plan]["image_gen_and_analysis"]
        obj.allow_audio_gen_and_analysis = SUBSCRIPTION_LIMITS[obj.subscription_plan]["audio_gen_and_analysis"]
        if obj.subscription_plan != "free":
            obj.subscription_status = "active"
        super().save_model(request, obj, form, change)
