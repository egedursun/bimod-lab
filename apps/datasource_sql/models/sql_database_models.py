from django.db import models

from apps.datasource_sql.utils import DBMS_CHOICES, DBMSChoicesNames
import psycopg2
import mysql.connector


class SQLDatabaseConnection(models.Model):
    """
    SQLDatabaseConnection Model:
    - Purpose: Represents a connection to an SQL database, storing metadata and connection details such as the DBMS type, host, port, and credentials. The model also retrieves and stores schema information for the connected database.
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `dbms_type`: The type of DBMS (e.g., PostgreSQL, MySQL).
        - `name`: The name of the database connection.
        - `description`: A description of the connection.
        - `host`, `port`, `database_name`, `username`, `password`: Fields for storing database connection details.
        - `one_time_sql_retrieval_instance_limit`, `one_time_sql_retrieval_token_limit`: Limits for SQL retrieval instances and tokens.
        - `is_read_only`: Boolean flag to indicate if the connection is read-only.
        - `schema_data_json`: JSONField for storing the database schema.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the user who created the connection.
        - `custom_queries`: ManyToManyField linking to custom SQL queries associated with the database connection.
    - Methods:
        - `save()`: Overridden to retrieve and store the database schema before saving the model.
        - `retrieve_schema()`: Determines the correct schema retrieval method based on the DBMS type.
        - `retrieve_postgresql_schema()`: Retrieves schema information from a PostgreSQL database.
        - `retrieve_mysql_schema()`: Retrieves schema information from a MySQL database.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                  related_name='sql_database_connections',
                                  default=None, null=True)

    dbms_type = models.CharField(max_length=50, choices=DBMS_CHOICES)
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
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='sql_database_connections',
                                        default=None, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'SQL Database Connections'
        verbose_name = 'SQL Database Connection'
        indexes = [
            models.Index(fields=['assistant', 'dbms_type', 'name']),
            models.Index(fields=['assistant', 'dbms_type', 'created_at']),
            models.Index(fields=['assistant', 'dbms_type', 'updated_at']),
            models.Index(fields=['assistant', 'dbms_type', 'name', 'created_at']),
            models.Index(fields=['assistant', 'dbms_type', 'name', 'updated_at']),
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

    # Retrieve Postgres schema data from the database
    def retrieve_postgresql_schema(self):
        schema = {}
        try:
            connection = psycopg2.connect(
                dbname=self.database_name,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port
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
            print(f"[SQLDatabaseConnection.save] Error retrieving PostgreSQL schema: {e}")
            return {}
        return schema

    def retrieve_mysql_schema(self):
        schema = {}
        try:
            connection = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                database=self.database_name,
                port=self.port
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
            print(f"[SQLDatabaseConnection.retrieve_mysql_schema] Error retrieving MySQL schema: {e}")
            return {}
        return schema
