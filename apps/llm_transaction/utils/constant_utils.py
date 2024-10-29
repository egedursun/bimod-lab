#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from config import settings

TOKENIZATION_ENCODING_ENGINES = [
    ("cl100k_base", "cl100k_base"),
    ("p50k_base", "p50k_base"),
    ("r50k_base", "r50k_base"),
]

LLM_TRANSACTION_ROLES_FOR_TYPE = [
    ("user", "User"),
    ("assistant", "Assistant"),
    ("system", "System"),
]

SOURCES_OF_LLM_TRANSACTION = [
    ("app", "Application"),
    ("api", "API"),
    ("generation", "Generation"),
    ("sql-read", "SQL Read"),
    ("sql-write", "SQL Write"),
    ("nosql-read", "NoSQL Read"),
    ("nosql-write", "NoSQL Write"),
    ("store-memory", "Store Memory"),
    ("interpret-code", "Interpret Code"),
    ("reasoning", "Reasoning"),
    ("upload-file", "Upload File"),
    ("download-file", "Download File"),
    ("file-system-commands", "File System Commands"),
    ("knowledge-base-search", "Knowledge Base Search"),
    ("code-base-search", "Code Base Search"),
    ("retrieve-memory", "Retrieve Memory"),
    ("ml-model-prediction", "ML Model Prediction"),
    ("browsing", "Browsing"),
    ("internal-function-execution", "Internal Function Execution"),
    ("external-function-execution", "External Function Execution"),
    ("internal-api-execution", "Internal API Execution"),
    ("external-api-execution", "External API Execution"),
    ("internal-script-retrieval", "Internal Script Retrieval"),
    ("external-script-retrieval", "External Script Retrieval"),
    ("interpret-file", "Interpret File"),
    ("interpret-image", "Interpret Image"),
    ("scheduled-job-execution", "Scheduled Job Execution"),
    ("trigger-job-execution", "Trigger Job Execution"),
    ("generate-image", "Generate Image"),
    ("modify-image", "Modify Image"),
    ("variate-image", "Variate Image"),
    ("audio-processing-stt", "Audio Processing STT"),
    ("audio-processing-tts", "Audio Processing TTS"),
    ("brainstorming", "Brainstorming"),
    ("generate-video", "Generate Video"),
    ("drafting", "Drafting"),
    ("hadron-prime", "Hadron Prime"),
    ("smart-contract-creation", "Smart Contract Creation"),
    ("binexus", "Binexus"),
    ("metakanban", "MetaKanban"),
    ("meeting-transcription", "Meeting Transcription"),
    ("metatempo", "MetaTempo"),
]


