#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: remove_credit_card_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from auth.models import UserCreditCard


logger = logging.getLogger(__name__)


class UserProfileView_CreditCardRemove(LoginRequiredMixin, TemplateView):
    def post(self, request, card_id, *args, **kwargs):
        try:
            card = request.user.credit_cards.get(id=card_id)
            card.delete()
            logger.info(f"Credit card removed by User: {request.user.id}.")
            messages.success(request, 'Credit card removed successfully.')
        except UserCreditCard.DoesNotExist:
            logger.error(f"Credit card not found: {card_id}")
            messages.error(request, 'Credit card not found.')
        return redirect('user_profile_management:list')
