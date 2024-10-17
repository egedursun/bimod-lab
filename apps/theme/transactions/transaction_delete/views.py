#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView
from django.contrib import messages
from apps.theme.transactions.models import Transaction
from django.contrib.auth.mixins import PermissionRequiredMixin

class TransactionDeleteView(PermissionRequiredMixin, DeleteView):

    permission_required = ("llm_transaction.delete_transaction")

    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, id=pk)
        transaction.delete()
        messages.success(request, 'Transaction Deleted')
        return redirect('llm_transaction')
