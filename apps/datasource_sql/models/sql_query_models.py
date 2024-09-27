from django.db import models


class CustomSQLQuery(models.Model):
    """
    CustomSQLQuery Model:
    - Purpose: Represents a custom SQL query associated with a specific SQL database connection. The model stores the query text, any associated parameters, and metadata such as the name and description of the query.
    - Key Fields:
        - `database_connection`: ForeignKey linking to the `SQLDatabaseConnection` model.
        - `name`: The name of the custom SQL query.
        - `description`: A description of the query.
        - `sql_query`: The SQL query text.
        - `parameters`: Optional JSONField for storing query parameters.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Methods:
        - `save()`: Overridden to automatically add the query to the associated database connection's custom queries.
    """

    database_connection = models.ForeignKey('datasource_sql.SQLDatabaseConnection', on_delete=models.CASCADE,
                                            related_name='custom_queries')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    sql_query = models.TextField()

    parameters = models.JSONField(blank=True, null=True)  # Optional: Use if you need to handle query parameters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.database_connection.name + ' - ' + self.database_connection.dbms_type

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # add itself to the database connection's custom queries
        super().save(force_insert, force_update, using, update_fields)
        self.database_connection.custom_queries.add(self)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Custom SQL Queries'
        verbose_name = 'Custom SQL Query'
        indexes = [
            models.Index(fields=['database_connection', 'name']),
            models.Index(fields=['database_connection', 'created_at']),
            models.Index(fields=['database_connection', 'updated_at']),
            models.Index(fields=['database_connection', 'name', 'created_at']),
            models.Index(fields=['database_connection', 'name', 'updated_at']),
        ]
