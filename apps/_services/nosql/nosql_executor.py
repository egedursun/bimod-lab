import json

import certifi
from pymongo import MongoClient

from apps.datasource_nosql.models import NoSQLDatabaseConnection, NoSQLDBMSChoicesNames
from apps.datasource_nosql.utils import calculate_number_of_tokens, GPT_DEFAULT_ENCODING_ENGINE, \
    trim_according_to_token_limit


def before_execute_nosql_query(connection: NoSQLDatabaseConnection):
    old_schema_json = connection.schema_data_json
    new_schema = {}
    if connection.dbms_type == NoSQLDBMSChoicesNames.MONGODB:
        new_schema = connection.retrieve_mongodb_schema(
            connection_string=connection.connection_string,
            db_name=connection.db_name)
    if new_schema != old_schema_json:
        connection.schema_data_json = new_schema
        connection.save()


def can_write_to_database(connection: NoSQLDatabaseConnection):
    return not connection.is_read_only


class AllowedMongoDBWriteOperations:
    INSERT_ONE = "insert_one"
    INSERT_MANY = "insert_many"
    UPDATE_ONE = "update_one"
    UPDATE_MANY = "update_many"
    DELETE_ONE = "delete_one"
    DELETE_MANY = "delete_many"


class AllowedMongoDBHelperOperations:
    FILTER = "filter"


TRUNCATION_THRESHOLD_DATA = 1000
TOTAL_DATA_SAFETY_THRESHOLD_TOKENS = 10000


class MongoDBQueryExecutor:

    def __init__(self, connection: NoSQLDatabaseConnection):
        ##################################################
        # run the before_execute_nosql_query function to refresh the schema
        before_execute_nosql_query(connection)
        ##################################################

        self.connection_string = connection.connection_string
        self.connection_object = connection
        self.client = MongoClient(self.connection_string, tlsCAFile=certifi.where())
        self.db = self.client[connection.db_name]

    def execute_read(self, query, parameters=None):
        results = {"status": True, "data": [], "error": ""}
        try:
            # Assuming query is a dictionary specifying the MongoDB read operation
            collection_name = query.get('collection')
            collection = self.db.get_collection(collection_name)
            query_json = query.get('query', {})
            cursor = collection.find(query_json)
            limited_results = []

            # Limit the depth of each document to only the first level
            cursor_docs = list(cursor)
            cursor_docs = json.loads(json.dumps(cursor_docs, default=str))
            for doc in cursor_docs:
                limited_doc = {}
                for key, value in doc.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        limited_doc[key] = "{ ... inner_document_requiring_distinct_query ... }"
                    else:
                        try:
                            stringified_value = str(value)
                        except Exception as e:
                            stringified_value = "<unstringifiable>"
                        limited_doc[key] = stringified_value[:TRUNCATION_THRESHOLD_DATA] if len(
                            stringified_value) > TRUNCATION_THRESHOLD_DATA else stringified_value

                limited_results.append(limited_doc)

            limited_results_text = json.dumps(limited_results, default=str)
            number_of_tokens = calculate_number_of_tokens(encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                                        text=limited_results_text)
            if number_of_tokens > TOTAL_DATA_SAFETY_THRESHOLD_TOKENS:
                # truncate the data
                limited_results_text = trim_according_to_token_limit(
                    text=limited_results_text,
                    current_tokens=number_of_tokens,
                    token_limit=TOTAL_DATA_SAFETY_THRESHOLD_TOKENS) + "... <overflow_truncated>"

            results["data"] = limited_results_text
            print(f"Results: {results["data"]}")
        except Exception as e:
            print(f"Error executing MongoDB / Read Query: {e}")
            results["status"] = False
            results["error"] = str(e)
        return results

    def execute_write(self, query, parameters=None):
        if not can_write_to_database(self.connection_object):
            return {"status": False, "error": "No write permission within this database connection."}

        output = {"status": True, "error": ""}
        try:
            collection_name = query.pop('collection')
            collection = self.db[collection_name]

            if AllowedMongoDBWriteOperations.INSERT_ONE in query:
                collection.insert_one(
                    query[AllowedMongoDBWriteOperations.INSERT_ONE]
                )
            elif AllowedMongoDBWriteOperations.INSERT_MANY in query:
                collection.insert_many(
                    query[AllowedMongoDBWriteOperations.INSERT_MANY]
                )
            elif AllowedMongoDBWriteOperations.UPDATE_ONE in query:
                collection.update_one(
                    query[AllowedMongoDBHelperOperations.FILTER],
                    query[AllowedMongoDBWriteOperations.UPDATE_ONE]
                )
            elif AllowedMongoDBWriteOperations.UPDATE_MANY in query:
                collection.update_many(
                    query[AllowedMongoDBHelperOperations.FILTER],
                    query[AllowedMongoDBWriteOperations.UPDATE_MANY]
                )
            elif AllowedMongoDBWriteOperations.DELETE_ONE in query:
                collection.delete_one(
                    query[AllowedMongoDBHelperOperations.FILTER]
                )
            elif AllowedMongoDBWriteOperations.DELETE_MANY in query:
                collection.delete_many(
                    query[AllowedMongoDBHelperOperations.FILTER]
                )
            else:
                output["status"] = False
                output["error"] = f"""
                    Invalid operation specified, the allowed operations are:

                    Write Operations:
                    - {AllowedMongoDBWriteOperations.INSERT_ONE}
                    - {AllowedMongoDBWriteOperations.INSERT_MANY}
                    - {AllowedMongoDBWriteOperations.UPDATE_ONE}
                    - {AllowedMongoDBWriteOperations.UPDATE_MANY}
                    - {AllowedMongoDBWriteOperations.DELETE_ONE}
                    - {AllowedMongoDBWriteOperations.DELETE_MANY}

                    Helper Operations:
                    - {AllowedMongoDBHelperOperations.FILTER}
                    """
        except Exception as e:
            print(f"Error executing MongoDB / Write Query: {e}")
            output["status"] = False
            output["error"] = str(e)

        return output
