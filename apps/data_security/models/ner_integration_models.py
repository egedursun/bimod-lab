#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ner_integration_models.py
#  Last Modified: 2024-10-05 01:39:47
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

from django.db import models

from apps.data_security.utils.constant_utils import (
    NER_LANGUAGES
)


class NERIntegration(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    description = models.TextField()

    language = models.CharField(
        max_length=2,
        choices=NER_LANGUAGES,
        default='en'
    )

    encrypt_persons = models.BooleanField(default=False)  # PERSON
    encrypt_orgs = models.BooleanField(default=False)  # ORG

    encrypt_nationality_religion_political = models.BooleanField(default=False)  # NORP
    encrypt_facilities = models.BooleanField(default=False)  # FAC

    encrypt_countries_cities_states = models.BooleanField(default=False)  # GPE
    encrypt_locations = models.BooleanField(default=False)  # LOC

    encrypt_products = models.BooleanField(default=False)  # PRODUCT
    encrypt_events = models.BooleanField(default=False)  # EVENT

    encrypt_artworks = models.BooleanField(default=False)  # WORK_OF_ART
    encrypt_laws = models.BooleanField(default=False)  # LAW

    encrypt_languages = models.BooleanField(default=False)  # LANGUAGE
    encrypt_dates = models.BooleanField(default=False)  # DATE

    encrypt_times = models.BooleanField(default=False)  # TIME
    encrypt_percentages = models.BooleanField(default=False)  # PERCENT

    encrypt_money = models.BooleanField(default=False)  # MONEY
    encrypt_quantities = models.BooleanField(default=False)  # QUANTITY

    encrypt_ordinal_numbers = models.BooleanField(default=False)  # ORDINAL
    encrypt_cardinal_numbers = models.BooleanField(default=False)  # CARDINAL

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='nerintegrations_created'
    )

    def __str__(self):
        return self.name + ' (' + self.language + ')' + ' - ' + self.organization.name

    class Meta:
        verbose_name = 'NER Integration'
        verbose_name_plural = 'NER Integrations'

        unique_together = [
            [
                'organization',
                'name'
            ],
        ]

        indexes = [
            models.Index(fields=[
                'organization'
            ]),
            models.Index(fields=[
                'language'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
            models.Index(fields=[
                'name'
            ]),
            models.Index(fields=[
                'organization',
                'language'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user'
            ]),
            models.Index(fields=[
                'organization',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'updated_at'
            ]),
            models.Index(fields=[
                'organization',
                'name'
            ]),
            models.Index(fields=[
                'organization',
                'language',
                'created_by_user'
            ]),
            models.Index(fields=[
                'organization',
                'language',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'language',
                'updated_at'
            ]),
            models.Index(fields=[
                'organization',
                'language',
                'name'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user',
                'updated_at'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user',
                'name'
            ]),
            models.Index(fields=[
                'organization',
                'created_at',
                'updated_at'
            ]),
            models.Index(fields=[
                'organization',
                'created_at',
                'name'
            ]),
        ]
