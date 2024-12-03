#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_query_models.py
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

from django.db import models


class CustomSQLQuery(models.Model):
    database_connection = models.ForeignKey(
        'datasource_sql.SQLDatabaseConnection',
        on_delete=models.CASCADE,
        related_name='custom_queries'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sql_query = models.TextField()

    parameters = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.database_connection.name + ' - ' + self.database_connection.dbms_type

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

        self.database_connection.custom_queries.add(self)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Custom SQL Queries'
        verbose_name = 'Custom SQL Query'

        unique_together = [
            [
                'database_connection',
                'name'
            ],
        ]

        indexes = [
            models.Index(
                fields=[
                    'database_connection',
                    'name'
                ]
            ),
            models.Index(
                fields=[
                    'database_connection',
                    'created_at']
            ),
            models.Index(
                fields=[
                    'database_connection',
                    'updated_at']
            ),
            models.Index(
                fields=[
                    'database_connection',
                    'name',
                    'created_at']
            ),
            models.Index(
                fields=[
                    'database_connection',
                    'name',
                    'updated_at'
                ]
            ),
        ]
