#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_database_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from django.db import models

from apps.datasource_sql.utils import (
    DBMS_CHOICES,
    DBMSChoicesNames,
    POSTGRESQL_SCHEMA_RETRIEVAL_QUERY,
    POSTGRESQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY,
    MYSQL_SCHEMA_RETRIEVAL_QUERY,
    MYSQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY
)

import psycopg2
import mysql.connector

logger = logging.getLogger(__name__)


class SQLDatabaseConnection(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='sql_database_connections',
        default=None,
        null=True
    )

    dbms_type = models.CharField(
        max_length=50,
        choices=DBMS_CHOICES
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    database_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    one_time_sql_retrieval_instance_limit = models.IntegerField(default=100)
    one_time_sql_retrieval_token_limit = models.IntegerField(default=10_000)

    is_read_only = models.BooleanField(default=True)
    schema_data_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='sql_database_connections',
        default=None,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

        verbose_name_plural = 'SQL Database Connections'
        verbose_name = 'SQL Database Connection'

        unique_together = [
            [
                "assistant",
                "host",
                "port",
                "database_name"
            ],
        ]

        indexes = [
            models.Index(fields=[
                'assistant',
                'dbms_type',
                'name'
            ]),
            models.Index(fields=[
                'assistant',
                'dbms_type',
                'created_at'
            ]),
            models.Index(fields=[
                'assistant',
                'dbms_type',
                'updated_at'
            ]),
            models.Index(fields=[
                'assistant',
                'dbms_type',
                'name',
                'created_at'
            ]),
            models.Index(fields=[
                'assistant',
                'dbms_type',
                'name',
                'updated_at'
            ]),
        ]

    def __str__(self):
        return self.dbms_type + ' - ' + self.name

    def save(self, *args, **kwargs):
        self.schema_data_json = self.retrieve_schema()

        super().save(*args, **kwargs)

    def retrieve_schema(self):
        schema = {}

        if self.dbms_type == DBMSChoicesNames.POSTGRESQL:
            schema = self.retrieve_postgresql_schema()

        elif self.dbms_type == DBMSChoicesNames.MYSQL:
            schema = self.retrieve_mysql_schema()

        return schema

    def retrieve_postgresql_schema(self):
        schema = {}
        try:
            c = psycopg2.connect(
                dbname=self.database_name,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                connect_timeout=10
            )

            crs = c.cursor()

            crs.execute(
                POSTGRESQL_SCHEMA_RETRIEVAL_QUERY
            )

            tables = crs.fetchall()

            for table in tables:
                table_name = table[0]
                crs.execute(
                    POSTGRESQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY,
                    (table_name,)
                )

                columns = crs.fetchall()

                schema[table_name] = [
                    {
                        'name': col[0], 'type': col[1]
                    } for col in columns
                ]

            crs.close()
            c.close()

            logger.info(f"Schema retrieved: {schema}")

        except Exception as e:
            logger.error(f"Error occurred while retrieving the schema: {e}")
            return {}

        return schema

    def retrieve_mysql_schema(self):
        schema = {}
        try:
            c = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                database=self.database_name,
                port=self.port,
                connection_timeout=10
            )

            crs = c.cursor()

            crs.execute(
                MYSQL_SCHEMA_RETRIEVAL_QUERY
            )

            tables = crs.fetchall()

            for table in tables:
                table_name = table[0]

                crs.execute(
                    MYSQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY,
                    (table_name,)
                )

                columns = crs.fetchall()

                schema[table_name] = [
                    {
                        'name': col[0], 'type': col[1]
                    } for col in columns
                ]

            crs.close()
            c.close()

            logger.info(f"Schema retrieved: {schema}")

        except Exception as e:
            logger.error(f"Error occurred while retrieving the schema: {e}")

            return {}

        return schema
