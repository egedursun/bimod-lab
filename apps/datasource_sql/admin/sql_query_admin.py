from django.contrib import admin

from apps.datasource_sql.models import CustomSQLQuery


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
