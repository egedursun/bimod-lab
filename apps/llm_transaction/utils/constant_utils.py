from config import settings

ENCODING_ENGINES = [
    ("cl100k_base", "cl100k_base"),
    ("p50k_base", "p50k_base"),
    ("r50k_base", "r50k_base"),
]
TRANSACTION_TYPE_ROLES = [
    ("user", "User"),
    ("assistant", "Assistant"),
    ("system", "System"),
]
TRANSACTION_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("generation", "Generation"),
    ("sql-read", "SQL Read"),
    ("sql-write", "SQL Write"),
    ("store-memory", "Store Memory"),
    ("interpret-code", "Interpret Code"),
    ("download-file", "Download File"),
    ("file-system-commands", "File System Commands"),
    ("knowledge-base-search", "Knowledge Base Search"),
    ("retrieve-memory", "Retrieve Memory"),
    ("ml-model-prediction", "ML Model Prediction"),
    ("internal-function-execution", "Internal Function Execution"),
    ("external-function-execution", "External Function Execution"),
    ("interpret-file", "Interpret File"),
    ("interpret-image", "Interpret Image"),
]


class TransactionTypeRolesNames:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TransactionSourcesNames:
    APP = "app"
    API = "api"
    ############################
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
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

    @staticmethod
    def as_list():
        return [
            TransactionSourcesNames.APP,
            TransactionSourcesNames.API,
            TransactionSourcesNames.GENERATION,
            TransactionSourcesNames.SQL_READ,
            TransactionSourcesNames.SQL_WRITE,
            TransactionSourcesNames.STORE_MEMORY,
            TransactionSourcesNames.INTERPRET_CODE,
            TransactionSourcesNames.UPLOAD_FILE,
            TransactionSourcesNames.DOWNLOAD_FILE,
            TransactionSourcesNames.FILE_SYSTEM_COMMANDS,
            TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH,
            TransactionSourcesNames.RETRIEVE_MEMORY,
            TransactionSourcesNames.CODE_BASE_SEARCH,
            TransactionSourcesNames.ML_MODEL_PREDICTION,
            TransactionSourcesNames.BROWSING,
            TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            TransactionSourcesNames.EXTERNAL_API_EXECUTION,
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.INTERPRET_FILE,
            TransactionSourcesNames.INTERPRET_IMAGE,
            TransactionSourcesNames.SCHEDULED_JOB_EXECUTION,
            TransactionSourcesNames.TRIGGER_JOB_EXECUTION,
            TransactionSourcesNames.GENERATE_IMAGE,
            TransactionSourcesNames.MODIFY_IMAGE,
            TransactionSourcesNames.VARIATE_IMAGE,
        ]


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


PAYMENT_METHODS = [
    ("credit-card", "Credit Card"),
    ("internal-transfer", "Internal Transfer"),
]


class PaymentMethodsNames:
    CREDIT_CARD = "credit-card"
    INTERNAL_TRANSFER = "internal-transfer"

    @staticmethod
    def as_list():
        return [
            PaymentMethodsNames.CREDIT_CARD,
            PaymentMethodsNames.INTERNAL_TRANSFER,
        ]


FILTER_TYPES = [
    ('seconds', 'seconds'),
    ('minutes', 'minutes'),
    ('hours', 'hours'),
    ('days', 'days'),
    ('weeks', 'weeks'),
    ('months', 'months'),
    ('years', 'years'),
]
DEFAULT_PAGINATION_SIZE_LIST_TRANSACTIONS = 5
MAXIMUM_TOTAL_PAGES = 50


class LLMCostsPerMillionTokens:
    OPENAI_GPT_COSTS = {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
    }


SERVICE_PROFIT_MARGIN = settings.__SERVICE_PROFIT_MARGIN
VAT_TAX_RATE = settings.__SERVICE_TAX_RATE
