#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: settings.py
#  Last Modified: 2024-12-13 03:19:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-13 03:24:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import os
import sys

from pathlib import (
    Path
)

from django.conf import (
    settings
)

from django.urls import (
    path
)

from django.utils.translation import (
    gettext_lazy as _
)

from dotenv import (
    load_dotenv
)

import sentry_sdk

from pydub import (
    AudioSegment
)

from .template import (
    TEMPLATE_CONFIG,
    THEME_LAYOUT_DIR,
    THEME_VARIABLES
)

############################################################################################################
# INITIAL SETUP
############################################################################################################

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

APPEND_SLASH = True

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default=''
)

############################################################################################################
# RUNTIME ENVIRONMENT
############################################################################################################

DEBUG = os.environ.get(
    "DEBUG",
    'True'
).lower() in ['true', 'yes', '1']

ENVIRONMENT = os.environ.get(
    "DJANGO_ENVIRONMENT",
    default="local"
)

BASE_URL = os.environ.get(
    "BASE_URL",
    default="http://127.0.0.1:8000"
)

############################################################################################################
# INSTALLED APPLICATIONS AND MIDDLEWARES
############################################################################################################

INSTALLED_APPS = [
    "jazzmin",

    "config.apps.MainAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    'django_extensions',
    "corsheaders",
    'cacheops',
    "channels",

    "apps.theme.dashboards",
    "apps.theme.layouts",
    "apps.theme.front_pages",
    "apps.theme.mail",
    "apps.theme.chat",
    "apps.theme.my_calendar",
    "apps.theme.kanban",
    "apps.theme.ecommerce",
    "apps.theme.academy",
    "apps.theme.logistics",
    "apps.theme.invoice",
    "apps.theme.users",
    "apps.theme.access",
    "apps.theme.pages",
    "apps.theme.authentication",
    "apps.theme.wizard_examples",
    "apps.theme.modal_examples",
    "apps.theme.cards",
    "apps.theme.ui",
    "apps.theme.extended_ui",
    "apps.theme.icons",
    "apps.theme.forms",
    "apps.theme.form_layouts",
    "apps.theme.form_wizard",
    "apps.theme.form_validation",
    "apps.theme.tables",
    "apps.theme.charts",
    "apps.theme.maps",
    "auth.apps.AuthConfig",
    "apps.theme.transactions",
    'django.contrib.sitemaps',

    "apps.audit_logs",
    "apps.landing",
    "apps.user_profile_management",
    "apps.user_settings",
    "apps.dashboard",
    "apps.assistants",
    "apps.leanmod",
    "apps.llm_core",
    "apps.llm_transaction",
    "apps.user_management",
    "apps.user_permissions",
    "apps.organization",
    "apps.multimodal_chat",
    "apps.export_assistants",
    "apps.export_leanmods",
    "apps.export_orchestrations",
    "apps.export_voidforger",
    "apps.datasource_sql",
    "apps.datasource_nosql",
    "apps.datasource_codebase",
    "apps.datasource_file_systems",
    "apps.datasource_media_storages",
    "apps.datasource_ml_models",
    "apps.datasource_browsers",
    "apps.starred_messages",
    "apps.memories",
    "apps.message_templates",
    "apps.datasource_knowledge_base",
    "apps.mm_functions",
    "apps.mm_apis",
    "apps.mm_scripts",
    "apps.mm_scheduled_jobs",
    "apps.mm_triggered_jobs",
    "apps.orchestrations",
    "apps.data_security",
    "apps.data_backups",
    "apps.brainstorms",
    "apps.video_generations",
    "apps.harmoniq",
    "apps.drafting",
    "apps.hadron_prime",
    "apps.smart_contracts",
    "apps.notifications",
    "apps.binexus",
    "apps.metakanban",
    "apps.metatempo",
    "apps.projects",
    "apps.ellma",
    "apps.sheetos",
    "apps.formica",
    "apps.slider",
    "apps.bmd_academy",
    "apps.integrations",
    "apps.meta_integrations",
    "apps.ml_model_store",
    "apps.knowledge_base_store",
    "apps.semantor",
    "apps.voidforger",
    "apps.quick_setup_helper",
    "apps.mobile_client",
    "apps.beamguard",
    "apps.datasource_website",
    "apps.sinaptera",
    "apps.browser_extensions",

    "apps.support_system",
    "apps.community_forum",
    "apps.blog_app",
    "apps.bimod_lite",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "web_project.language_middleware.DefaultLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "config.middleware.SessionTimeoutMiddleware",
    "config.middleware.AppendSlashMiddleware",
    "config.middleware.LoadingBarMiddleware",
    "config.middleware.ContentTypeMiddleware",
]

