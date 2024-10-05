#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: remove_credit_card_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: remove_credit_card_views.py
#  Last Modified: 2024-09-26 22:43:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:11:23
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
