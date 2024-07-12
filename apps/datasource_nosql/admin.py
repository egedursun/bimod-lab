import json

import certifi
from django.contrib import admin
from pymongo import MongoClient

from .models import NoSQLDatabaseConnection, CustomNoSQLQuery, NoSQLDBMSChoicesNames
from .utils import get_simplified_mongodb_schema


@admin.register(NoSQLDatabaseConnection)
class NoSQLDatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'dbms_type', 'host', 'db_name', 'schema_data_json',
                    'is_read_only', 'created_at', 'updated_at')
    list_filter = ('dbms_type', 'db_name', 'is_read_only', 'created_at')
    search_fields = ('name', 'host', 'db_name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'connection_string')
    list_editable = ('schema_data_json',)

    fieldsets = (
        (None, {
            'fields': ('assistant', 'dbms_type', 'db_name', 'name', 'description', 'host', 'username', 'password',
                       'is_read_only')
        }),
        ('Connection Details', {
            'fields': ('connection_string', 'schema_data_json')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.connection_string = (f"mongodb+srv://{obj.username}:{obj.password}@{obj.host}/?retryWrites=true&w"
                                 f"=majority&appName=BimodTest")
        obj.schema_data_json = self.retrieve_schema(obj)
        super().save_model(request, obj, form, change)

    @staticmethod
    def retrieve_schema(obj):
        schema = {}
        if obj.dbms_type == NoSQLDBMSChoicesNames.MONGODB:
            schema = obj.retrieve_mongodb_schema(obj.connection_string, obj.db_name)
        return schema

    @staticmethod
    def retrieve_mongodb_schema(connection_string, db_name):
        schema = {}
        try:
            client = MongoClient(connection_string, tlsCAFile=certifi.where())
            db = client.get_database(db_name)
            collections = db.list_collection_names()
            for collection in collections:
                collection_data = db[collection]
                sample_document = collection_data.find_one()
                if sample_document:
                    schema[collection] = get_simplified_mongodb_schema(sample_document)
        except Exception as e:
            print(f"Error retrieving MongoDB schema: {e}")
            return {}
        return schema

@admin.register(CustomNoSQLQuery)
class CustomNoSQLQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'database_connection', 'created_at', 'updated_at')
    list_filter = ('database_connection', 'created_at')
    search_fields = ('name', 'description', 'query')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('database_connection', 'name', 'description', 'query', 'parameters')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