ROOT_URLCONF = "config.urls"

############################################################################################################
# ASYNCHRONOUS APPLICATION CONFIGURATIONS
############################################################################################################

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                (
                    '127.0.0.1',
                    6379
                )
            ]
        }
    }
}

############################################################################################################
# DATABASE CONFIGURATIONS
############################################################################################################

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv(
            'DB_HOST',
            'localhost'
        ),
        'PORT': os.getenv(
            'DB_PORT',
            ''
        ),
        'CONN_MAX_AGE': 3600 * 24 * 30,  # 30 days
    }
}

############################################################################################################
# AUTHENTICATION AND INTEGRITY
############################################################################################################

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "10.0.2.2",

    "www.bimod.io",
    "bimod.io",
    "dev.bimod.io",
    ".ngrok-free.app",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

ENCRYPTION_SALT = os.environ.get(
    "ENCRYPTION_SALT",
    default=""
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

############################################################################################################
# INTERNATIONALIZATION
############################################################################################################

LANGUAGES = [
    ("en", _("English")),
    # ("tr", _("Turkish")),
]

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

############################################################################################################
# STATIC FILES AND TEMPLATES
############################################################################################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.language_code",
                "config.context_processors.my_setting",
                "config.context_processors.get_cookie",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme"
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme"
            ],
        },
    },
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "src" / "assets"]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-central-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'config.custom_storages.MediaStorage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

############################################################################################################
# SERVICE LIMITS
############################################################################################################

MAX_ASSISTANT_EXPORTS_ORGANIZATION = int(
    os.environ.get(
        "MAX_ASSISTANT_EXPORTS_ORGANIZATION",
        default="5"
    )
)

MAX_LEANMODS_EXPORTS_ORGANIZATION = int(
    os.environ.get(
        "MAX_LEANMODS_EXPORTS_ORGANIZATION",
        default="5"
    )
)

MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION = int(
    os.environ.get(
        "MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION",
        default="5"
    )
)

MAX_VOIDFORGER_EXPORTS_ORGANIZATION = int(
    os.environ.get(
        "MAX_VOIDFORGER_EXPORTS_ORGANIZATION",
        default="5"
    )
)

MAX_BROWSERS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_BROWSERS_PER_ASSISTANT",
        default="3"
    )
)

MAX_CODE_BASES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_CODE_BASES_PER_ASSISTANT",
        default="3"
    )
)

MAX_WEBSITE_STORAGES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_WEBSITE_STORAGES_PER_ASSISTANT",
        default="3"
    )
)

MAX_WEBSITE_ITEMS_PER_STORAGE = int(
    os.environ.get(
        "MAX_WEBSITE_ITEMS_PER_STORAGE",
        default="10"
    )
)

MAX_FILE_SYSTEMS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_FILE_SYSTEMS_PER_ASSISTANT",
        default="3"
    )
)

MAX_KNOWLEDGE_BASES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_KNOWLEDGE_BASES_PER_ASSISTANT",
        default="3"
    )
)

MAX_MEDIA_STORAGES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_MEDIA_STORAGES_PER_ASSISTANT",
        default="20"
    )
)

MAX_ML_STORAGES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_ML_STORAGES_PER_ASSISTANT",
        default="3"
    )
)

MAX_ML_MODELS_PER_STORAGE = int(
    os.environ.get(
        "MAX_ML_MODELS_PER_STORAGE",
        default="5"
    )
)

MAX_NOSQL_DBS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_NOSQL_DBS_PER_ASSISTANT",
        default="3"
    )
)

MAX_NOSQL_QUERIES_PER_DB = int(
    os.environ.get(
        "MAX_NOSQL_QUERIES_PER_DB",
        default="5"
    )
)

MAX_SQL_DBS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_SQL_DBS_PER_ASSISTANT",
        default="3"
    )
)

MAX_SQL_QUERIES_PER_DB = int(
    os.environ.get(
        "MAX_SQL_QUERIES_PER_DB",
        default="5"
    )
)

