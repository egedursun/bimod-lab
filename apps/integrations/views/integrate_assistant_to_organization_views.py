#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_assistant_to_organization_views.py
#  Last Modified: 2024-11-05 20:12:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 20:12:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IntegrationView_IntegrateAssistantToOrganization(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #############################################################################################################
        #  USER DEFINED PROPERTIES
        #############################################################################################################
        # Configuration:
        #   i. organization
        #   ii. llm_model
        #############################################################################################################
        #  DATA SOURCE ADDITIONS (A 'DUPLICATE' of the data source connection must be created) (OPTIONAL)
        #############################################################################################################
        # i. Web Browsers (Optional) -- (WEB)
        # ii. SSH File Systems (Optional) -- (SSH)
        # iii. SQL Databases (Optional) -- (SQL)
        # iv. NoSQL Databases (Optional) -- (NOSQL)
        # v. Knowledge Bases (Optional) -- (KB + DOCS)
        # vi. Code Bases (Optional) -- (CODE)
        # vii. Media Storages (Optional) -- (MEDIA + FILES)
        # viii. ML models (Optional) -- (ML)
        # ix. Video Generators (Optional) -- (VID)
        #############################################################################################################
        # MULTI-MODALITIES (Can be later MODIFIED BY USER, but on creation content PASSED FROM BIMOD STAFF) (OPTIONAL)
        #############################################################################################################
        # i. Custom Functions
        # ii. Custom APIs
        # iii. Custom Scripts
        #############################################################################################################

        pass
