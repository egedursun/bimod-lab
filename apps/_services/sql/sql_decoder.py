from apps._services.sql.sql_executor import PostgresSQLExecutor, MySQLExecutor
from apps.datasource_sql.models import SQLDatabaseConnection


class InternalSQLClient:

    SQL_DBMS_PROVIDERS = {
        "POSTGRESQL": {"code": "postgresql", "name": "PostgreSQL"},
        "MYSQL": {"code": "mysql", "name": "MySQL"},
    }

    @staticmethod
    def get(connection: SQLDatabaseConnection):
        if connection.dbms_type == InternalSQLClient.SQL_DBMS_PROVIDERS["POSTGRESQL"]["code"]:
            print(f"[InternalSQLClient.get] PostgreSQL connection detected.")
            return PostgresSQLExecutor(connection)
        elif connection.dbms_type == InternalSQLClient.SQL_DBMS_PROVIDERS["MYSQL"]["code"]:
            print(f"[InternalSQLClient.get] MySQL connection detected.")
            return MySQLExecutor(connection)
