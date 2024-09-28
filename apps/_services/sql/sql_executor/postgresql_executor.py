import psycopg2
from psycopg2.extras import RealDictCursor

from apps._services.config.costs_map import ToolCostsMap
from apps._services.sql.utils import before_execute_sql_query, can_write_to_database
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class PostgresSQLExecutor:
    def __init__(self, connection: SQLDatabaseConnection):
        # run the before_execute_sql_query function to refresh the schema
        before_execute_sql_query(connection)
        self.conn_params = {
            'dbname': connection.database_name,
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'port': connection.port
        }
        self.connection_object = connection

    def execute_read(self, query, parameters=None):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        results = {"status": True, "error": ""}
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    print(f"[PostgresSQLExecutor.execute_read] Executing Query: {query}")
                    cursor.execute(query, parameters)
                    results = cursor.fetchall()
            print(f"[PostgresSQLExecutor.execute_read] Read operation is successful.")
        except Exception as e:
            print(f"[PostgresSQLExecutor.execute_read] Error executing PostgreSQL / Read Query: {e}")
            results["status"] = False
            results["error"] = str(e)

        new_transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.SQLReadExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.SQL_READ,
            is_tool_cost=True
        )
        new_transaction.save()
        print(f"[PostgresSQLExecutor.execute_read] Transaction has been saved.")
        return results

    def execute_write(self, query, parameters=None) -> dict:
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        if not can_write_to_database(self.connection_object):
            return {"status": False, "error": "No write permission within this database connection."}

        output = {"status": True, "error": ""}
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, parameters)
                    conn.commit()
            print(f"[PostgresSQLExecutor.execute_write] Write operation is successful.")
        except Exception as e:
            print(f"[PostgresSQLExecutor.execute_write] Error executing PostgreSQL / Write Query: {e}")
            output["status"] = False
            output["error"] = str(e)

        new_transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.SQLWriteExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.SQL_WRITE,
            is_tool_cost=True
        )
        new_transaction.save()
        print(f"[PostgresSQLExecutor.execute_write] Transaction has been saved.")
        return output
