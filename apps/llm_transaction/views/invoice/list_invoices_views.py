#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_invoices_views.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:57:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.llm_transaction.models import TransactionInvoice
from apps.organization.models import Organization
from web_project import TemplateLayout


class ListTransactionInvoicesView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # Get the organizations related to the current user
        organizations = Organization.objects.filter(users__in=[self.request.user]).all()
        context['invoices'] = TransactionInvoice.objects.filter(
            organization__in=organizations
        ).select_related('organization', 'responsible_user').order_by('-transaction_date')
        context['organizations'] = organizations
        return context
