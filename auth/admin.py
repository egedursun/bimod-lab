from django.contrib import admin
from .models import Profile, UserCreditCard


# Register your models here.
class Member(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "is_verified",
        "created_at",
    )


@admin.register(UserCreditCard)
class UserCreditCardAdmin(admin.ModelAdmin):
    list_display = (
        "name_on_card",
        "card_number",
        "card_expiration_month",
        "card_expiration_year",
        "card_cvc",
        "created_at",
    )


admin.site.register(Profile, Member)
