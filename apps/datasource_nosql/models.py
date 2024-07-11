import json

import certifi
from django.db import models

# Create your models here.

from django.db import models
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from apps.datasource_nosql.utils import get_simplified_mongodb_schema

DBMS_CHOICES = [
    ('mongodb', 'MongoDB'),
]


class DBMSChoicesNames:
    MONGODB = 'mongodb'


class NoSQLDatabaseConnection(models.Model):
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                  related_name='nosql_database_connections',
                                  default=None, null=True)

    dbms_type = models.CharField(max_length=50, choices=DBMS_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    host = models.CharField(max_length=1000)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    db_name = models.CharField(max_length=255, blank=True, null=True)

    connection_string = models.CharField(max_length=5000, blank=True, null=True)

    is_read_only = models.BooleanField(default=True)

    schema_data_json = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='nosql_database_connections',
                                        default=None, null=True)

    custom_queries = models.ManyToManyField('CustomNoSQLQuery', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'NoSQL Database Connections'
        verbose_name = 'NoSQL Database Connection'

    def __str__(self):
        return self.dbms_type + ' - ' + self.name

    def save(self, *args, **kwargs):
        self.connection_string = (f"mongodb+srv://{self.username}:{self.password}@{self.host}/?retryWrites=true&w"
                                  f"=majority&appName=BimodTest")
        self.schema_data_json = self.retrieve_schema()
        super().save(*args, **kwargs)

    def retrieve_schema(self):
        schema = {}
        if self.dbms_type == DBMSChoicesNames.MONGODB:
            schema = self.retrieve_mongodb_schema(self.connection_string, self.db_name)
        return schema

    # Retrieve MongoDB schema data from the database
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


class CustomNoSQLQuery(models.Model):
    database_connection = models.ForeignKey(NoSQLDatabaseConnection, on_delete=models.CASCADE, related_name='queries')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    query = models.TextField()

    parameters = models.JSONField(blank=True, null=True)  # Optional: Use if you need to handle query parameters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.database_connection.name + ' - ' + self.database_connection.dbms_type

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # add itself to the database connection's custom queries
        super().save(force_insert, force_update, using, update_fields)
        self.database_connection.custom_queries.add(self)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Custom NoSQL Queries'
        verbose_name = 'Custom NoSQL Query'