MAX_VIDEO_GENERATORS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_VIDEO_GENERATORS_PER_ASSISTANT",
        default="3"
    )
)

MAX_PROJECTS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_PROJECTS_PER_ASSISTANT",
        default="3"
    )
)

MAX_TEAMS_PER_PROJECT = int(
    os.environ.get(
        "MAX_TEAMS_PER_PROJECT",
        default="5"
    )
)

MAX_HADRON_NODES_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_HADRON_NODES_PER_ASSISTANT",
        default="3"
    )
)

MAX_METAKANBAN_BOARDS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_METAKANBAN_BOARDS_PER_ASSISTANT",
        default="3"
    )
)

MAX_METATEMPO_TRACKERS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_METATEMPO_TRACKERS_PER_ASSISTANT",
        default="3"
    )
)

MAX_ORCHESTRATION_TRIGGERS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_ORCHESTRATION_TRIGGERS_PER_ASSISTANT",
        default="3"
    )
)

MAX_FUNCTIONS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_FUNCTIONS_PER_ASSISTANT",
        default="3"
    )
)

MAX_APIS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_APIS_PER_ASSISTANT",
        default="3"
    )
)

MAX_SCRIPTS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_SCRIPTS_PER_ASSISTANT",
        default="3"
    )
)

MAX_SCHEDULED_JOBS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_SCHEDULED_JOBS_PER_ASSISTANT",
        default="3"
    )
)

MAX_SCHEDULED_JOBS_PER_LEANMOD = int(
    os.environ.get(
        "MAX_SCHEDULED_JOBS_PER_LEANMOD",
        default="3"
    )
)

MAX_SCHEDULED_JOBS_PER_MAESTRO = int(
    os.environ.get(
        "MAX_SCHEDULED_JOBS_PER_MAESTRO",
        default="3"
    )
)

MAX_TRIGGERED_JOBS_PER_ASSISTANT = int(
    os.environ.get(
        "MAX_TRIGGERED_JOBS_PER_ASSISTANT",
        default="3"
    )
)

MAX_TRIGGERED_JOBS_PER_LEANMOD = int(
    os.environ.get(
        "MAX_TRIGGERED_JOBS_PER_LEANMOD",
        default="3"
    )
)

MAX_TRIGGERED_JOBS_PER_MAESTRO = int(
    os.environ.get(
        "MAX_TRIGGERED_JOBS_PER_MAESTRO",
        default="3"
    )
)

############################################################################################################
# SERVICE PROFIT MARGINS
############################################################################################################

__SERVICE_PROFIT_MARGIN = float(
    os.environ.get(
        "SERVICE_PROFIT_MARGIN",
        default="2.00"
    )
)

__SERVICE_TAX_RATE = float(
    os.environ.get(
        "SERVICE_TAX_RATE",
        default="0.18"
    )
)

############################################################################################################
# SERVICE DIRECT FEES
############################################################################################################

CONTEXT_MEMORY = os.environ.get(
    "CONTEXT_MEMORY",
    default="0"
)
CONTEXT_MEMORY_RETRIEVAL = os.environ.get(
    "CONTEXT_MEMORY_RETRIEVAL",
    default="0"
)
FILE_INTERPRETER = os.environ.get(
    "FILE_INTERPRETER",
    default="0"
)
IMAGE_INTERPRETER = os.environ.get(
    "IMAGE_INTERPRETER",
    default="0"
)
CODE_INTERPRETER = os.environ.get(
    "CODE_INTERPRETER",
    default="0"
)
DOWNLOAD_EXECUTOR = os.environ.get(
    "DOWNLOAD_EXECUTOR",
    default="0"
)

FILE_SYSTEMS_EXECUTOR = os.environ.get(
    "FILE_SYSTEMS_EXECUTOR",
    default="0"
)

KNOWLEDGE_BASE_EXECUTOR = os.environ.get(
    "KNOWLEDGE_BASE_EXECUTOR",
    default="0"
)

BROWSING_EXECUTOR = os.environ.get(
    "BROWSING_EXECUTOR",
    default="0"
)

CODE_REPOSITORY_EXECUTOR = os.environ.get(
    "CODE_REPOSITORY_EXECUTOR",
    default="0"
)

ML_MODEL_EXECUTOR = os.environ.get(
    "ML_MODEL_EXECUTOR",
    default="0"
)

