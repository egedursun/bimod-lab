#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_database_models.py
#  Last Modified: 2024-10-12 13:08:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:08:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
from datetime import timedelta

import pymongo
import redis
import weaviate

from neo4j import (
    GraphDatabase
)

from elasticsearch import (
    Elasticsearch
)

from couchbase.auth import (
    PasswordAuthenticator
)

from couchbase.cluster import (
    Cluster
)

from couchbase.options import (
    QueryOptions,
    ClusterOptions,
    ClusterTimeoutOptions
)

from couchbase.exceptions import (
    CouchbaseException,
    KeyspaceNotFoundException
)

from django.db import models

from apps.datasource_nosql.utils import (
    NOSQL_DATABASE_CHOICES,
    NoSQLDatabaseChoicesNames,
    RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED,
    VALUE_TRUNCATION_PREFIX_LENGTH,
    VALUE_TRUNCATION_SUFFIX_LENGTH,
    RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED,
    DEFAULT_SCHEMA_SAMPLING_LIMIT,
    NOSQL_KV_TIMOUT_CONSTANT,
    NOSQL_CONNECT_TIMOUT_CONSTANT,
    NOSQL_QUERY_TIMOUT_CONSTANT,
    neo4j_infer_data_type,
    NEO4J_SESSION_NODE_LABELS_QUERY,
    NEO4J_PROPERTY_RETRIEVAL_QUERY,
    NEO4J_SESSION_RELATIONSHIP_TYPES_QUERY,
    NEO4J_RELATIONSHIP_RETRIEVAL_QUERY
)

from config import settings

logger = logging.getLogger(__name__)


