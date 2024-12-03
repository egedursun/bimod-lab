#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_ner_integration_views.py
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

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.data_security.models import NERIntegration
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NERView_IntegrationUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        try:
            ner_integration = NERIntegration.objects.get(
                id=self.kwargs['pk']
            )

            context['ner_integration'] = ner_integration
            context['organizations'] = Organization.objects.filter(
                users__in=[self.request.user]
            )

            context['boolean_fields'] = [
                {
                    'name': 'encrypt_persons',
                    'label': 'Encrypt Persons (PERSON)',
                    'value': ner_integration.encrypt_persons},
                {
                    'name': 'encrypt_orgs',
                    'label': 'Encrypt Organizations (ORG)',
                    'value': ner_integration.encrypt_orgs},
                {
                    'name': 'encrypt_nationality_religion_political',
                    'label': 'Encrypt NORP',
                    'value': ner_integration.encrypt_nationality_religion_political},
                {
                    'name': 'encrypt_facilities',
                    'label': 'Encrypt Facilities (FAC)',
                    'value': ner_integration.encrypt_facilities},
                {
                    'name': 'encrypt_countries_cities_states',
                    'label': 'Encrypt GPE',
                    'value': ner_integration.encrypt_countries_cities_states},
                {
                    'name': 'encrypt_locations',
                    'label': 'Encrypt Locations (LOC)',
                    'value': ner_integration.encrypt_locations},
                {
                    'name': 'encrypt_products',
                    'label': 'Encrypt Products (PRODUCT)',
                    'value': ner_integration.encrypt_products},
                {
                    'name': 'encrypt_events',
                    'label': 'Encrypt Events (EVENT)', 'value': ner_integration.encrypt_events},
                {
                    'name': 'encrypt_artworks',
                    'label': 'Encrypt Work of Art (WORK_OF_ART)',
                    'value': ner_integration.encrypt_artworks},
                {
                    'name': 'encrypt_laws',
                    'label': 'Encrypt Laws (LAW)', 'value': ner_integration.encrypt_laws},
                {
                    'name': 'encrypt_languages',
                    'label': 'Encrypt Languages (LANGUAGE)',
                    'value': ner_integration.encrypt_languages},
                {
                    'name': 'encrypt_dates',
                    'label': 'Encrypt Dates (DATE)', 'value': ner_integration.encrypt_dates
                },
                {
                    'name': 'encrypt_times',
                    'label': 'Encrypt Times (TIME)', 'value': ner_integration.encrypt_times},
                {
                    'name': 'encrypt_percentages',
                    'label': 'Encrypt Percentages (PERCENT)',
                    'value': ner_integration.encrypt_percentages},
                {
                    'name': 'encrypt_money',
                    'label': 'Encrypt Money (MONEY)', 'value': ner_integration.encrypt_money},
                {
                    'name': 'encrypt_quantities',
                    'label': 'Encrypt Quantities (QUANTITY)',
                    'value': ner_integration.encrypt_quantities},
                {
                    'name': 'encrypt_ordinal_numbers',
                    'label': 'Encrypt Ordinal Numbers (ORDINAL)',
                    'value': ner_integration.encrypt_ordinal_numbers},
                {
                    'name': 'encrypt_cardinal_numbers',
                    'label': 'Encrypt Cardinal Numbers (CARDINAL)',
                    'value': ner_integration.encrypt_cardinal_numbers
                },
            ]
        except Exception as e:
            logger.error(f"User: {self.request.user} - NER Integration: {self.kwargs['pk']} - Update Error: {e}")
            messages.error(self.request, 'An error occurred while listing update page for NER Integration.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_DATA_SECURITY
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_DATA_SECURITY
        ):
            messages.error(self.request, "You do not have permission to update data security layers.")
            return redirect('data_security:list_ner_integrations')
        ##############################

        try:
            ner_integration = NERIntegration.objects.get(
                id=self.kwargs['pk']
            )

            ner_integration.encrypt_persons = request.POST.get('encrypt_persons') == 'True'
            ner_integration.encrypt_orgs = request.POST.get('encrypt_orgs') == 'True'

            ner_integration.encrypt_nationality_religion_political = request.POST.get(
                'encrypt_nationality_religion_political'
            ) == 'True'

            ner_integration.encrypt_facilities = request.POST.get('encrypt_facilities') == 'True'

            ner_integration.encrypt_countries_cities_states = request.POST.get(
                'encrypt_countries_cities_states'
            ) == 'True'

            ner_integration.encrypt_locations = request.POST.get('encrypt_locations') == 'True'
            ner_integration.encrypt_products = request.POST.get('encrypt_products') == 'True'
            ner_integration.encrypt_events = request.POST.get('encrypt_events') == 'True'
            ner_integration.encrypt_artworks = request.POST.get('encrypt_artworks') == 'True'
            ner_integration.encrypt_laws = request.POST.get('encrypt_laws') == 'True'

            ner_integration.encrypt_languages = request.POST.get('encrypt_languages') == 'True'
            ner_integration.encrypt_dates = request.POST.get('encrypt_dates') == 'True'
            ner_integration.encrypt_times = request.POST.get('encrypt_times') == 'True'
            ner_integration.encrypt_percentages = request.POST.get('encrypt_percentages') == 'True'

            ner_integration.encrypt_money = request.POST.get('encrypt_money') == 'True'
            ner_integration.encrypt_quantities = request.POST.get('encrypt_quantities') == 'True'
            ner_integration.encrypt_ordinal_numbers = request.POST.get('encrypt_ordinal_numbers') == 'True'
            ner_integration.encrypt_cardinal_numbers = request.POST.get('encrypt_cardinal_numbers') == 'True'

            ner_integration.name = request.POST.get('name')
            ner_integration.description = request.POST.get('description')
            ner_integration.language = request.POST.get('language')
            organization_id = request.POST.get('organization')

            if organization_id:
                ner_integration.organization_id = organization_id
            ner_integration.save()

        except Exception as e:
            logger.error(f"User: {request.user} - NER Integration: {self.kwargs['pk']} - Update Error: {e}")
            messages.error(request, 'An error occurred while updating NER Integration.')

            return redirect('data_security:list_ner_integrations')

        logger.info(f"User: {request.user} - NER Integration: {ner_integration.name} - Updated.")

        return redirect('data_security:update_ner_integration', pk=ner_integration.id)
