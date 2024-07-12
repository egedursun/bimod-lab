from apps._services.nosql.nosql_executor import MongoDBQueryExecutor
from apps.datasource_nosql.models import NoSQLDatabaseConnection


class InternalNoSQLClient:

    NOSQL_DBMS_PROVIDERS = {
        "MONGODB": {
            "code": "mongodb",
            "name": "MongoDB"
        },
    }

    @staticmethod
    def get(connection: NoSQLDatabaseConnection):
        if connection.dbms_type == InternalNoSQLClient.NOSQL_DBMS_PROVIDERS["MONGODB"]["code"]:
            return MongoDBQueryExecutor(connection)
