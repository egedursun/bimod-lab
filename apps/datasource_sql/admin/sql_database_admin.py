#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_database_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#
import logging

import psycopg2
from django.contrib import admin

from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_sql.utils import DBMSChoicesNames, POSTGRESQL_SCHEMA_RETRIEVAL_QUERY, \
    POSTGRESQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY, MYSQL_SCHEMA_RETRIEVAL_QUERY, MYSQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY, \
    SQL_DATABASE_ADMIN_LIST, SQL_DATABASE_ADMIN_FILTER, SQL_DATABASE_ADMIN_SEARCH
import mysql.connector


logger = logging.getLogger(__name__)


@admin.register(SQLDatabaseConnection)
class SQLDatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = SQL_DATABASE_ADMIN_LIST
    list_filter = SQL_DATABASE_ADMIN_FILTER
    search_fields = SQL_DATABASE_ADMIN_SEARCH
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.schema_data_json = self.retrieve_schema(obj)
        super().save_model(request, obj, form, change)

    def retrieve_schema(self, obj):
        schema = {}
        if obj.dbms_type == DBMSChoicesNames.POSTGRESQL:
            schema = self.retrieve_postgresql_schema(obj)
        elif obj.dbms_type == DBMSChoicesNames.MYSQL:
            schema = self.retrieve_mysql_schema(obj)
        return schema

    def retrieve_postgresql_schema(self, obj):
        schema = {}
        try:
            c = psycopg2.connect(
                dbname=obj.database_name, user=obj.username, password=obj.password, host=obj.host, port=obj.port
            )
            csr = c.cursor()
            csr.execute(POSTGRESQL_SCHEMA_RETRIEVAL_QUERY)
            tables = csr.fetchall()
            for table in tables:
                table_name = table[0]
                csr.execute(POSTGRESQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY, (table_name,))
                columns = csr.fetchall()
                schema[table_name] = [{'name': col[0], 'type': col[1]} for col in columns]
            csr.close()
            c.close()
        except Exception as e:
            logger.error(f"Error occurred while retrieving the schema: {e}")
            return {}
        return schema

    def retrieve_mysql_schema(self, obj):
        schema = {}
        try:
            c = mysql.connector.connect(
                user=obj.username, password=obj.password, host=obj.host, database=obj.database_name,
                port=obj.port
            )
            csr = c.cursor()
            csr.execute(MYSQL_SCHEMA_RETRIEVAL_QUERY)
            tables = csr.fetchall()
            for table in tables:
                table_name = table[0]
                csr.execute(MYSQL_SCHEMA_RETRIEVAL_QUERY_SUPPLY, (table_name,))
                columns = csr.fetchall()
                schema[table_name] = [{'name': col[0], 'type': col[1]} for col in columns]
            csr.close()
            c.close()
        except Exception as e:
            logger.error(f"Error occurred while retrieving the schema: {e}")
            return {}
        return schema
