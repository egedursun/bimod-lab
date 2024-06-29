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
from django.urls import include, path

from config import settings
from web_project.views import SystemView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth.urls")),
    path("organization/", include("apps.organization.urls", namespace="organization")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)


# Dashboard urls
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
# path("", include("apps.theme.transactions.urls")),
