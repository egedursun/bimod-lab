"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from config import settings
from web_project.views import SystemView


# Sentry SDK Test
def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


def docs_redirect_view(request):
    return redirect('/static/docs/index.html')


urlpatterns = [
    #################################################################################################################
    # Core Endpoints
    #################################################################################################################
    path("", include("apps.landing.urls", namespace="landing")),
    path("admin/", admin.site.urls),
    path("app/", include("auth.urls")),
    path("app/user_profile_management/", include("apps.user_profile_management.urls", namespace="user_profile_management")),
    path("app/user_settings/", include("apps.user_settings.urls", namespace="user_settings")),
    path("app/dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("app/organization/", include("apps.organization.urls", namespace="organization")),
    path("app/llm_core/", include("apps.llm_core.urls", namespace="llm_core")),
    path("app/llm_transaction/", include("apps.llm_transaction.urls", namespace="llm_transaction")),
    path("app/subscription/", include("apps.subscription.urls", namespace="subscription")),
    path("app/user_management/", include("apps.user_management.urls", namespace="user_management")),
    path("app/user_permissions/", include("apps.user_permissions.urls", namespace="user_permissions")),
    path("app/assistants/", include("apps.assistants.urls", namespace="assistants")),
    path("app/multimodal_chat/", include("apps.multimodal_chat.urls", namespace="multimodal_chat")),
    path("app/memories/", include("apps.memories.urls", namespace="memories")),
    path("app/starred_messages/", include("apps.starred_messages.urls", namespace="starred_messages")),
    path("app/message_templates/", include("apps.message_templates.urls", namespace="message_templates")),
    path("app/export_assistants/", include("apps.export_assistants.urls", namespace="export_assistants")),
    path("app/datasource_sql/", include("apps.datasource_sql.urls", namespace="datasource_sql")),
    path("app/datasource_knowledge_base/", include("apps.datasource_knowledge_base.urls")),
    path("app/datasource_file_systems/", include("apps.datasource_file_systems.urls", namespace="datasource_file_systems")),
    path("app/datasource_media_storages/", include("apps.datasource_media_storages.urls", namespace="datasource_media_storages")),
    path("app/datasource_ml_models/", include("apps.datasource_ml_models.urls", namespace="datasource_ml_models")),
    path("app/datasource_browsers/", include("apps.datasource_browsers.urls", namespace="datasource_browser")),
    path("app/mm_functions/", include("apps.mm_functions.urls", namespace="mm_functions")),
    path("app/mm_apis/", include("apps.mm_apis.urls", namespace="mm_apis")),
    path("app/mm_scripts/", include("apps.mm_scripts.urls", namespace="mm_scripts")),
    path("app/mm_scheduled_jobs/", include("apps.mm_scheduled_jobs.urls", namespace="mm_scheduled_jobs")),
    path("app/mm_triggered_jobs/", include("apps.mm_triggered_jobs.urls", namespace="mm_triggered_jobs")),
    path("app/orchestrations/", include("apps.orchestrations.urls", namespace="orchestrations")),
    path("app/finetuning/", include("apps.finetuning.urls", namespace="finetuning")),
    #################################################################################################################

    #################################################################################################################
    # Meta Endpoints
    #################################################################################################################
    path('app/voidforger/', include("apps._meta.voidforger.urls", namespace="voidforger")),

    #################################################################################################################
    # Support System Endpoints
    path('app/docs/', docs_redirect_view, name='technical_docs'),
    path("app/support_system/", include("apps.support_system.urls", namespace="support_system")),
    path("app/community_forum/", include("apps.community_forum.urls", namespace="community_forum")),
    path("app/blog_app/", include("apps.blog_app.urls", namespace="blog_app")),
    #################################################################################################################
    # Test Endpoints
    #################################################################################################################
    path('sentry/test/', trigger_error),
    #################################################################################################################
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)

HANDLED_HTTP_NEGATIVE_RESPONSES = {
    "client_side": [
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
        410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
        422, 423, 424, 425, 426, 428, 429, 431, 451
    ],
    "server_side": [
        500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
    ],
}

#####################################################################################################################
# CLIENT SIDE ERRORS
#####################################################################################################################

handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler401 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=401)
handler402 = SystemView.as_view(template_name="pages_misc_error.html", status=402)
handler403 = SystemView.as_view(template_name="pages_misc_error.html", status=403)
handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler405 = SystemView.as_view(template_name="pages_misc_error.html", status=405)
handler406 = SystemView.as_view(template_name="pages_misc_error.html", status=406)
handler407 = SystemView.as_view(template_name="pages_misc_error.html", status=407)
handler408 = SystemView.as_view(template_name="pages_misc_error.html", status=408)
handler409 = SystemView.as_view(template_name="pages_misc_error.html", status=409)
handler410 = SystemView.as_view(template_name="pages_misc_error.html", status=410)
handler411 = SystemView.as_view(template_name="pages_misc_error.html", status=411)
handler412 = SystemView.as_view(template_name="pages_misc_error.html", status=412)
handler413 = SystemView.as_view(template_name="pages_misc_error.html", status=413)
handler414 = SystemView.as_view(template_name="pages_misc_error.html", status=414)
handler415 = SystemView.as_view(template_name="pages_misc_error.html", status=415)
handler416 = SystemView.as_view(template_name="pages_misc_error.html", status=416)
handler417 = SystemView.as_view(template_name="pages_misc_error.html", status=417)
handler418 = SystemView.as_view(template_name="pages_misc_error.html", status=418)
handler421 = SystemView.as_view(template_name="pages_misc_error.html", status=421)
handler422 = SystemView.as_view(template_name="pages_misc_error.html", status=422)
handler423 = SystemView.as_view(template_name="pages_misc_error.html", status=423)
handler424 = SystemView.as_view(template_name="pages_misc_error.html", status=424)
handler425 = SystemView.as_view(template_name="pages_misc_error.html", status=425)
handler426 = SystemView.as_view(template_name="pages_misc_error.html", status=426)
handler428 = SystemView.as_view(template_name="pages_misc_error.html", status=428)
handler429 = SystemView.as_view(template_name="pages_misc_error.html", status=429)
handler431 = SystemView.as_view(template_name="pages_misc_error.html", status=431)
handler451 = SystemView.as_view(template_name="pages_misc_error.html", status=451)

