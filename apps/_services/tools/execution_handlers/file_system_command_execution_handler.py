from apps._services.file_systems.file_systems_executor import FileSystemsExecutor
from apps.datasource_file_systems.models import DataSourceFileSystem


def execute_file_system_commands(connection_id: int, commands: list[str]):
    file_system_connection = DataSourceFileSystem.objects.get(id=connection_id)
    print(
        f"[file_system_command_execution_handler.execute_file_system_commands] Executing file system commands: {commands}.")
    try:
        client = FileSystemsExecutor(connection=file_system_connection)
        file_system_response = client.execute_file_system_command_set(commands=commands)
    except Exception as e:
        error = (f"[file_system_command_execution_handler.execute_file_system_commands] Error occurred while "
                 f"executing the file system commands: {str(e)}")
        return error
    print(
        f"[file_system_command_execution_handler.execute_file_system_commands] File system commands executed "
        f"successfully.")
    return file_system_response