INTERNAL_CUSTOM_FUNCTION_EXECUTOR = os.environ.get(
    "INTERNAL_CUSTOM_FUNCTION_EXECUTOR",
    default="0"
)

EXTERNAL_CUSTOM_FUNCTION_EXECUTOR = os.environ.get(
    "EXTERNAL_CUSTOM_FUNCTION_EXECUTOR",
    default="0"
)

INTERNAL_CUSTOM_API_EXECUTOR = os.environ.get(
    "INTERNAL_CUSTOM_API_EXECUTOR",
    default="0"
)

EXTERNAL_CUSTOM_API_EXECUTOR = os.environ.get(
    "EXTERNAL_CUSTOM_API_EXECUTOR",
    default="0"
)

INTERNAL_CUSTOM_SCRIPT_EXECUTOR = os.environ.get(
    "INTERNAL_CUSTOM_SCRIPT_EXECUTOR",
    default="0"
)

EXTERNAL_CUSTOM_SCRIPT_EXECUTOR = os.environ.get(
    "EXTERNAL_CUSTOM_SCRIPT_EXECUTOR",
    default="0"
)

SQL_READ_EXECUTOR = os.environ.get(
    "SQL_READ_EXECUTOR",
    default="0"
)

SQL_WRITE_EXECUTOR = os.environ.get(
    "SQL_WRITE_EXECUTOR",
    default="0"
)

NOSQL_READ_EXECUTOR = os.environ.get(
    "NOSQL_READ_EXECUTOR",
    default="0"
)

NOSQL_WRITE_EXECUTOR = os.environ.get(
    "NOSQL_WRITE_EXECUTOR",
    default="0"
)

SCHEDULED_JOB_EXECUTOR = os.environ.get(
    "SCHEDULED_JOB_EXECUTOR",
    default="0"
)

TRIGGERED_JOB_EXECUTOR = os.environ.get(
    "TRIGGERED_JOB_EXECUTOR",
    default="0"
)

IMAGE_GENERATOR = os.environ.get(
    "IMAGE_GENERATOR",
    default="0"
)

IMAGE_MODIFICATION = os.environ.get(
    "IMAGE_MODIFICATION",
    default="0"
)

IMAGE_VARIATION = os.environ.get(
    "IMAGE_VARIATION",
    default="0"
)

AUDIO_PROCESSING_STT = os.environ.get(
    "AUDIO_PROCESSING_STT",
    default="0"
)

AUDIO_PROCESSING_TTS = os.environ.get(
    "AUDIO_PROCESSING_TTS",
    default="0"
)

VIDEO_GENERATOR = os.environ.get(
    "VIDEO_GENERATOR",
    default="0"
)

REASONING = os.environ.get(
    "REASONING",
    default="0"
)

DRAFTING = os.environ.get(
    "DRAFTING",
    default="0"
)

SHEETOS = os.environ.get(
    "SHEETOS",
    default="0"
)

FORMICA = os.environ.get(
    "FORMICA",
    default="0"
)

SLIDER = os.environ.get(
    "SLIDER",
    default="0"
)

BROWSER_EXTENSION = os.environ.get(
    "BROWSER_EXTENSION",
    default="0"
)

HADRON_PRIME = os.environ.get(
    "HADRON_PRIME",
    default="0"
)

SMART_CONTRACT_CREATION = os.environ.get(
    "SMART_CONTRACT_CREATION",
    default="0"
)

BINEXUS = os.environ.get(
    "BINEXUS",
    default="0"
)

METAKANBAN = os.environ.get(
    "METAKANBAN",
    default="0"
)

MEETING_TRANSCRIPTION = os.environ.get(
    "MEETING_TRANSCRIPTION",
    default="0"
)

METATEMPO = os.environ.get(
    "METATEMPO",
    default="0"
)

ELLMA_SCRIPTING = os.environ.get(
    "ELLMA_SCRIPTING",
    default="0"
)

WEBSITE_STORAGE_EXECUTOR = os.environ.get(
    "WEBSITE_STORAGE_EXECUTOR",
    default="0"
)

