import mysql
import psycopg2
from mysql.connector.cursor import MySQLCursorDict
from psycopg2.extras import RealDictCursor

from apps.datasource_sql.models import SQLDatabaseConnection, DBMSChoicesNames


# This function will refresh the schema data before executing the SQL query, which will improve the accuracy
# and comprehension of the AI assistant
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


# Checking the read and write permissions
def can_write_to_database(connection: SQLDatabaseConnection):
    return not connection.is_read_only


class PostgresSQLExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        ##################################################
        # run the before_execute_sql_query function to refresh the schema
        before_execute_sql_query(connection)
        ##################################################

        self.conn_params = {
            'dbname': connection.database_name,
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'port': connection.port
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
        ##################################################
        # run the before_execute_sql_query function to refresh the schema
        before_execute_sql_query(connection)
        ##################################################

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
