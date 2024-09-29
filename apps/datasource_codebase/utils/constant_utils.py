#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:38:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.


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