COSTS_MAP = {
    "CONTEXT_MEMORY": float(CONTEXT_MEMORY),
    "CONTEXT_MEMORY_RETRIEVAL": float(CONTEXT_MEMORY_RETRIEVAL),
    "FILE_INTERPRETER": float(FILE_INTERPRETER),
    "IMAGE_INTERPRETER": float(IMAGE_INTERPRETER),
    "CODE_INTERPRETER": float(CODE_INTERPRETER),
    "DOWNLOAD_EXECUTOR": float(DOWNLOAD_EXECUTOR),

    "FILE_SYSTEMS_EXECUTOR": float(FILE_SYSTEMS_EXECUTOR),
    "KNOWLEDGE_BASE_EXECUTOR": float(KNOWLEDGE_BASE_EXECUTOR),
    "CODE_BASE_EXECUTOR": float(CODE_REPOSITORY_EXECUTOR),
    "BROWSING_EXECUTOR": float(BROWSING_EXECUTOR),
    "ML_MODEL_EXECUTOR": float(ML_MODEL_EXECUTOR),

    "INTERNAL_CUSTOM_FUNCTION_EXECUTOR": float(INTERNAL_CUSTOM_FUNCTION_EXECUTOR),
    "EXTERNAL_CUSTOM_FUNCTION_EXECUTOR": float(EXTERNAL_CUSTOM_FUNCTION_EXECUTOR),
    "INTERNAL_CUSTOM_API_EXECUTOR": float(INTERNAL_CUSTOM_API_EXECUTOR),
    "EXTERNAL_CUSTOM_API_EXECUTOR": float(EXTERNAL_CUSTOM_API_EXECUTOR),
    "INTERNAL_CUSTOM_SCRIPT_EXECUTOR": float(INTERNAL_CUSTOM_SCRIPT_EXECUTOR),

    "EXTERNAL_CUSTOM_SCRIPT_EXECUTOR": float(EXTERNAL_CUSTOM_SCRIPT_EXECUTOR),
    "SQL_READ_EXECUTOR": float(SQL_READ_EXECUTOR),
    "SQL_WRITE_EXECUTOR": float(SQL_WRITE_EXECUTOR),
    "NOSQL_READ_EXECUTOR": float(NOSQL_READ_EXECUTOR),
    "NOSQL_WRITE_EXECUTOR": float(NOSQL_WRITE_EXECUTOR),

    "SCHEDULED_JOB_EXECUTOR": float(SCHEDULED_JOB_EXECUTOR),
    "TRIGGERED_JOB_EXECUTOR": float(TRIGGERED_JOB_EXECUTOR),
    "IMAGE_GENERATOR": float(IMAGE_GENERATOR),
    "IMAGE_MODIFICATION": float(IMAGE_MODIFICATION),
    "IMAGE_VARIATION": float(IMAGE_VARIATION),

    "AUDIO_PROCESSING_STT": float(AUDIO_PROCESSING_STT),
    "AUDIO_PROCESSING_TTS": float(AUDIO_PROCESSING_TTS),
    "VIDEO_GENERATOR": float(VIDEO_GENERATOR),
    "REASONING": float(REASONING),
    "DRAFTING": float(DRAFTING),
    "SHEETOS": float(SHEETOS),

    "FORMICA": float(FORMICA),
    "SLIDER": float(SLIDER),
    "BROWSER_EXTENSION": float(BROWSER_EXTENSION),
    "HADRON_PRIME": float(HADRON_PRIME),
    "SMART_CONTRACT_CREATION": float(SMART_CONTRACT_CREATION),
    "BINEXUS": float(BINEXUS),
    "METAKANBAN": float(METAKANBAN),

    "MEETING_TRANSCRIPTION": float(MEETING_TRANSCRIPTION),
    "METATEMPO": float(METATEMPO),
    "ELLMA_SCRIPTING": float(ELLMA_SCRIPTING),
    "WEBSITE_STORAGE_EXECUTOR": float(WEBSITE_STORAGE_EXECUTOR),
}

############################################################################################################
# TEMPLATE SETTINGS
############################################################################################################

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

############################################################################################################
# EMAIL SETTINGS
############################################################################################################

# Change this if you need to send real emails for testing purposes.

FORCE_SMTP_USE = os.getenv(
    'FORCE_SMTP_USE',
    "false"
).lower() in ['true', '1', 'yes']

