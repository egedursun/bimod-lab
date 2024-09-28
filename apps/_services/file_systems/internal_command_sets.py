class DataSourceFileSystemsOsTypeNames:
    LINUX = 'linux'
    MACOS = 'macos'


LIST_DIRECTORY_RECURSIVE = 'list_directory_recursive'
INTERNAL_COMMAND_SETS = {
    LIST_DIRECTORY_RECURSIVE: {
        'description': 'List directory contents recursively',
        DataSourceFileSystemsOsTypeNames.LINUX: 'ls -R ../',
        DataSourceFileSystemsOsTypeNames.MACOS: 'ls -R ../',
    }
}
