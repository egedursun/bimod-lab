#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from auth.models import UserCreditCard


class RemoveCardView(LoginRequiredMixin, TemplateView):
    """
    Handles the removal of a user's stored credit card.

    POST:
    - Deletes the specified credit card from the user's account.
    - Displays a success message if the card is removed successfully.
    - Displays an error message if the specified card does not exist.
    """

    def post(self, request, card_id, *args, **kwargs):
        try:
            card = request.user.credit_cards.get(id=card_id)
            card.delete()
            print('[RemoveCardView.post] Credit card removed successfully.')
            messages.success(request, 'Credit card removed successfully.')
        except UserCreditCard.DoesNotExist:
            messages.error(request, 'Credit card not found.')
        return redirect('user_profile_management:list')