if ENVIRONMENT != "local" or FORCE_SMTP_USE:
    print("[settings.py] Email backend is set to SMTP for production environment (or forced SMTP in local).")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = os.getenv(
        'EMAIL_HOST',
        'smtp.gmail.com'
    )

    EMAIL_PORT = os.getenv(
        'EMAIL_PORT',
        587
    )

    EMAIL_USE_SSL = os.getenv(
        'EMAIL_USE_SSL',
        'False'
    ).lower() in [
                        'true',
                        '1',
                        'yes'
                    ]

    EMAIL_USE_TLS = os.getenv(
        'EMAIL_USE_TLS',
        'True'
    ).lower() in [
                        'true',
                        '1',
                        'yes'
                    ]

    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    DEFAULT_FROM_EMAIL = os.getenv(
        'DEFAULT_FROM_EMAIL',
        EMAIL_HOST_USER
    )

else:
    print("[settings.py] Email backend is set to CONSOLE for local environment.")
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

############################################################################################################
# LOGIN AND SESSION CONFIGURATIONS
############################################################################################################

DEFAULT_APPLICATION_ZOOM = int(
    os.environ.get(
        "DEFAULT_APPLICATION_ZOOM",
        default="100"
    )
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

LOGIN_URL = "/app/login/"
LOGOUT_REDIRECT_URL = "/app/login/"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5050",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000",

    "http://10.0.2.2:8000",
    "https://bimod.io",
    "https://dev.bimod.io",
    "https://www.bimod.io",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5050",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000",

    "http://10.0.2.2:8000",
    "https://bimod.io",
    "https://dev.bimod.io",
    "https://www.bimod.io",
]

CORS_ALLOW_CREDENTIALS = True

SUFFIX_ANY = "*"

EXCLUDED_PAGES = [
    "/",
    "/admin/*",
    "/app/login/*",
    "/app/logout/*",
    "/app/register/*",

    "/app/verify_email_page/*",
    "/app/verify/email/*",
    "/app/verify_email/*",
    "/app/send_verification/*",

    "/app/forgot_password/*",
    "/app/reset_password/*",
    "/app/multimodal_chat/tts/chat/message/*"
    "/contact-form-submit/*",

    "/electron_copilot_releases/*",
    "/fermion_copilot_releases/*",
    "/docs/*",
    "/faq/*",
    "/bmd_academy/*",

    "/app/blog_app/*",
    "/not_accredited/*",
    "/bimod_endeavours/*",
    "/integration_to_organizations/*",

    "/app/export_assistants/exported/*",
    "/app/export_assistants/health/*",
    "/app/export_leanmods/exported/*",
    "/app/export_leanmods/health/*",

    "/app/export_orchestrations/exported/*",
    "/app/export_orchestrations/health/*",
    "/app/export_voidforger/exported/*",
    "/app/export_voidforger/health/*",
    "/app/export_voidforger/status/*",

    "/app/export_voidforger/manual_trigger/*",
    "/app/hadron_prime/hadron_node/activate/*",
    "/app/hadron_prime/hadron_node/speak/*",
    "/app/metakanban/meeting/recording/delivery/*",

    "/app/metatempo/tempo/screenshot/delivery/*",
    "/app/metatempo/tempo/connection/config/*",
    "/app/drafting/public/*",
    "/app/sheetos/public/*",

    "/app/formica/public/*",
    "/app/slider/public/*",
    "/app/browser_extensions/public/*",
    "/app/mm_triggered_jobs/api/v1/webhook/*",

    "/app/mm_triggered_jobs/orchestration/api/v1/webhook/*",
    "/app/mobile_client/*"
]

############################################################################################################
# DISPATCHED ENDPOINTS
############################################################################################################

DESIGN_DOCS_ROUTE = 'dev/design/'

EXPORT_API_BASE_URL = "app/export_assistants/exported/assistants"
EXPORT_API_HEALTH_BASE_URL = "app/export_assistants/health/assistants"

EXPORT_LEANMOD_API_BASE_URL = "app/export_leanmods/exported/leanmod_assistants"
EXPORT_LEANMOD_API_HEALTH_BASE_URL = "app/export_leanmods/health/leanmod_assistants"

EXPORT_ORCHESTRATION_API_BASE_URL = "app/export_orchestrations/exported/orchestrator_assistants"
EXPORT_ORCHESTRATION_API_HEALTH_BASE_URL = "app/export_orchestrations/health/orchestrator_assistants"

EXPORT_VOIDFORGER_API_BASE_URL = "app/export_voidforger/exported/voidforger_assistants"
EXPORT_VOIDFORGER_API_HEALTH_BASE_URL = "app/export_voidforger/health/voidforger_assistants"

LEAN_BASE_URL = BASE_URL.split("://")[-1].split(":")[0]

