import os

import boto3
from django.db import models
from slugify import slugify

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.utils import generate_class_name
from config.settings import MEDIA_URL

KNOWLEDGE_BASE_SYSTEMS = [
    ('weaviate', 'Weaviate'),
]

VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class KnowledgeBaseSystemNames:
    WEAVIATE = 'weaviate'


SUPPORTED_CODE_FILE_TYPES = [
    ('.py', 'Python'),
    ('.ipynb', 'Jupyter Notebook'),
    ('.rmd', 'R Markdown'),
    ('.java', 'Java'),
    ('.js', 'JavaScript'),
    ('.jsx', 'JSX'),
    ('.ts', 'TypeScript'),
    ('.tsx', 'TSX'),
    ('.html', 'HTML'),
    ('.htm', 'HTML'),
    ('.css', 'CSS'),
    ('.sass', 'SASS'),
    ('.scss', 'SCSS'),
    ('.styl', 'Stylus'),
    ('.vue', 'Vue'),
    ('.less', 'LESS'),
    ('.php', 'PHP'),
    ('.sql', 'SQL'),
    ('.dart', 'Dart'),
    ('.r', 'R'),
    ('.rb', 'Ruby'),
    ('.go', 'Go'),
    ('.c', 'C'),
    ('.cpp', 'C++'),
    ('.cs', 'C#'),
    ('.swift', 'Swift'),
    ('.kt', 'Kotlin'),
    ('.scala', 'Scala'),
    ('.groovy', 'Groovy'),
    ('.perl', 'Perl'),
    ('.lua', 'Lua'),
    ('.rust', 'Rust'),
    ('.elm', 'Elm'),
    ('.ocaml', 'OCaml'),
    ('.fsharp', 'F#'),
    ('.haskell', 'Haskell'),
    ('.clojure', 'Clojure'),
    ('.erlang', 'Erlang'),
    ('.ex', 'Elixir'),
    ('.exs', 'Elixir Script'),
    ('.julia', 'Julia'),
    ('.fortran', 'Fortran'),
    ('.pascal', 'Pascal'),
    ('.ada', 'Ada'),
    ('.lisp', 'Lisp'),
    ('.scheme', 'Scheme'),
    ('.prolog', 'Prolog'),
    ('.smalltalk', 'Smalltalk'),
    ('.forth', 'Forth'),
    ('.bash', 'Bash'),
    ('.powershell', 'PowerShell'),
    ('.batch', 'Batch'),
    ('.perl6', 'Perl 6'),
    ('.tcl', 'Tcl'),
    ('.awk', 'AWK'),
    ('.sed', 'sed'),
    ('.yaml', 'YAML'),
    ('.json', 'JSON'),
    ('.xml', 'XML'),
    ('.toml', 'TOML'),
    ('.ini', 'INI'),
    ('.cfg', 'CFG'),
    ('.conf', 'CONF'),
    ('.properties', 'Properties'),
    ('.env', 'ENV'),
    ('.md', 'Markdown'),
    ('.rst', 'reStructuredText'),
    ('.txt', 'Text'),
    ('.log', 'Log'),
]


