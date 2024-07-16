from apps._services.file_systems.file_systems_executor import FileSystemsExecutor
from apps.datasource_file_systems.models import DataSourceFileSystem


def execute_file_system_commands(connection_id: int, commands: list[str]):
    file_system_connection = DataSourceFileSystem.objects.get(id=connection_id)

    client = FileSystemsExecutor(connection=file_system_connection)

    file_system_response = client.execute_file_system_command_set(commands=commands)

    return file_system_response
