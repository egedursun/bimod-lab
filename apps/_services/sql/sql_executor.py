import mysql
import psycopg2
from mysql.connector.cursor import MySQLCursorDict
from psycopg2.extras import RealDictCursor

from apps.datasource_sql.models import SQLDatabaseConnection


class PostgresSQLExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        self.conn_params = {
            'dbname': connection.database_name,
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'port': connection.port,
            'options': f'-c search_path={connection.schema_name}'
        }

    def execute_read(self, query, parameters=None):
        results = []
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, parameters)
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error executing PostgreSQL / Read Query: {e}")
        return results

    def execute_write(self, query, parameters=None) -> dict:
        output = {"status": True, "error": ""}
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, parameters)
                    conn.commit()
        except Exception as e:
            print(f"Error executing PostgreSQL / Write Query: {e}")
            output["status"] = False
            output["error"] = str(e)
        return output


class MySQLExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        self.conn_params = {
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'database': connection.database_name,
            'port': connection.port
        }

    def execute_read(self, query, parameters=None):
        results = []
        try:
            with mysql.connector.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_class=MySQLCursorDict) as cursor:
                    cursor.execute(query, parameters)
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error executing MySQL / Read Query: {e}")
        return results

    def execute_write(self, query, parameters=None):
        output = {"status": True, "error": ""}
        try:
            with mysql.connector.connect(**self.conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, parameters)
                    conn.commit()
        except Exception as e:
            print(f"Error executing MySQL / Write Query: {e}")
            output["status"] = False
            output["error"] = str(e)
        return output