class SupportedCodeFileTypes:
    PYTHON = '.py'
    JUPYTER_NOTEBOOK = '.ipynb'
    R_MARKDOWN = '.rmd'
    JAVA = '.java'
    JAVASCRIPT = '.js'
    JSX = '.jsx'
    TYPESCRIPT = '.ts'
    TSX = '.tsx'
    HTML = '.html'
    HTM = '.htm'
    CSS = '.css'
    SASS = '.sass'
    SCSS = '.scss'
    STYLUS = '.styl'
    VUE = '.vue'
    LESS = '.less'
    PHP = '.php'
    SQL = '.sql'
    DART = '.dart'
    R = '.r'
    RUBY = '.rb'
    GO = '.go'
    C = '.c'
    CPP = '.cpp'
    CSHARP = '.cs'
    SWIFT = '.swift'
    KOTLIN = '.kt'
    SCALA = '.scala'
    GROOVY = '.groovy'
    PERL = '.perl'
    LUA = '.lua'
    RUST = '.rust'
    ELM = '.elm'
    OCAML = '.ocaml'
    FSHARP = '.fsharp'
    HASKELL = '.haskell'
    CLOJURE = '.clojure'
    ERLANG = '.erlang'
    ELIXIR = '.ex'
    ELIXIR_SCRIPT = '.exs'
    JULIA = '.julia'
    FORTRAN = '.fortran'
    PASCAL = '.pascal'
    ADA = '.ada'
    LISP = '.lisp'
    SCHEME = '.scheme'
    PROLOG = '.prolog'
    SMALLTALK = '.smalltalk'
    FORTH = '.forth'
    BASH = '.bash'
    POWERSHELL = '.powershell'
    BATCH = '.batch'
    PERL6 = '.perl6'
    TCL = '.tcl'
    AWK = '.awk'
    SED = '.sed'
    YAML = '.yaml'
    JSON = '.json'
    XML = '.xml'
    TOML = '.toml'
    INI = '.ini'
    CFG = '.cfg'
    CONF = '.conf'
    PROPERTIES = '.properties'
    ENV = '.env'
    MARKDOWN = '.md'
    RESTRUCTUREDTEXT = '.rst'
    TEXT = '.txt'
    LOG = '.log'

    @staticmethod
    def as_list():
        return [
            SupportedCodeFileTypes.PYTHON,
            SupportedCodeFileTypes.JUPYTER_NOTEBOOK,
            SupportedCodeFileTypes.R_MARKDOWN,
            SupportedCodeFileTypes.JAVA,
            SupportedCodeFileTypes.JAVASCRIPT,
            SupportedCodeFileTypes.JSX,
            SupportedCodeFileTypes.TYPESCRIPT,
            SupportedCodeFileTypes.TSX,
            SupportedCodeFileTypes.HTML,
            SupportedCodeFileTypes.HTM,
            SupportedCodeFileTypes.CSS,
            SupportedCodeFileTypes.SASS,
            SupportedCodeFileTypes.SCSS,
            SupportedCodeFileTypes.STYLUS,
            SupportedCodeFileTypes.VUE,
            SupportedCodeFileTypes.LESS,
            SupportedCodeFileTypes.PHP,
            SupportedCodeFileTypes.SQL,
            SupportedCodeFileTypes.DART,
            SupportedCodeFileTypes.R,
            SupportedCodeFileTypes.RUBY,
            SupportedCodeFileTypes.GO,
            SupportedCodeFileTypes.C,
            SupportedCodeFileTypes.CPP,
            SupportedCodeFileTypes.CSHARP,
            SupportedCodeFileTypes.SWIFT,
            SupportedCodeFileTypes.KOTLIN,
            SupportedCodeFileTypes.SCALA,
            SupportedCodeFileTypes.GROOVY,
            SupportedCodeFileTypes.PERL,
            SupportedCodeFileTypes.LUA,
            SupportedCodeFileTypes.RUST,
            SupportedCodeFileTypes.ELM,
            SupportedCodeFileTypes.OCAML,
            SupportedCodeFileTypes.FSHARP,
            SupportedCodeFileTypes.HASKELL,
            SupportedCodeFileTypes.CLOJURE,
            SupportedCodeFileTypes.ERLANG,
            SupportedCodeFileTypes.ELIXIR,
            SupportedCodeFileTypes.ELIXIR_SCRIPT,
            SupportedCodeFileTypes.JULIA,
            SupportedCodeFileTypes.FORTRAN,
            SupportedCodeFileTypes.PASCAL,
            SupportedCodeFileTypes.ADA,
            SupportedCodeFileTypes.LISP,
            SupportedCodeFileTypes.SCHEME,
            SupportedCodeFileTypes.PROLOG,
            SupportedCodeFileTypes.SMALLTALK,
            SupportedCodeFileTypes.FORTH,
            SupportedCodeFileTypes.BASH,
            SupportedCodeFileTypes.POWERSHELL,
            SupportedCodeFileTypes.BATCH,
            SupportedCodeFileTypes.PERL6,
            SupportedCodeFileTypes.TCL,
            SupportedCodeFileTypes.AWK,
            SupportedCodeFileTypes.SED,
            SupportedCodeFileTypes.YAML,
            SupportedCodeFileTypes.JSON,
            SupportedCodeFileTypes.XML,
            SupportedCodeFileTypes.TOML,
            SupportedCodeFileTypes.INI,
            SupportedCodeFileTypes.CFG,
            SupportedCodeFileTypes.CONF,
            SupportedCodeFileTypes.PROPERTIES,
            SupportedCodeFileTypes.ENV,
            SupportedCodeFileTypes.MARKDOWN,
            SupportedCodeFileTypes.RESTRUCTUREDTEXT,
            SupportedCodeFileTypes.TEXT,
            SupportedCodeFileTypes.LOG
        ]


class RepositoryUploadStatusNames:
    STAGED = 'staged'
    UPLOADED = 'uploaded'
    LOADED = 'loaded'
    CHUNKED = 'chunked'
    EMBEDDED_DOCUMENT = 'embedded_document'
    SAVED_DOCUMENT = 'saved_document'
    PROCESSED_DOCUMENT = 'processed_document'
    EMBEDDED_CHUNKS = 'embedded_chunks'
    SAVED_CHUNKS = 'saved_chunks'
    PROCESSED_CHUNKS = 'processed_chunks'
    COMPLETED = 'completed'
    FAILED = 'failed'
    PARTIALLY_FAILED = 'partially_failed'