class NoSQLDatabaseConnection(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='nosql_database_connections',
        default=None,
        null=True
    )

    nosql_db_type = models.CharField(
        max_length=500,
        choices=NOSQL_DATABASE_CHOICES
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    host = models.CharField(max_length=255)
    port = models.IntegerField(blank=True, null=True)
    bucket_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    one_time_retrieval_instance_limit = models.IntegerField(default=100)
    one_time_retrieval_token_limit = models.IntegerField(default=10_000)
    is_read_only = models.BooleanField(default=True)
    schema_data_json = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='nosql_database_connections',
        default=None,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'NoSQL Database Connections'
        verbose_name = 'NoSQL Database Connection'

        unique_together = [
            [
                'assistant',
                'name',
            ],
        ]

        indexes = [
            models.Index(
                fields=[
                    'assistant',
                    'nosql_db_type',
                    'name'
                ]
            ),
            models.Index(
                fields=[
                    'assistant',
                    'nosql_db_type',
                    'created_at'
                ]
            ),
            models.Index(
                fields=[
                    'assistant',
                    'nosql_db_type',
                    'updated_at'
                ]
            ),
            models.Index(
                fields=[
                    'assistant',
                    'nosql_db_type',
                    'name',
                    'created_at'
                ]
            ),
            models.Index(
                fields=[
                    'assistant',
                    'nosql_db_type',
                    'name',
                    'updated_at'
                ]
            ),
        ]

    def __str__(self):
        return self.nosql_db_type + ' - ' + self.name + ' - ' + self.host

    def save(self, *args, **kwargs):

        try:
            self.schema_data_json = self.retrieve_schema()

        except Exception as e:
            logger.error(f"Unable to retrieve schema for NoSQL database connection. Error: {e}")
            pass

        super().save(*args, **kwargs)

    def retrieve_schema(self):
        schema = {}

        if self.nosql_db_type == NoSQLDatabaseChoicesNames.COUCHBASE:
            schema = self.retrieve_couchbase_schema()

        elif self.nosql_db_type == NoSQLDatabaseChoicesNames.MONGODB:
            schema = self.retrieve_mongodb_schema()

        elif self.nosql_db_type == NoSQLDatabaseChoicesNames.REDIS:
            schema = self.retrieve_redis_schema()

        elif self.nosql_db_type == NoSQLDatabaseChoicesNames.ELASTICSEARCH:
            schema = self.retrieve_elasticsearch_schema()

        elif self.nosql_db_type == NoSQLDatabaseChoicesNames.NEO4J:
            schema = self.retrieve_neo4j_schema()

        elif self.nosql_db_type == NoSQLDatabaseChoicesNames.WEAVIATE:
            schema = self.retrieve_weaviate_schema()

        return schema

    @staticmethod
    def _infer_collection_schema(
        cluster,
        bucket_name,
        collection_name,
        max_value_characters_allowed=RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED,
        max_depth_infer_schema=RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED
    ):

        schema = {}
        error = None

        try:
            query = f'SELECT * FROM `{bucket_name}`._default.`{collection_name}` LIMIT {DEFAULT_SCHEMA_SAMPLING_LIMIT}'

            result = cluster.query(query, QueryOptions())

            for row in result:
                document = row.get(
                    collection_name,
                    {}
                )

                schema = NoSQLDatabaseConnection._merge_schemas(
                    schema, NoSQLDatabaseConnection._infer_fields(
                        document,
                        max_value_characters_allowed,
                        max_depth_infer_schema
                    )
                )

        except KeyspaceNotFoundException as ke:
            logger.warning(f"[_infer_collection_schema] Error: {ke}")
            pass

        except CouchbaseException as e:
            error = str(e)

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[_infer_collection_schema] Error: {error}")

        return schema

    @staticmethod
    def _merge_schemas(existing_schema, new_schema):

        for key, value in new_schema.items():

            if key in existing_schema:

                if isinstance(
                    existing_schema[key],
                    dict
                ) and isinstance(
                    value,
                    dict
                ):
                    existing_schema[key] = NoSQLDatabaseConnection._merge_schemas(
                        existing_schema[key],
                        value
                    )

                elif isinstance(
                    existing_schema[key],
                    list
                ) and isinstance(
                    value,
                    list
                ):

                    if existing_schema[key] and value:
                        existing_schema[key][0] = NoSQLDatabaseConnection._merge_schemas(
                            existing_schema[key][0], value[0])
            else:
                existing_schema[key] = value

        return existing_schema

    @staticmethod
    def _infer_fields(
        document,
        max_value_characters_allowed,
        max_depth,
        current_depth=0
    ):
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
                        inferred_schema[field] = [
                            NoSQLDatabaseConnection._infer_fields(
                                value[0],
                                max_value_characters_allowed,
                                max_depth,
                                current_depth + 1
                            )
                        ]

                    else:
                        inferred_schema[field] = ["List of nested structures (max depth reached)"]

                else:
                    inferred_schema[field] = NoSQLDatabaseConnection._truncate_value(
                        value,
                        max_value_characters_allowed
                    )

        except Exception as e:
            logger.error(f"[_infer_fields] Error: {e}")

        return inferred_schema

    @staticmethod
    def _truncate_value(
        value,
        max_value_characters_allowed
    ):

        try:
            if isinstance(
                value,
                str
            ) and len(value) > max_value_characters_allowed:
                return value[:VALUE_TRUNCATION_PREFIX_LENGTH] + "..." + value[-VALUE_TRUNCATION_SUFFIX_LENGTH:]

        except Exception as e:
            logger.error(f"[_truncate_value] Error: {e}")

        return type(value).__name__

    def retrieve_couchbase_schema(self):
        schema = {}

        error = None

        timeout_options = ClusterTimeoutOptions(
            kv_timeout=timedelta(
                seconds=NOSQL_KV_TIMOUT_CONSTANT
            ),
            connect_timeout=timedelta(
                seconds=NOSQL_CONNECT_TIMOUT_CONSTANT
            ),
            query_timeout=timedelta(
                seconds=NOSQL_QUERY_TIMOUT_CONSTANT
            )
        )

        try:
            cluster = Cluster(
                f"couchbase://{self.host}",
                ClusterOptions(
                    PasswordAuthenticator(
                        self.username,
                        self.password
                    ),
                    timeout_options=timeout_options
                ),
            )

            bucket = cluster.bucket(
                self.bucket_name
            )

            collection_manager = bucket.collections()

            for scope in collection_manager.get_all_scopes():

                for collection in scope.collections:
                    schema[collection.name] = self._infer_collection_schema(
                        cluster,
                        bucket.name,
                        collection.name
                    )

        except CouchbaseException as e:
            error = str(e)

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[retrieve_couchbase_schema] Error: {error}")

        return schema

    def retrieve_mongodb_schema(self):
        schema = {}
        error = None

        try:
            uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/"

            database_name = self.bucket_name.split('.')[0]

            client = pymongo.MongoClient(
                uri,
                serverSelectionTimeoutMS=30000
            )

            database = client[database_name]

            for collection_name in database.list_collection_names():
                collection = database[collection_name]

                collection_schema = {}

                for document in collection.find(
                    {},
                    limit=DEFAULT_SCHEMA_SAMPLING_LIMIT
                ):
                    collection_schema = NoSQLDatabaseConnection._merge_schemas(
                        collection_schema, NoSQLDatabaseConnection._infer_fields(
                            document, RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED,
                            RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED
                        )
                    )

                schema[collection_name] = collection_schema

            client.close()

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[retrieve_mongodb_schema] Error: {error}")

        return schema

    def retrieve_redis_schema(self):
        schema = {}
        error = None
        try:

            connection_params = {
                'host': self.host,
                'port': self.port,
                'socket_timeout': 10
            }

            if self.password and self.password != '':
                connection_params['password'] = self.password

            if self.username and self.username != '':
                connection_params['username'] = self.username

            client = redis.StrictRedis(
                **connection_params
            )

            cursor = 0
            while True:
                cursor, keys = client.scan(
                    cursor=cursor,
                    count=DEFAULT_SCHEMA_SAMPLING_LIMIT
                )

                for key in keys:
                    key_type = client.type(
                        key
                    ).decode()

                    if key_type == 'string':
                        schema[
                            key.decode()
                        ] = "string"

                    elif key_type == 'hash':
                        fields = client.hkeys(
                            key
                        )

                        schema[key.decode()] = {
                            field.decode(): "string" for field in fields
                        }

                    elif key_type == 'list':
                        schema[
                            key.decode()
                        ] = [
                            "list item"
                        ]

                    elif key_type == 'set':
                        schema[
                            key.decode()
                        ] = {
                            "set": "values"
                        }

                    elif key_type == 'zset':
                        schema[
                            key.decode()
                        ] = {
                            "sorted_set": "values"
                        }

                if cursor == 0:
                    break

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[retrieve_redis_schema] Error: {error}")

        return schema

    def retrieve_elasticsearch_schema(self):
        schema = {}
        try:
            client = Elasticsearch(
                hosts=[
                    {
                        "host": self.host,
                        "port": self.port,
                        "scheme": (
                            "http" if settings.ENVIRONMENT == 'local' else "https"
                        ),
                    }
                ],
                basic_auth=(
                    self.username,
                    self.password
                )
            )

            try:
                index_info = client.indices.get(
                    index=self.bucket_name
                )

                if self.bucket_name in index_info:
                    index_mappings = index_info[self.bucket_name]["mappings"].get("properties", {})

                    logger.info(f"Index mappings properties: {index_mappings}")

                    if index_mappings:
                        schema[self.bucket_name] = NoSQLDatabaseConnection._infer_fields(
                            index_mappings,
                            RETRIEVE_NOSQL_SCHEMA_MAX_VALUE_CHARACTERS_ALLOWED,
                            RETRIEVE_NOSQL_SCHEMA_MAX_DEPTH_ALLOWED
                        )

                        logger.info(f"Schema for index {self.bucket_name}: {schema[self.bucket_name]}")

                    else:
                        logger.error(
                            f"[retrieve_elasticsearch_schema] No valid properties found in the mappings for index '{self.bucket_name}'.")

                else:
                    logger.error(f"[retrieve_elasticsearch_schema] No metadata found for index '{self.bucket_name}'.")


            except Exception as ex:
                logger.error(f"[retrieve_elasticsearch_schema] Error retrieving mappings for your index: {ex}")

                return schema

        except Exception as ex:
            error = str(ex)
            logger.error(f"[retrieve_elasticsearch_schema] Error: {error}")

        return schema

    def retrieve_neo4j_schema(self):
        schema = {}
        error = None

        try:
            driver = GraphDatabase.driver(
                f"bolt://{self.host}:{self.port}",
                auth=(
                    self.username,
                    self.password
                )
            )

            with driver.session() as session:
                node_labels = session.run(NEO4J_SESSION_NODE_LABELS_QUERY)

                for record in node_labels:
                    label = record["label"]

                    schema[label] = {
                        "type": "node",
                        "properties": {}
                    }

                    property_query = NEO4J_PROPERTY_RETRIEVAL_QUERY % label

                    properties = session.run(
                        property_query
                    )

                    for prop_record in properties:
                        prop_name = prop_record["prop"]
                        sample_value = prop_record["sample"]

                        schema[label]["properties"][prop_name] = neo4j_infer_data_type(
                            value=sample_value
                        )

                relationship_types = session.run(NEO4J_SESSION_RELATIONSHIP_TYPES_QUERY)

                for record in relationship_types:
                    rel_type = record["relationshipType"]

                    schema[rel_type] = {
                        "type": "relationship",
                        "properties": {}
                    }

                    property_query = NEO4J_RELATIONSHIP_RETRIEVAL_QUERY % rel_type

                    properties = session.run(property_query)

                    for prop_record in properties:
                        prop_name = prop_record["prop"]
                        sample_value = prop_record["sample"]

                        schema[rel_type]["properties"][prop_name] = neo4j_infer_data_type(
                            value=sample_value
                        )

            driver.close()

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[retrieve_neo4j_schema] Error: {error}")

            return None

        print("NEO4J Schema: ", schema)

        return schema

    def retrieve_weaviate_schema(self):
        schema = {}
        error = None
        try:

            client = weaviate.Client(
                url=self.host,
                additional_headers={
                    "Authorization": f"Bearer {self.password}",
                }
            )

            schema_response = client.schema.get()

            for class_definition in schema_response.get(
                "classes",
                []
            ):
                class_name = class_definition["class"]

                properties = {
                    prop["name"]: prop["dataType"] for prop in class_definition.get(
                        "properties",
                        []
                    )
                }

                schema[class_name] = {
                    "type": "class",
                    "properties": properties
                }

        except Exception as ex:
            error = str(ex)

        if error:
            logger.error(f"[retrieve_weaviate_schema] Error: {error}")

        print("WEAVIATE Schema: ", schema)
        return schema