############################################################################################################
# LOGGING, QUEUEING AND MESSAGE BROKER CONFIGURATIONS
############################################################################################################

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = [
    'json'
]

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CLEAN_DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}', 'style': '{'
        },
        'simple': {
            'format': '{levelname} {message}', 'style': '{'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(
                BASE_DIR,
                'django_debug.log'
            ),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'file'
            ],
            'level': 'DEBUG',
            'propagate': True
        }
    },
}

if ENVIRONMENT != "local":
    sentry_sdk.init(
        dsn=os.getenv(
            "SENTRY_DSN",
            default=""
        ),
        traces_sample_rate=float(
            os.getenv(
                "SENTRY_TRACES_SAMPLE_RATE",
                default=0.1
            )
        ),
        profiles_sample_rate=float(
            os.getenv(
                "SENTRY_PROFILES_SAMPLE_RATE",
                default=0.1
            )
        ),
    )

else:
    print("[settings.py] Sentry SDK is intentionally disabled in local environment, skipping the initialization.")
    pass

############################################################################################################
# TESTING MODE CONFIGURATIONS
############################################################################################################

TESTING = sys.argv[0].endswith(
    "pytest"
)

print("[settings.py] Testing Mode: ", TESTING)

if TESTING:
    print("[settings.py] Integration Testing Mode is activated...")
    pass

else:
    print("[settings.py] Integration Testing Mode is deactive, deploy mode is activated...")
    pass

############################################################################################################
# PROMOTIONS
############################################################################################################

NEW_USER_FREE_CREDITS = int(
    os.environ.get(
        "NEW_USER_FREE_CREDITS",
        default="0"
    )
)

BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_1 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_1",
        default="1000"
    )
)

BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_2 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_2",
        default="5000"
    )
)

BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_3 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_3",
        default="10000"
    )
)

BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_4 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_THRESHOLD__SPECIFIER_4",
        default="50000"
    )
)

BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_1000_LT_5000 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_1000_LT_5000",
        default="0"
    )
)

BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_5000_LT_10000 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_5000_LT_10000",
        default="0"
    )
)

BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_10000_LT_50000 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_10000_LT_50000",
        default="0"
    )
)

BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_50000 = int(
    os.environ.get(
        "BALANCE_ADDITION_BONUS_PERCENTAGE__GTE_50000",
        default="0"
    )
)

############################################################################################################
# THIRD PARTY API KEYS AND SECRETS
############################################################################################################

INFURA_API_KEY = os.environ.get(
    "INFURA_API_KEY",
    default=""
)

INFURA_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"

VOSK_MODEL_PATH = os.environ.get(
    "VOSK_MODEL_PATH",
    default="ml_models/vosk-model-en-us-0.22-lgraph"
)

INTERNAL_OPENAI_API_KEY = os.environ.get(
    "INTERNAL_OPENAI_API_KEY",
    default=""
)

INTERNAL_REPLICATE_API_KEY = os.environ.get(
    "INTERNAL_REPLICATE_API_KEY",
    default=""
)

INTERNAL_LLM_MODEL_NAME = os.environ.get(
    "INTERNAL_LLM_MODEL_NAME",
    default=""
)

############################################################################################################
# ADMIN PANEL CONFIGURATIONS
############################################################################################################

JAZZMIN_SETTINGS = {
    "site_title": "BimodLab Admin",
    "site_header": "BimodLab Admin",
    "site_brand": "BimodLab Admin",
    "welcome_sign": "Primary Staff Control Panel",
    "copyright": "BMD Autonomous Holdings. All rights reserved.",
    "show_sidebar": True,
}

#####################################################################################################################
# FIXTURE DEPLOYMENT ATTEMPTS CONFIGURATIONS
#####################################################################################################################

ATTEMPT_FIXTURE_DEPLOYMENT = False

SKIP_FIXTURE_EMBEDDINGS = True

if ATTEMPT_FIXTURE_DEPLOYMENT is True:
    print("[settings.py] [V] Attempting to deploy the database fixtures...")

else:
    print("[settings.py] [X] Skipping the database fixtures deployment...")

if SKIP_FIXTURE_EMBEDDINGS is True:
    print("[settings.py] [X] Skipping the database vector embeddings deployment...")

else:
    print("[settings.py] [V] Attempting to deploy the database vector embeddings...")

#####################################################################################################################