class CodeRepositoryStorageConnection(models.Model):
    # Main information
    provider = models.CharField(max_length=100, choices=KNOWLEDGE_BASE_SYSTEMS)
    host_url = models.CharField(max_length=1000)
    provider_api_key = models.CharField(max_length=1000, null=True, blank=True)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    # Class metadata
    class_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField()
    vectorizer = models.CharField(max_length=100, choices=VECTORIZERS, default="text2vec-openai", null=True, blank=True)
    vectorizer_api_key = models.CharField(max_length=1000, null=True, blank=True)

    # Langchain chunking rules
    embedding_chunk_size = models.IntegerField(default=1024)
    embedding_chunk_overlap = models.IntegerField(default=256)

    # Schema (for defining the overall structure to the assistant)
    schema_json = models.TextField(null=True, blank=True)

    search_instance_retrieval_limit = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.assistant.name + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Repository Storage Connection"
        verbose_name_plural = "Code Repository Storage Connections"
        ordering = ["-created_at"]
        unique_together = ['host_url', 'assistant']
        indexes = [
            models.Index(fields=["provider", "assistant", "name"]),
            models.Index(fields=["provider", "assistant", "created_at"]),
            models.Index(fields=["provider", "assistant", "updated_at"]),
            models.Index(fields=["class_name"]),
            models.Index(fields=["vectorizer"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.vectorizer is None:
            self.vectorizer = "text2vec-openai"

        if self.class_name is None:
            self.class_name = generate_class_name(self)

        client = CodeBaseDecoder.get(self)
        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnection.save] Error creating Weaviate classes: {result['error']}")

        self.schema_json = client.retrieve_schema()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the classes from Weaviate
        client = CodeBaseDecoder.get(self)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=self.class_name)
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnection.save] Error deleting Weaviate classes: {result['error']}")

        super().delete(using, keep_parents)


class CodeBaseRepository(models.Model):
    knowledge_base = models.ForeignKey("CodeRepositoryStorageConnection", on_delete=models.CASCADE,
                                       related_name="code_base_repositories")
    repository_name = models.CharField(max_length=1000)
    repository_description = models.TextField()
    repository_metadata = models.JSONField()  # auto
    repository_uri = models.CharField(max_length=1000, null=True, blank=True)

    # to associate the element with the Weaviate object
    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)

    # Documents have chunks
    repository_content_temporary = models.TextField(blank=True, null=True)  # This will be emptied before indexing

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return slugify(self.repository_name) + " - " + self.knowledge_base.name + " - " + self.created_at.strftime(
            "%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Base Repository"
        verbose_name_plural = "Code Base Repositories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["knowledge_base", "repository_name"]),
            models.Index(fields=["knowledge_base", "created_at"]),
            models.Index(fields=["knowledge_base", "updated_at"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.document_file_name = slugify(self.repository_name)
        self.document_content_temporary = ""
        self.document_description = ""
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # delete the document from Weaviate
        client = CodeBaseDecoder.get(self.knowledge_base)
        if client is not None:
            result = client.delete_weaviate_document(
                class_name=self.knowledge_base.class_name,
                document_uuid=self.knowledge_base_uuid)
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnection.delete] Error deleting Weaviate document: {result['error']}")
            # remove the document from the directory
            document_full_path = self.repository_uri
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3_path = document_full_path.split(MEDIA_URL)[1]
            s3_path = s3_path.replace('/', '')
            s3_path = f"{s3_path}/"
            if document_full_path is not None:
                try:
                    boto3_client.delete_object(Bucket=bucket_name, Key=s3_path)
                except Exception as e:
                    print(f"[CodeBaseRepository.delete] Error deleting S3 object: {str(e)}")
        # delete the object from ORM
        super().delete(using, keep_parents)


class CodeBaseRepositoryChunk(models.Model):
    knowledge_base = models.ForeignKey("CodeRepositoryStorageConnection", on_delete=models.CASCADE)
    repository = models.ForeignKey("CodeBaseRepository", on_delete=models.CASCADE, related_name="repository_chunks")

    chunk_number = models.IntegerField()
    chunk_content = models.TextField()  # This will be the text content of the chunk
    chunk_metadata = models.TextField()
    chunk_repository_uri = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_base_uuid = models.CharField(max_length=1000, null=True, blank=True)
    repository_uuid = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(
            self.chunk_number) + " - " + self.repository.repository_name + " - " + self.knowledge_base.name + " - " + self.created_at.strftime(
            "%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Code Base Document Chunk"
        verbose_name_plural = "Code Base Document Chunks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["knowledge_base", "repository", "chunk_number"]),
            models.Index(fields=["knowledge_base", "repository", "created_at"]),
            models.Index(fields=["knowledge_base", "repository", "updated_at"]),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


class RepositoryProcessingLog(models.Model):
    repository_full_uri = models.CharField(max_length=1000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.repository_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Repository Processing Log"
        verbose_name_plural = "Repository Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["repository_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
