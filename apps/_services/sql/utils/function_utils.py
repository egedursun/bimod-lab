from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_sql.utils import DBMSChoicesNames


def before_execute_sql_query(connection: SQLDatabaseConnection):
    # This function is called before executing the SQL query, to refresh the database schema
    old_schema_json = connection.schema_data_json
    new_schema = {}
    if connection.dbms_type == DBMSChoicesNames.POSTGRESQL:
        new_schema = connection.retrieve_postgresql_schema()
    elif connection.dbms_type == DBMSChoicesNames.MYSQL:
        new_schema = connection.retrieve_mysql_schema()
    if new_schema != old_schema_json:
        connection.schema_data_json = new_schema
        connection.save()


def can_write_to_database(connection: SQLDatabaseConnection):
    print(f"[sql_executor.can_write_to_database] Checking the write permission for the connection.")
    return not connection.is_read_only