class LLMTransactionRolesForTypeNames:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class LLMTransactionSourcesTypesNames:
    APP = "app"
    API = "api"
    ############################
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    NOSQL_READ = "nosql-read"
    NOSQL_WRITE = "nosql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
    REASONING = "reasoning"
    UPLOAD_FILE = "upload-file"
    DOWNLOAD_FILE = "download-file"
    FILE_SYSTEM_COMMANDS = "file-system-commands"
    KNOWLEDGE_BASE_SEARCH = "knowledge-base-search"
    CODE_BASE_SEARCH = "code-base-search"
    RETRIEVE_MEMORY = "retrieve-memory"
    ML_MODEL_PREDICTION = "ml-model-prediction"
    BROWSING = "browsing"
    INTERNAL_FUNCTION_EXECUTION = "internal-function-execution"
    EXTERNAL_FUNCTION_EXECUTION = "external-function-execution"
    INTERNAL_API_EXECUTION = "internal-api-execution"
    EXTERNAL_API_EXECUTION = "external-api-execution"
    INTERNAL_SCRIPT_RETRIEVAL = "internal-script-retrieval"
    EXTERNAL_SCRIPT_RETRIEVAL = "external-script-retrieval"
    INTERPRET_FILE = "interpret-file"
    INTERPRET_IMAGE = "interpret-image"
    SCHEDULED_JOB_EXECUTION = "scheduled-job-execution"
    TRIGGER_JOB_EXECUTION = "trigger-job-execution"
    GENERATE_IMAGE = "generate-image"
    MODIFY_IMAGE = "modify-image"
    VARIATE_IMAGE = "variate-image"
    AUDIO_PROCESSING_STT = "audio-processing-stt"
    AUDIO_PROCESSING_TTS = "audio-processing-tts"
    BRAINSTORMING = "brainstorming"
    GENERATE_VIDEO = "generate-video"
    DRAFTING = "drafting"
    HADRON_PRIME = "hadron-prime"
    SMART_CONTRACT_CREATION = "smart-contract-creation"
    BINEXUS = "binexus"
    METAKANBAN = "metakanban"
    MEETING_TRANSCRIPTION = "meeting-transcription"
    METATEMPO = "metatempo"

    @staticmethod
    def as_list():
        return [
            LLMTransactionSourcesTypesNames.APP,
            LLMTransactionSourcesTypesNames.API,
            LLMTransactionSourcesTypesNames.GENERATION,
            LLMTransactionSourcesTypesNames.SQL_READ,
            LLMTransactionSourcesTypesNames.SQL_WRITE,
            LLMTransactionSourcesTypesNames.NOSQL_READ,
            LLMTransactionSourcesTypesNames.NOSQL_WRITE,
            LLMTransactionSourcesTypesNames.STORE_MEMORY,
            LLMTransactionSourcesTypesNames.INTERPRET_CODE,
            LLMTransactionSourcesTypesNames.UPLOAD_FILE,
            LLMTransactionSourcesTypesNames.DOWNLOAD_FILE,
            LLMTransactionSourcesTypesNames.FILE_SYSTEM_COMMANDS,
            LLMTransactionSourcesTypesNames.KNOWLEDGE_BASE_SEARCH,
            LLMTransactionSourcesTypesNames.RETRIEVE_MEMORY,
            LLMTransactionSourcesTypesNames.CODE_BASE_SEARCH,
            LLMTransactionSourcesTypesNames.ML_MODEL_PREDICTION,
            LLMTransactionSourcesTypesNames.BROWSING,
            LLMTransactionSourcesTypesNames.INTERNAL_FUNCTION_EXECUTION,
            LLMTransactionSourcesTypesNames.EXTERNAL_FUNCTION_EXECUTION,
            LLMTransactionSourcesTypesNames.INTERNAL_API_EXECUTION,
            LLMTransactionSourcesTypesNames.EXTERNAL_API_EXECUTION,
            LLMTransactionSourcesTypesNames.INTERNAL_SCRIPT_RETRIEVAL,
            LLMTransactionSourcesTypesNames.EXTERNAL_SCRIPT_RETRIEVAL,
            LLMTransactionSourcesTypesNames.INTERPRET_FILE,
            LLMTransactionSourcesTypesNames.INTERPRET_IMAGE,
            LLMTransactionSourcesTypesNames.SCHEDULED_JOB_EXECUTION,
            LLMTransactionSourcesTypesNames.TRIGGER_JOB_EXECUTION,
            LLMTransactionSourcesTypesNames.GENERATE_IMAGE,
            LLMTransactionSourcesTypesNames.MODIFY_IMAGE,
            LLMTransactionSourcesTypesNames.VARIATE_IMAGE,
            LLMTransactionSourcesTypesNames.AUDIO_PROCESSING_STT,
            LLMTransactionSourcesTypesNames.AUDIO_PROCESSING_TTS,
            LLMTransactionSourcesTypesNames.BRAINSTORMING,
            LLMTransactionSourcesTypesNames.GENERATE_VIDEO,
            LLMTransactionSourcesTypesNames.REASONING,
            LLMTransactionSourcesTypesNames.DRAFTING,
            LLMTransactionSourcesTypesNames.HADRON_PRIME,
            LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION,
            LLMTransactionSourcesTypesNames.BINEXUS,
            LLMTransactionSourcesTypesNames.METAKANBAN,
            LLMTransactionSourcesTypesNames.MEETING_TRANSCRIPTION,
            LLMTransactionSourcesTypesNames.METATEMPO,
        ]


