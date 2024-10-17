#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_invoices_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.llm_transaction.models import TransactionInvoice
from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class Transactions_InvoiceList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orgs = Organization.objects.filter(users__in=[self.request.user]).all()
        context['invoices'] = TransactionInvoice.objects.filter(organization__in=orgs).select_related(
            'organization', 'responsible_user').order_by('-transaction_date')
        context['organizations'] = orgs
        logger.info(f"Invoices were listed by User: {self.request.user.id}.")
        return context
