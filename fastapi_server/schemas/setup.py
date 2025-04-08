#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: quick_setup.py
#  Last Modified: 2025-02-01 22:33:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 22:33:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from enum import Enum
from pydantic import BaseModel


class ScheduledJobFrequencies(str, Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class SQLDatabaseTypes(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    ORACLE = "oracle"
    MSSQL = "mssql"
    MARIADB = "mariadb"


class NoSQLDatabaseTypes(str, Enum):
    MONGODB = "mongodb"
    COUCHBASE = "couchbase"
    NEO4J = "neo4j"
    ELASTICSEARCH = "elasticsearch"
    REDIS = "redis"
    WEAVIATE = "weaviate"


class FileSystemTypes(str, Enum):
    LINUX = "linux"
    MACOSX = "macosx"


class UserAuthorizationLevels(str, Enum):
    BASIC = "basic"
    MEDIUM = "medium"
    HIGH = "high"


class OverallLogIntervalTypes(str, Enum):
    DAILY = "daily"
    BIDAILY = "bidaily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class MemberLogIntervalTypes(str, Enum):
    X12PERHOUR = "x12perhour"
    X6PERHOUR = "x6perhour"
    X4PERHOUR = "x4perhour"
    X3PERHOUR = "x3perhour"
    X2PERHOUR = "x2perhour"
    HOUR = "hour"
    EVERY2HOUR = "every2hour"
    EVERY4HOUR = "every4hour"


class MetaTempoTrackingDays(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class ContextOverflowStrategyNames(str, Enum):
    FORGET = "forget"
    STOP = "stop"
    VECTORIZE = "vectorize"


class MultiStepReasoningChoices(str, Enum):
    NONE = "none"
    COST_EFFECTIVE = "cost_effective"
    HIGH_PERFORMANCE = "high_performance"


class AssistantMemoryScopes(str, Enum):
    ORGANIZATION = "organization"
    ASSISTANT = "assistant"
    USER = "user"


class BlockchainTypes(str, Enum):
    ETHEREUM = "ethereum"


class QuickSetup__ProjectTeam(BaseModel):
    team_name: str
    team_description: str = ""


class QuickSetup__MetaTempoTracker(BaseModel):
    tracking_active: bool = True
    overall_log_intervals: OverallLogIntervalTypes = OverallLogIntervalTypes.DAILY
    member_log_intervals: MemberLogIntervalTypes = MemberLogIntervalTypes.X12PERHOUR
    tracking_days: list[MetaTempoTrackingDays] = [
        MetaTempoTrackingDays.MONDAY,
        MetaTempoTrackingDays.TUESDAY,
        MetaTempoTrackingDays.WEDNESDAY,
        MetaTempoTrackingDays.THURSDAY,
        MetaTempoTrackingDays.FRIDAY
    ]
    tracking_start_time: str = "08:00"
    tracking_end_time: str = "17:00"
    optional_instructions: str = ""
    manager_assistant_names: list[str] = None


class QuickSetup__MetaKanbanBoard(BaseModel):
    board_title: str
    board_description: str = ""
    metatempo_tracker: QuickSetup__MetaTempoTracker = None
    manager_assistant_names: list[str] = None


class QuickSetup__Project(BaseModel):
    project_name: str
    project_description: str = ""
    project_department: str = ""
    project_status: str = ""
    project_priority: str = ""
    project_risk_level: str = ""
    project_goals: str = ""
    project_constraints: str = ""
    project_stakeholders: str = ""
    project_start_date: str = ""
    project_end_date: str = ""
    project_budget: float = 0.00
    project_teams: list[QuickSetup__ProjectTeam] = None
    project_boards: list[QuickSetup__MetaKanbanBoard] = None


class QuickSetup__BrainstormingSession(BaseModel):
    session_name: str
    topic_definition: str
    topic_constraints: str = ""


class QuickSetup__Organization(BaseModel):
    name: str
    description: str
    mission: str = ""
    vision: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    postal_code: str = ""
    industry: str = ""
    projects: list[QuickSetup__Project] = None


class QuickSetup__LLMModel(BaseModel):
    nickname: str
    description: str = ""
    temperature: float = 0.25
    max_tokens: int = 4096
    top_p: float = 1.00
    stop_sequences: list[str] = None
    frequency_penalty: float = 0.00
    presence_penalty: float = 0.00


class QuickSetup__Assistant(BaseModel):
    use_case_descriptions: list[str]


class QuickSetup__NERPolicy__Entities(BaseModel):
    encrypt_PERSON: bool = False
    encrypt_ORG: bool = False
    encrypt_NORP: bool = False
    encrypt_FAC: bool = False
    encrypt_GPE: bool = False
    encrypt_LOC: bool = False
    encrypt_PRODUCT: bool = False
    encrypt_EVENT: bool = False
    encrypt_WORK_OF_ART: bool = False
    encrypt_LAW: bool = False
    encrypt_LANGUAGE: bool = False
    encrypt_DATE: bool = False
    encrypt_TIME: bool = False
    encrypt_PERCENT: bool = False
    encrypt_MONEY: bool = False
    encrypt_QUANTITY: bool = False
    encrypt_ORDINAL: bool = False
    encrypt_CARDINAL: bool = False


class QuickSetup__NERPolicy(BaseModel):
    name: str
    description: str = ""
    language: str = "en"
    entities: QuickSetup__NERPolicy__Entities


class QuickSetup__GlossaryItem(BaseModel):
    term_name: str
    term_definition: str


class QuickSetup__Assistant__Manual(BaseModel):
    name: str
    instructions: str = "You are a helpful assistant."
    description: str = ""
    ner_policy: QuickSetup__NERPolicy = None
    response_template: str = ""
    audience: str = "Standard"
    tone: str = "Standard"
    time_and_spatial_awareness: bool = True
    image_generation_and_manipulation: bool = True
    beamguard_data_protection: bool = True
    max_retries: int = 3
    max_tool_retries: int = 3
    max_pipelines: int = 3
    max_message_memory: int = 25
    response_language: str = "auto"
    context_overflow_management_strategy: ContextOverflowStrategyNames = ContextOverflowStrategyNames.VECTORIZE
    multistep_reasoning: MultiStepReasoningChoices = MultiStepReasoningChoices.HIGH_PERFORMANCE
    glossary: list[QuickSetup__GlossaryItem] = None
    related_project_names: list[str] = None


class QuickSetup__Assistant__Wrapper(BaseModel):
    auto_infer: QuickSetup__Assistant = None
    custom: QuickSetup__Assistant__Manual = None


class QuickSetup__Memory(BaseModel):
    scope: AssistantMemoryScopes = AssistantMemoryScopes.ASSISTANT
    memory_content: str = ""
    assistant_name: str = None


class QuickSetup__Memories(BaseModel):
    memories: list[QuickSetup__Memory] = None


class QuickSetup__MessageTemplate(BaseModel):
    template_text: str


class QuickSetup__StepGuideList(BaseModel):
    step_description: str


class QuickSetup__ScheduledJob(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    minutes: str = "*"
    hours: str = "0"
    days_of_week: str = "1, 2, 3, 4, 5"
    days_of_month: str = "1"
    months_of_year: str = "*"
    maximum_runs: int = 100
    assistant_names: list[str]


class QuickSetup__ScheduledJob__Lean(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    minutes: str = "*"
    hours: str = "0"
    days_of_week: str = "1, 2, 3, 4, 5"
    days_of_month: str = "1"
    months_of_year: str = "*"
    maximum_runs: int = 100
    leanmod_names: list[str]


class QuickSetup__ScheduledJob__Meta(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    minutes: str = "*"
    hours: str = "0"
    days_of_week: str = "1, 2, 3, 4, 5"
    days_of_month: str = "1"
    months_of_year: str = "*"
    maximum_runs: int = 100
    orchestrator_names: list[str]


class QuickSetup__ScheduledJob__Wrapper(BaseModel):
    assistants: list[QuickSetup__ScheduledJob]
    leanmods: list[QuickSetup__ScheduledJob__Lean]
    orchestrators: list[QuickSetup__ScheduledJob__Meta]


class QuickSetup__TriggeredJob(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    trigger_source_url: str = ""
    trigger_explanation: str = ""
    maximum_runs: int = 100
    assistant_names: list[str] = ""


class QuickSetup__TriggeredJob__Lean(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    trigger_source_url: str = ""
    trigger_explanation: str = ""
    maximum_runs: int = 100
    leanmod_names: list[str] = ""


class QuickSetup__TriggeredJob__Meta(BaseModel):
    name: str
    description: str = ""
    step_guide: list[QuickSetup__StepGuideList] = None
    trigger_source_url: str = ""
    trigger_explanation: str = ""
    maximum_runs: int = 100
    orchestrator_names: list[str] = ""


class QuickSetup__TriggeredJob__Wrapper(BaseModel):
    assistants: list[QuickSetup__TriggeredJob]
    leanmods: list[QuickSetup__TriggeredJob__Lean]
    orchestrators: list[QuickSetup__TriggeredJob__Meta]


class CustomFunctionParamTypes(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    TUPLE = "tuple"
    LIST = "list"
    DICT = "dict"


class CustomToolCategories(str, Enum):
    DATA = "data"
    AIML = "ai-ml"
    MEDIA = "media"
    AUTOMATION = "automation"
    API = "api"
    FINANCE = "finance"
    COMMERCE = "commerce"
    SUPPORT = "support"
    SOCIAL = "social"
    IOT = "iot"
    HEALTH = "health"
    LEGAL = "legal"
    EDUCATION = "education"
    TRAVEL = "travel"
    SECURITY = "security"
    PRIVACY = "privacy"
    ENTERTAINMENT = "entertainment"
    PRODUCTIVITY = "productivity"
    UTILITIES = "utilities"
    MISCELLANEOUS = "miscellaneous"


class QuickSetup__CustomFunctions__PackageDefinition(BaseModel):
    package_name: str
    package_version: str


class QuickSetup__CustomFunctions__InputField(BaseModel):
    name: str
    description: str
    type: CustomFunctionParamTypes = CustomFunctionParamTypes.STRING
    is_required: bool = False


class QuickSetup__CustomFunctions__OutputField(BaseModel):
    name: str
    description: str
    type: CustomFunctionParamTypes = CustomFunctionParamTypes.STRING


class QuickSetup__CustomFunction(BaseModel):
    nickname: str
    description: str = ""
    packages_and_versions: list[QuickSetup__CustomFunctions__PackageDefinition] = None
    input_parameters: QuickSetup__CustomFunctions__InputField = None
    output_parameters: QuickSetup__CustomFunctions__OutputField = None
    raw_code_content: str
    categories: list[CustomToolCategories] = None
    is_shared_on_public_store: bool = False
    connected_assistant_names: list[str] = None


class CustomAPIAllowedMethods(str, Enum):
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    POST = "POST"
    DELETE = "DELETE"


class QuickSetup__CustomAPI__Endpoint(BaseModel):
    name: str
    description: str
    path: str
    http_method: CustomAPIAllowedMethods = CustomAPIAllowedMethods.GET
    header_parameters: list[str]
    path_parameters: list[str]
    query_parameters: list[str]
    body_parameters: list[str]


class QuickSetup__CustomAPI(BaseModel):
    nickname: str
    description: str = ""
    auth_token: str = ""
    base_url: str
    endpoints: list[QuickSetup__CustomAPI__Endpoint] = None
    categories: CustomToolCategories = None
    is_shared_on_public_store: bool = False


class QuickSetup__CustomScript(BaseModel):
    nickname: str
    description: str = ""
    raw_bash_script_content: str
    step_guide: list[QuickSetup__StepGuideList] = None
    categories: list[CustomToolCategories] = None
    is_shared_on_public_store: bool = False
    connected_assistant_names: list[str] = None


class QuickSetup__Tools(BaseModel):
    functions: list[QuickSetup__CustomFunction] = None
    apis: list[QuickSetup__CustomAPI] = None
    scripts: list[QuickSetup__CustomScript] = None


class QuickSetup__PaymentMethod(BaseModel):
    credit_card_number: str = ""
    name_on_card: str = ""
    expiration_month: str = ""
    expiration_year: str = ""
    cvc: str = ""


class VideoGeneratorProviders(str, Enum):
    LUMA_AI = "luma-ai"


class QuickSetup__VideoGenerator(BaseModel):
    provider: VideoGeneratorProviders = VideoGeneratorProviders.LUMA_AI
    nickname: str
    description: str = ""
    provider_api_key: str = ""
    connected_assistant_names: list[str] = None


class QuickSetup__MLModel__Item(BaseModel):
    download_url: str


class QuickSetup__MLModelStorage(BaseModel):
    nickname: str
    description: str = ""
    interpretation_temperature: int = 0.25
    interpretation_max_tokens: int = 4096
    ml_models: list[QuickSetup__MLModel__Item] = None
    connected_assistant_names: list[str] = None


class QuickSetup__VoidForgerConfiguration(BaseModel):
    response_tone: str = "Professional and Assertive"
    response_language: str = "auto"
    additional_instructions: str = ""
    max_actions_per_cycle: int = 5
    max_lifetime_cycles: int = 1000
    auto_trigger_interval_minutes: int = 15
    short_term_memory_max_messages: int = 25


class QuickSetup__OfficeTools__Drafting(BaseModel):
    folder_names: list[str] = None
    generate_google_apps_plugin_keys: bool = True


class QuickSetup__OfficeTools__Sheetos(BaseModel):
    folder_names: list[str] = None
    generate_google_apps_plugin_keys: bool = True


class QuickSetup__OfficeTools__Formica(BaseModel):
    generate_google_apps_plugin_keys: bool = True


class QuickSetup__OfficeTools__Slider(BaseModel):
    generate_google_apps_plugin_keys: bool = True


class QuickSetup__OfficeTools(BaseModel):
    integrate_office_tools: bool
    drafting: QuickSetup__OfficeTools__Drafting
    sheetos: QuickSetup__OfficeTools__Sheetos
    slider: QuickSetup__OfficeTools__Slider
    formica: QuickSetup__OfficeTools__Formica


class QuickSetup__AutoTopUp__TypeThreshold(BaseModel):
    threshold_value: float
    threshold_increment: float


class QuickSetup__AutoTopUp__TypeInterval(BaseModel):
    interval_days: int
    interval_increment: float


class QuickSetup__AutoTopUp(BaseModel):
    threshold_type: QuickSetup__AutoTopUp__TypeThreshold = None
    interval_type: QuickSetup__AutoTopUp__TypeInterval = None
    maximum_monthly_spend: float = 100.00


class QuickSetup__BlockchainWallet(BaseModel):
    blockchain_type: BlockchainTypes = BlockchainTypes.ETHEREUM
    nickname: str
    description: str = ""
    wallet_address: str
    wallet_private_key: str


class QuickSetup__ExportAPIs__Assistants(BaseModel):
    integrate_apis: bool = True
    api_key_protection: bool = True
    hourly_request_limit: int = 100


class QuickSetup__ExportAPIs__LeanMods(BaseModel):
    integrate_apis: bool = True
    api_key_protection: bool = True
    hourly_request_limit: int = 100


class QuickSetup__ExportAPIs__Orchestrators(BaseModel):
    integrate_apis: bool = True
    api_key_protection: bool = True
    hourly_request_limit: int = 100


class QuickSetup__ExportAPIs__VoidForgers(BaseModel):
    integrate_apis: bool = True
    api_key_protection: bool = True
    hourly_request_limit: int = 100


class QuickSetup__ExportAPIs(BaseModel):
    assistant_exports: QuickSetup__ExportAPIs__Assistants = None
    leanmod_exports: QuickSetup__ExportAPIs__LeanMods = None
    orchestrator_exports: QuickSetup__ExportAPIs__Orchestrators = None
    voidforger_exports: QuickSetup__ExportAPIs__VoidForgers = None


class QuickSetup__DataSources__SQL_CustomQuery(BaseModel):
    name: str
    description: str = ""
    raw_query_content: str


class QuickSetup__DataSources__NoSQL_CustomQuery(BaseModel):
    name: str
    description: str = ""
    raw_query_content: str


class QuickSetup__DataSources__SQL(BaseModel):
    nickname: str
    description: str = ""
    type: SQLDatabaseTypes = SQLDatabaseTypes.POSTGRESQL
    host: str
    port: int
    database_name: str
    username: str
    password: str
    write_permissions: bool
    max_record_retrieval_per_query: int = 50
    max_tokens_per_retrieval: int = 10000
    custom_sql_queries: list[QuickSetup__DataSources__SQL_CustomQuery] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__NoSQL(BaseModel):
    nickname: str
    description: str = ""
    type: NoSQLDatabaseTypes = NoSQLDatabaseTypes.COUCHBASE
    host: str
    port: int
    bucket_name: str
    username: str
    password: str
    write_permissions: bool
    max_record_retrieval_per_query: int = 50
    max_tokens_per_retrieval: int = 10000
    custom_nosql_queries: list[QuickSetup__DataSources__NoSQL_CustomQuery] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__FileSystem(BaseModel):
    nickname: str
    description: str = ""
    type: FileSystemTypes = FileSystemTypes.LINUX
    host: str
    port: int
    username: str
    password: str
    max_characters_retrieval_per_query: int = 5000
    write_permissions: bool
    connected_assistant_names: list[str] = None


class MediaStorageCategories(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    COMPRESSED = "compressed"
    CODE = "code"
    DATA = "data"


class QuickSetup__DataSources__MediaStorage__File(BaseModel):
    download_url: str


class QuickSetup__DataSources__MediaStorage(BaseModel):
    category: MediaStorageCategories = MediaStorageCategories.DATA
    nickname: str
    description: str = ""
    interpretation_temperature: float = 0.25
    interpretation_max_tokens: int = 4096
    medias_to_download: list[QuickSetup__DataSources__MediaStorage__File] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__KnowledgeBase__Document(BaseModel):
    download_url: str


class QuickSetup__DataSources__KnowledgeBaseStorage(BaseModel):
    nickname: str
    description: str = ""
    embedding_chunk_size: int = 1000
    embedding_chunk_overlap: int = 500
    max_search_retrieval_per_query: int = 10
    documents_to_index: list[QuickSetup__DataSources__KnowledgeBase__Document] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__WebPageIndexes(BaseModel):
    url: str


class QuickSetup__DataSources__EmbeddingVectorizers(str, Enum):
    TEXT2VEC_OPENAI = "text2vec-openai"


class QuickSetup__DataSources__WebPageStorage(BaseModel):
    nickname: str
    description: str = ""
    embedding_chunk_size: int = 1000
    embedding_chunk_overlap: int = 500
    max_search_retrieval_per_query: int = 10
    max_pages_to_index: int = 1000
    web_pages_to_index: list[QuickSetup__DataSources__WebPageIndexes] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__CodeRepositoryIndexes(BaseModel):
    url: str


class QuickSetup__DataSources__CodeRepositoryStorage(BaseModel):
    nickname: str
    description: str = ""
    embedding_chunk_size: int = 1000
    embedding_chunk_overlap: int = 500
    max_search_retrieval_per_query: int = 10
    repositories_to_index: list[QuickSetup__DataSources__CodeRepositoryIndexes] = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources__Browser__ExtensionDefinition(BaseModel):
    url_or_domain_extension: str


class QuickSetup__DataSources__Browser__HTMLCleanupStrategies(BaseModel):
    clean_javascript: bool = True
    clean_styles: bool = True
    clean_inline_styles: bool = True
    clean_comments: bool = True
    clean_links: bool = True
    clean_meta_tags: bool = True
    clean_page_structure: bool = True
    clean_processing_instructions: bool = True
    clean_embedded: bool = True
    clean_frames: bool = True
    clean_forms: bool = True
    clean_tags: list[str] = None


class QuickSetup__DataSources__Browser(BaseModel):
    nickname: str
    description: str = ""
    data_selectivity: float = 0.5
    minimum_investigation_sites: int = 2
    whitelisted_extensions: list[QuickSetup__DataSources__Browser__ExtensionDefinition] = None
    blacklisted_extensions: list[QuickSetup__DataSources__Browser__ExtensionDefinition] = None
    html_cleanup_strategies: QuickSetup__DataSources__Browser__HTMLCleanupStrategies = None
    connected_assistant_names: list[str] = None


class QuickSetup__DataSources(BaseModel):
    sql_databases: list[QuickSetup__DataSources__SQL] = None
    nosql_databases: list[QuickSetup__DataSources__NoSQL] = None
    file_systems: list[QuickSetup__DataSources__FileSystem] = None
    browsers: list[QuickSetup__DataSources__Browser] = None
    media_storages: list[QuickSetup__DataSources__MediaStorage] = None
    ml_model_storages: list[QuickSetup__MLModelStorage] = None
    video_generators: list[QuickSetup__VideoGenerator] = None
    knowledge_base_storages: list[QuickSetup__DataSources__KnowledgeBaseStorage] = None
    web_page_storages: list[QuickSetup__DataSources__WebPageStorage] = None
    code_repository_storages: list[QuickSetup__DataSources__CodeRepositoryStorage] = None


class QuickSetup__UserInvite(BaseModel):
    username: str
    email: str
    temporary_password: str = "Password123456!"
    first_name: str = ""
    last_name: str = ""
    phone_number: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    postal_code: str = ""
    role_names: list[str] = None


class QuickSetup__UserRoles__Automated(BaseModel):
    user_role_authorization_level: UserAuthorizationLevels = UserAuthorizationLevels.BASIC


class QuickSetup__RoleDefinitions(BaseModel):
    role_name: str
    permissions: list[str] = None


class QuickSetup__UserRoles__Wrapper(BaseModel):
    automated: QuickSetup__UserRoles__Automated = None
    custom: list[QuickSetup__RoleDefinitions] = None


class QuickSetup__EvaluationRubric__Base(BaseModel):
    comprehensiveness_weight: int = 10
    accuracy_weight: int = 9
    relevance_weight: int = 8
    cohesiveness_weight: int = 8
    diligence_weight: int = 6
    grammar_weight: int = 4
    naturalness_weight: int = 2


class QuickSetup__EvaluationRubric__AdditionalCriterion(BaseModel):
    criterion_name: str
    criterion_weight: int
    best_score_description: str
    above_average_score_description: str
    below_average_score_description: str
    worst_score_description: str


class QuickSetup__EvaluationRubric__AdditionalCriteria(BaseModel):
    additional_criteria: list[QuickSetup__EvaluationRubric__AdditionalCriterion] = None


class QuickSetup__EvaluationRubric__Wrapper(BaseModel):
    base_rubric: QuickSetup__EvaluationRubric__Base
    additional_criteria: QuickSetup__EvaluationRubric__AdditionalCriteria = None


class QuickSetup__SinapteraConfig(BaseModel):
    nitro_boost: bool = False
    active_on_assistants: bool = False
    active_on_leanmods: bool = False
    active_on_orchestrators: bool = False
    active_on_voidforgers: bool = False
    branching_factor: int = 3
    branch_keeping_factor: int = 1
    evaluation_depth_factor: int = 2
    evaluation_rubric: QuickSetup__EvaluationRubric__Wrapper


class QuickSetupPlugPlayAssistant(BaseModel):
    boilerplate_assistant_name: str


class QuickSetupPlugPlayTeam(BaseModel):
    boilerplate_team_name: str


class ExpertNetworks(BaseModel):
    network_name: str
    network_description: str
    assistant_names: list[str] = None


class LeanModAssistant(BaseModel):
    name: str
    instructions: str = "You are a helpful assistant."
    supervised_expert_network_names: list[str] = None
    context_overflow_management_strategy: ContextOverflowStrategyNames = ContextOverflowStrategyNames.VECTORIZE
    max_message_memory: int = 25


class OrchestrationMaestro(BaseModel):
    name: str
    max_assistants_limit: int = 10
    instructions: str = "You are a helpful orchestrator."
    description: str = ""
    step_by_step_task_explanation: str = ""
    response_template: str = ""
    audience: str = "Standard"
    tone: str = "Standard"
    response_language: str = "auto"
    worker_assistant_names: list[str] = None
    manager_assistant_names: list[str] = None


class SemantorConfiguration(BaseModel):
    local_network_access: bool = True
    global_network_access: bool = True
    temporary_data_source_and_tool_access: bool = True
    maximum_local_network_search_results: int = 5
    maximum_global_network_search_results: int = 5


class HadronPrimeEndpoint(BaseModel):
    curl: str = ""
    input_parameters: str = ""
    output_parameters: str = ""


class HadronPrimeNode(BaseModel):
    node_name: str
    node_description: str = ""
    optional_instructions: str = ""
    current_state: HadronPrimeEndpoint
    goal_state: HadronPrimeEndpoint
    error_calculation: HadronPrimeEndpoint
    sensory_measurements: HadronPrimeEndpoint
    action_set: HadronPrimeEndpoint
    analytic_calculation: HadronPrimeEndpoint
    actuation: HadronPrimeEndpoint
    subscribed_topic_names: list[str] = None
    expert_network_names: list[str] = None
    publishing_history_memory_capacity: int = 20
    sease_memory_capacity: int = 20
    topic_message_memory_capacity: int = 50


class HadronPrimeTopicCategoriesNames(str, Enum):
    ALERTS = "alerts"
    INFO = "info"
    STATES = "states"
    MEASUREMENTS = "measurements"
    ACTIONS = "actions"
    COMMANDS = "commands"


class HadronPrimeTopic(BaseModel):
    topic_name: str
    topic_description: str = ""
    topic_purpose_explanation: str = ""
    topic_category: HadronPrimeTopicCategoriesNames = HadronPrimeTopicCategoriesNames.ALERTS


class HadronPrimeSystem(BaseModel):
    system_name: str
    system_description: str = ""
    manager_assistant_names: list[str] = None
    nodes: list[HadronPrimeNode] = None
    topics: list[HadronPrimeTopic] = None


class QuickSetupCreate(BaseModel):
    organization: QuickSetup__Organization
    llm: QuickSetup__LLMModel
    assistants: QuickSetup__Assistant__Wrapper
    leanmod_assistants: list[LeanModAssistant] = None
    orchestration_maestros: list[OrchestrationMaestro] = None
    memories: QuickSetup__Memories
    message_templates: list[QuickSetup__MessageTemplate] = None
    scheduled_jobs: QuickSetup__ScheduledJob__Wrapper = None
    triggered_jobs: QuickSetup__TriggeredJob__Wrapper = None
    office_tools: QuickSetup__OfficeTools
    payment_methods: QuickSetup__PaymentMethod = None
    auto_top_up: QuickSetup__AutoTopUp = None
    blockchain_wallets: list[QuickSetup__BlockchainWallet] = None
    export_apis: QuickSetup__ExportAPIs
    data_sources: QuickSetup__DataSources = None
    tools: QuickSetup__Tools = None
    user_invites: list[QuickSetup__UserInvite] = None
    user_roles: QuickSetup__UserRoles__Wrapper = None
    sinaptera_config: QuickSetup__SinapteraConfig = None
    boilerplate_assistants: list[QuickSetupPlugPlayAssistant] = None
    boilerplate_teams: list[QuickSetupPlugPlayTeam] = None
    expert_networks: list[ExpertNetworks] = None
    semantor_configuration: SemantorConfiguration = None
    brainstorming_sessions: list[QuickSetup__BrainstormingSession] = None
    hadron_prime_systems: list[HadronPrimeSystem] = None
    voidforger_configuration: QuickSetup__VoidForgerConfiguration = None


####################################################################################################
# SETUP RESPONSE SCHEMA
####################################################################################################


class QuickSetupResponse(BaseModel):
    organization_id: int
    llm_model_id: int
    assistants: list[str]
