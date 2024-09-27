MEDIA_CATEGORIES = (
    ('image', 'Image'),
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('compressed', 'Compressed'),
    ('code', 'Code'),
    ('data', 'Data'),
)


class MediaCategoriesNames:
    Image = 'image'
    Audio = 'audio'
    Video = 'video'
    Compressed = 'compressed'
    Code = 'code'
    Data = 'data'


MEDIA_FILE_TYPES = (
    # Image Files
    ('jpg', 'JPEG'),
    ('png', 'PNG'),
    ('gif', 'GIF'),
    ('svg', 'SVG'),
    ('bmp', 'BMP'),
    ('tiff', 'TIFF'),
    # Audio Files
    ('mp3', 'MP3'),
    ('wav', 'WAV'),
    ('flac', 'FLAC'),
    ('aac', 'AAC'),
    ('ogg', 'OGG'),
    # Video Files
    ('mp4', 'MP4'),
    ('avi', 'AVI'),
    ('mkv', 'MKV'),
    ('mov', 'MOV'),
    # Compressed Files
    ('zip', 'ZIP'),
    ('rar', 'RAR'),
    ('tar', 'TAR'),
    # Code Files
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('ts', 'TypeScript'),
    ('php', 'PHP'),
    ('css', 'CSS'),
    ('html', 'HTML'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('h', 'C-Header'),
    ('sh', 'Shell'),
    ('go', 'Go'),
    ('dart', 'Dart'),
    # Data Configuration files
    ('yml', 'YML'),
    ('yaml', 'YAML'),
    ('sql', 'SQL'),
    ('pkl', 'Pickle'),
    ('csv', 'CSV'),
    ('xlsx', 'XLSX'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('tsv', 'TSV'),
    ('docx', 'DOCX'),
    ('pptx', 'PPTX'),
    ('pdf', 'PDF'),
    ('txt', 'TXT'),
)


class MediaFileTypesNames:
    class Image:
        JPEG = 'jpg'
        PNG = 'png'
        GIF = 'gif'
        SVG = 'svg'
        BMP = 'bmp'
        TIFF = 'tiff'

    class Audio:
        MP3 = 'mp3'
        WAV = 'wav'
        FLAC = 'flac'
        AAC = 'aac'
        OGG = 'ogg'

    class Video:
        MP4 = 'mp4'
        AVI = 'avi'
        MKV = 'mkv'
        MOV = 'mov'

    class Compressed:
        ZIP = 'zip'
        RAR = 'rar'
        TAR = 'tar'

    class Code:
        Python = 'py'
        JavaScript = 'js'
        TypeScript = 'ts'
        PHP = 'php'
        CSS = 'css'
        HTML = 'html'
        Java = 'java'
        C = 'c'
        Cpp = 'cpp'
        CHeader = 'h'
        Shell = 'sh'
        Go = 'go'
        Dart = 'dart'

    class Data:
        YML = 'yml'
        YAML = 'yaml'
        SQL = 'sql'
        Pickle = 'pkl'
        CSV = 'csv'
        XLSX = 'xlsx'
        JSON = 'json'
        XML = 'xml'
        TSV = 'tsv'
        DOCX = 'docx'
        PPTX = 'pptx'
        PDF = 'pdf'
        TXT = 'txt'


class MediaFileTypesNamesLists:
    IMAGE = ['jpg', 'png', 'gif', 'svg', 'bmp', 'tiff']
    AUDIO = ['mp3', 'wav', 'flac', 'aac', 'ogg']
    VIDEO = ['mp4', 'avi', 'mkv', 'mov']
    COMPRESSED = ['zip', 'rar', 'tar']
    CODE = ['py', 'js', 'ts', 'php', 'css', 'html', 'java', 'c', 'cpp', 'h', 'sh', 'go', 'dart']
    DATA = ['yml', 'yaml', 'sql', 'pkl', 'csv', 'xlsx', 'json', 'xml', 'tsv', 'docx', 'pptx', 'pdf', 'txt']


FILE_TYPE_HIGHLIGHTING_DECODER = {
    "py": "python", "js": "javascript", "ts": "typescript", "php": "php", "css": "css", "html": "html",
    "java": "java", "c": "c", "cpp": "cpp", "h": "h", "sh": "shell", "go": "golang", "dart": "dart",
    "yml": "yaml", "yaml": "yaml", "sql": "sql", "pkl": "plaintext", "csv": "plaintext",
    "xlsx": "plaintext", "json": "json", "xml": "xml", "tsv": "plaintext", "docx": "plaintext",
    "pptx": "plaintext", "pdf": "plaintext", "txt": "plaintext",
}
