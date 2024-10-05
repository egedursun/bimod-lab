#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from django.views.generic import TemplateView
from django.db.models import Sum
from web_project.template_helpers.theme import TemplateHelper
from web_project import TemplateLayout
from apps.theme.transactions.models import Transaction



class TransactionListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        transactions = self.get_annotated_transactions()
        # Update the context
        context.update(
            {
                "llm_transaction": transactions,
                "transactions_count": Transaction.objects.count(),
                "due_count": self.get_total_due(),
                "paid_count": self.get_total_paid(),
                "canceled_count": self.get_total_canceled(),
            }
        )
        TemplateHelper.map_context(context)
        return context

    def get_annotated_transactions(self):
        # Get all llm_transaction and order them by ID
        return Transaction.objects.all().order_by('id')
    def get_total_due(self):
            total_due_amount = Transaction.objects.filter(status='Due').aggregate(total_due=Sum('total'))
            return float(total_due_amount['total_due']) if total_due_amount['total_due']  is not None else 0.0

    def get_total_paid(self):
        # Calculate the total sum of 'total' field for 'Paid' llm_transaction
        total_paid_amount = Transaction.objects.filter(status='Paid').aggregate(total_paid=Sum('total'))
        return float(total_paid_amount['total_paid']) if total_paid_amount['total_paid']  is not None else 0.0

    def get_total_canceled(self):
        total_canceled_amount = Transaction.objects.filter(status='Canceled').aggregate(total_canceled=Sum('total'))
        return float(total_canceled_amount['total_canceled']) if total_canceled_amount['total_canceled']  is not None else 0.0
