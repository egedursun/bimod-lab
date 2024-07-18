import os

from celery import shared_task


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
    ############################
    # Image Files
    ('jpg', 'JPEG'),
    ('png', 'PNG'),
    ('gif', 'GIF'),
    ('svg', 'SVG'),
    ('bmp', 'BMP'),
    ('tiff', 'TIFF'),
    ############################
    # Audio Files
    ('mp3', 'MP3'),
    ('wav', 'WAV'),
    ('flac', 'FLAC'),
    ('aac', 'AAC'),
    ('ogg', 'OGG'),
    ############################
    # Video Files
    ('mp4', 'MP4'),
    ('avi', 'AVI'),
    ('mkv', 'MKV'),
    ('mov', 'MOV'),
    ############################
    # Compressed Files
    ('zip', 'ZIP'),
    ('rar', 'RAR'),
    ('tar', 'TAR'),
    ############################
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

    ############################
    # Data Configuration files
    ('yml', 'YML'),
    ('yaml', 'YAML'),
    ('sql', 'SQL'),
    ('pkl', 'Pickle'),
    ('csv', 'CSV'),
    ('xlsx', 'Excel'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('tsv', 'TSV'),
    ############################
)


class MediaFileTypesNamesLists:
    IMAGE = ['jpg', 'png', 'gif', 'svg', 'bmp', 'tiff']
    AUDIO = ['mp3', 'wav', 'flac', 'aac', 'ogg']
    VIDEO = ['mp4', 'avi', 'mkv', 'mov']
    COMPRESSED = ['zip', 'rar', 'tar']
    CODE = ['py', 'js', 'ts', 'php', 'css', 'html', 'java', 'c', 'cpp', 'h', 'sh', 'go', 'dart']
    DATA = ['yml', 'yaml', 'sql', 'pkl', 'csv', 'xlsx', 'json', 'xml', 'tsv']


@shared_task
def upload_file_to_storage(file_bytes: bytes, full_path: str, media_category: str):

    file_format = full_path.split('.')[-1]
    if file_format not in [file_type[0] for file_type in MEDIA_FILE_TYPES]:
        print(f"Invalid file format: {file_format}, skipping file...")
        return False

    if media_category == MediaCategoriesNames.Image:
        if file_format not in MediaFileTypesNamesLists.IMAGE:
            print(f"Invalid IMAGE file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Audio:
        if file_format not in MediaFileTypesNamesLists.AUDIO:
            print(f"Invalid AUDIO file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Video:
        if file_format not in MediaFileTypesNamesLists.VIDEO:
            print(f"Invalid VIDEO file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Compressed:
        if file_format not in MediaFileTypesNamesLists.COMPRESSED:
            print(f"Invalid COMPRESSED file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Code:
        if file_format not in MediaFileTypesNamesLists.CODE:
            print(f"Invalid CODE file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Data:
        if file_format not in MediaFileTypesNamesLists.DATA:
            print(f"Invalid DATA file format: {file_format}, skipping file...")
            return False
    else:
        print(f"Invalid media category: {media_category}, skipping file...")
        return False

    try:
        with open(str("./"+full_path), "wb+") as file:
            # write the file
            file.write(file_bytes)
    except Exception as e:
        print(f"Error uploading file to storage: {e}")
        return False
    return True