"""
    ================================================================================================================
    **IMPORTANT NOTE:**
    ================================================================================================================

    **IF YOU ARE ADDING A NEW TOOL THAT IS ASSOCIATED WITH A "COST",**

    DON'T FORGET TO UPDATE:

    - TOOL_NAME_TO_COST_MAP
        (apps/core/internal_cost_manager/costs_map.py)

    ---

    If NO COST is associated with the tool, DON'T update the `TOOL_NAME_TO_COST_MAP`.

    ================================================================================================================
"""


INVOICE_TYPES = [
    ("auto-top-up", "Auto Top-Up"),
    ("top-up", "Top-Up"),
    ("gift-credits", "Gift Credits"),
    ("transferred-credits", "Transferred Credits"),
]


class InvoiceTypesNames:
    AUTO_TOP_UP = "auto-top-up"
    TOP_UP = "top-up"
    GIFT_CREDITS = "gift-credits"
    TRANSFERRED_CREDITS = "transferred-credits"

    @staticmethod
    def as_list():
        return [
            InvoiceTypesNames.AUTO_TOP_UP,
            InvoiceTypesNames.TOP_UP,
            InvoiceTypesNames.GIFT_CREDITS,
            InvoiceTypesNames.TRANSFERRED_CREDITS,
        ]


ACCEPTED_METHODS_OF_PAYMENT = [
    ("credit-card", "Credit Card"),
    ("internal-transfer", "Internal Transfer"),
    ("direct-sales", "Direct Sales"),
]


class AcceptedMethodsOfPaymentNames:
    CREDIT_CARD = "credit-card"
    INTERNAL_TRANSFER = "internal-transfer"
    DIRECT_SALES = "direct-sales"

    @staticmethod
    def as_list():
        return [
            AcceptedMethodsOfPaymentNames.CREDIT_CARD,
            AcceptedMethodsOfPaymentNames.INTERNAL_TRANSFER,
            AcceptedMethodsOfPaymentNames.DIRECT_SALES,
        ]


INTERNAL_TIME_FILTER_TYPES = [
    ('seconds', 'seconds'),
    ('minutes', 'minutes'),
    ('hours', 'hours'),
    ('days', 'days'),
    ('weeks', 'weeks'),
    ('months', 'months'),
    ('years', 'years'),
]


TXS_PAGINATION_ITEMS_PER_PAGE = 5
MAXIMUM_PAGES_POSSIBLE_TO_SHOW = 50


class LLMCostsPerMillionTokens:
    OPENAI_GPT_COSTS = {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
    }


INTERNAL_PROFIT_MARGIN_FOR_LLM = settings.__SERVICE_PROFIT_MARGIN
VALUE_ADDED_TAX_PERCENTAGE = settings.__SERVICE_TAX_RATE

AUTO_TOP_UP_ADMIN_LIST = [
    "organization",
    "on_balance_threshold_trigger",
    "on_interval_by_days_trigger",
    "balance_lower_trigger_threshold_value",
    "addition_on_balance_threshold_trigger"
]

INVOICE_ADMIN_LIST = [
    "organization",
    "responsible_user",
    "transaction_type",
    "amount_added",
    "payment_method",
    "transaction_date",
    "invoice_number",
    "barcode_image",
    "transaction_paper",
]

TRANSACTION_ADMIN_LIST = [
    "responsible_user", "responsible_assistant", "organization", "model", "transaction_source", "total_cost",
    "created_at"
]
TRANSACTION_ADMIN_FILTER = ["responsible_user", "responsible_assistant", "transaction_source", "organization", "model",
                            "created_at"]
TRANSACTION_ADMIN_SEARCH = ["organization__name", "model__nickname"]

BALANCE_SNAPSHOT_ADMIN_LIST = ["organization", "balance", "created_at"]
