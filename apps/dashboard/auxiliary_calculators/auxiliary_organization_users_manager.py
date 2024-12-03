#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_organization_users_manager.py
#  Last Modified: 2024-10-09 21:47:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:47:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.utils import timezone


class AuxiliaryOrganizationUsersManager:

    @staticmethod
    def calculate_total_users_per_organizations(orgs):

        org_users = {}

        for org in orgs:
            org_users[org.name] = org.users.count()

        return org_users

    @staticmethod
    def calculate_latest_registered_users_per_organizations(
        orgs,
        n_days
    ):

        org_users = {}

        for org in orgs:
            org_users[org.name] = org.users.filter(
                date_joined__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            ).count()

        return org_users
