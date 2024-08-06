import psycopg2
from django.contrib import admin

from apps.datasource_sql.models import SQLDatabaseConnection, CustomSQLQuery, DBMSChoicesNames
import mysql.connector


@admin.register(SQLDatabaseConnection)
class SQLDatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assistant', 'dbms_type', 'name', 'description', 'host', 'port', 'database_name', 'username',
                    'one_time_sql_retrieval_instance_limit', 'one_time_sql_retrieval_token_limit',
                    'is_read_only', 'password', 'created_at', 'updated_at', 'created_by_user')
    list_filter = ('dbms_type', 'created_at', 'updated_at')
    search_fields = ('name', 'host', 'database_name', 'username', 'is_read_only')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('assistant', 'dbms_type', 'name', 'description', 'host', 'port', 'database_name', 'username',
                          'one_time_sql_retrieval_instance_limit', 'one_time_sql_retrieval_token_limit',
                       'is_read_only', 'password', 'schema_data_json', 'created_by_user')
        }),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

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

    # Retrieve Postgres schema data from the database
    def retrieve_postgresql_schema(self, obj):
        schema = {}
        try:
            connection = psycopg2.connect(
                dbname=obj.database_name, user=obj.username, password=obj.password, host=obj.host, port=obj.port
            )
            cursor = connection.cursor()
            cursor.execute(
                f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
                """)
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(
                    f"""
                    SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'
                    """)
                columns = cursor.fetchall()
                schema[table_name] = [{'name': col[0], 'type': col[1]} for col in columns]
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"[SQLDatabaseConnectionAdmin.retrieve_postgresql_schema] Error retrieving PostgreSQL schema: {e}")
            return {}
        return schema

    def retrieve_mysql_schema(self, obj):
        schema = {}
        try:
            connection = mysql.connector.connect(
                user=obj.username,
                password=obj.password,
                host=obj.host,
                database=obj.database_name,
                port=obj.port
            )
            cursor = connection.cursor()
            cursor.execute(
                f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys');
                """)
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(
                    f"""
                    SELECT column_name, data_type FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    """)
                columns = cursor.fetchall()
                schema[table_name] = [{'name': col[0], 'type': col[1]} for col in columns]
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"[SQLDatabaseConnectionAdmin.retrieve_mysql_schema] Error retrieving MySQL schema: {e}")
            return {}
        return schema


@admin.register(CustomSQLQuery)
class CustomSQLQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'database_connection', 'name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('database_connection', 'name', 'description', 'sql_query', 'parameters')
        }),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