#####################################################################################################################
# SERVER SIDE ERRORS
#####################################################################################################################

handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
handler501 = SystemView.as_view(template_name="pages_misc_error.html", status=501)
handler502 = SystemView.as_view(template_name="pages_misc_error.html", status=502)
handler503 = SystemView.as_view(template_name="pages_misc_error.html", status=503)
handler504 = SystemView.as_view(template_name="pages_misc_error.html", status=504)
handler505 = SystemView.as_view(template_name="pages_misc_error.html", status=505)
handler506 = SystemView.as_view(template_name="pages_misc_error.html", status=506)
handler507 = SystemView.as_view(template_name="pages_misc_error.html", status=507)
handler508 = SystemView.as_view(template_name="pages_misc_error.html", status=508)
handler510 = SystemView.as_view(template_name="pages_misc_error.html", status=510)
handler511 = SystemView.as_view(template_name="pages_misc_error.html", status=511)

#####################################################################################################################
# THEME PAGES
#####################################################################################################################

# path("", include("apps.theme.dashboards.urls")),
# layouts urls
# path("", include("apps.theme.layouts.urls")),
# FrontPages urls
# path("", include("apps.theme.front_pages.urls")),
# FrontPages urls
# path("", include("apps.theme.mail.urls")),
# Chat urls
# path("", include("apps.theme.chat.urls")),
# Calendar urls
# path("", include("apps.theme.my_calendar.urls")),
# Kanban urls
# path("", include("apps.theme.kanban.urls")),
# eCommerce urls
# path("", include("apps.theme.ecommerce.urls")),
# Academy urls
# path("", include("apps.theme.academy.urls")),
# Logistics urls
# path("", include("apps.theme.logistics.urls")),
# Invoice urls
# path("", include("apps.theme.invoice.urls")),
# User urls
# path("", include("apps.theme.users.urls")),
# Access urls
# path("", include("apps.theme.access.urls")),
# Pages urls
# path("", include("apps.theme.pages.urls")),
# Auth urls
# path("", include("apps.theme.authentication.urls")),
# Wizard urls
# path("", include("apps.theme.wizard_examples.urls")),
# ModalExample urls
# path("", include("apps.theme.modal_examples.urls")),
# Card urls
# path("", include("apps.theme.cards.urls")),
# UI urls
# path("", include("apps.theme.ui.urls")),
# Extended UI urls
# path("", include("apps.theme.extended_ui.urls")),
# Icons urls
# path("", include("apps.theme.icons.urls")),
# Forms urls
# path("", include("apps.theme.forms.urls")),
# FormLayouts urls
# path("", include("apps.theme.form_layouts.urls")),
# FormWizard urls
# path("", include("apps.theme.form_wizard.urls")),
# FormValidation urls
# path("", include("apps.theme.form_validation.urls")),
# Tables urls
# path("", include("apps.theme.tables.urls")),
# Chart urls
# path("", include("apps.theme.charts.urls")),
# Map urls
# path("", include("apps.theme.maps.urls")),
# Auth urls
# path("", include("auth.urls")),
# Transaction urls
# path("", include("apps.theme.llm_transaction.urls")),

#####################################################################################################################
