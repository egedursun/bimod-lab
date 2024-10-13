#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: nosql_database_admin.py
#  Last Modified: 2024-10-12 13:08:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:08:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.exceptions import CouchbaseException, KeyspaceNotFoundException
from couchbase.options import ClusterOptions, QueryOptions, ClusterTimeoutOptions
from django.contrib import admin

from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_nosql.utils import NOSQL_DATABASE_ADMIN_LIST, NOSQL_DATABASE_ADMIN_FILTER, \
    NOSQL_DATABASE_ADMIN_SEARCH, NoSQLDatabaseChoicesNames, RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED, \
    RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED, DEFAULT_SCHEMA_SAMPLING_LIMIT, VALUE_TRUNCATION_PREFIX_LENGTH, \
    VALUE_TRUNCATION_SUFFIX_LENGTH, NOSQL_KV_TIMOUT_CONSTANT, NOSQL_CONNECT_TIMOUT_CONSTANT, \
    NOSQL_QUERY_TIMOUT_CONSTANT


@admin.register(NoSQLDatabaseConnection)
class NoSQLDatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = NOSQL_DATABASE_ADMIN_LIST
    list_filter = NOSQL_DATABASE_ADMIN_FILTER
    search_fields = NOSQL_DATABASE_ADMIN_SEARCH
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.schema_data_json = self.retrieve_schema(obj)
        super().save_model(request, obj, form, change)

    def retrieve_schema(self, obj):
        schema = {}
        if obj.nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:
            schema = self.retrieve_couchbase_schema(obj=obj)
        return schema

    @staticmethod
    def _infer_collection_schema(cluster, bucket_name, collection_name,
                                 max_value_characters_allowed=RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED,
                                 max_depth_infer_schema=RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED):
        schema = {}
        try:
            query = f'SELECT * FROM `{bucket_name}`._default.`{collection_name}` LIMIT {DEFAULT_SCHEMA_SAMPLING_LIMIT}'
            result = cluster.query(query, QueryOptions())
            for row in result:
                document = row.get(collection_name, {})
                schema = NoSQLDatabaseConnection._merge_schemas(
                    schema, NoSQLDatabaseConnection._infer_fields(
                        document, max_value_characters_allowed, max_depth_infer_schema)
                )

        except KeyspaceNotFoundException as ke:
            pass
        except CouchbaseException as e:
            print(f"[_infer_collection_schema] Error: {e}")
        except Exception as ex:
            print(f"[_infer_collection_schema] Unexpected error: {ex}")
        return schema

    @staticmethod
    def _merge_schemas(existing_schema, new_schema):
        for key, value in new_schema.items():
            if key in existing_schema:
                if isinstance(existing_schema[key], dict) and isinstance(value, dict):
                    existing_schema[key] = NoSQLDatabaseConnection._merge_schemas(existing_schema[key], value)
                elif isinstance(existing_schema[key], list) and isinstance(value, list):
                    if existing_schema[key] and value:
                        existing_schema[key][0] = NoSQLDatabaseConnection._merge_schemas(
                            existing_schema[key][0], value[0])
            else:
                existing_schema[key] = value
        return existing_schema

    @staticmethod
    def _infer_fields(document, max_value_characters_allowed, max_depth, current_depth=0):
        inferred_schema = {}
        try:
            for field, value in document.items():
                if isinstance(value, dict):
                    if current_depth < max_depth:
                        inferred_schema[field] = NoSQLDatabaseConnection._infer_fields(
                            value, max_value_characters_allowed, max_depth, current_depth + 1)
                    else:
                        inferred_schema[field] = "Nested structure (max depth reached)"
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    if current_depth < max_depth:
                        inferred_schema[field] = [NoSQLDatabaseConnection._infer_fields(
                            value[0], max_value_characters_allowed, max_depth, current_depth + 1)]
                    else:
                        inferred_schema[field] = ["List of nested structures (max depth reached)"]
                else:
                    inferred_schema[field] = NoSQLDatabaseConnection._truncate_value(
                        value, max_value_characters_allowed)
        except Exception as e:
            print(f"[_infer_fields] Error: {e}")
        return inferred_schema

    @staticmethod
    def _truncate_value(value, max_value_characters_allowed):
        try:
            if isinstance(value, str) and len(value) > max_value_characters_allowed:
                return value[:VALUE_TRUNCATION_PREFIX_LENGTH] + "..." + value[-VALUE_TRUNCATION_SUFFIX_LENGTH:]
        except Exception as e:
            print(f"[_truncate_value] Error: {e}")
        return type(value).__name__

    def retrieve_couchbase_schema(self, obj):
        schema = {}
        timeout_options = ClusterTimeoutOptions(
            kv_timeout=timedelta(seconds=NOSQL_KV_TIMOUT_CONSTANT),
            connect_timeout=timedelta(seconds=NOSQL_CONNECT_TIMOUT_CONSTANT),
            query_timeout=timedelta(seconds=NOSQL_QUERY_TIMOUT_CONSTANT)
        )
        try:
            cluster = Cluster(
                f"couchbase://{obj.host}",
                ClusterOptions(
                    PasswordAuthenticator(obj.username, obj.password), timeout_options=timeout_options),
            )
            bucket = cluster.bucket(obj.bucket_name)
            collection_manager = bucket.collections()
            for scope in collection_manager.get_all_scopes():
                for collection in scope.collections:
                    schema[collection.name] = self._infer_collection_schema(cluster, bucket.name, collection.name)
        except CouchbaseException as e:
            print("[retrieve_couchbase_schema] Error: ", e)
        except Exception as ex:
            print(f"[retrieve_couchbase_schema] Unexpected error: {ex}")
        return schema
