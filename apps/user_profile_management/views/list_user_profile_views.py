#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_user_profile_views.py
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

from apps.user_profile_management.forms import ProfileUpdateForm, CreditCardForm
from apps.user_profile_management.utils import infer_credit_card_type
from auth.utils.countries import COUNTRIES
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class UserProfileView_List(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['countries'] = COUNTRIES
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['credit_card_form'] = CreditCardForm()
        saved_cards = self.request.user.credit_cards.all()
        cards_with_types = []
        for card in saved_cards:
            card_type = infer_credit_card_type(card.card_number)
            cards_with_types.append({'card': card, 'card_type': card_type})
        context['saved_cards'] = cards_with_types
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        profile = request.user.profile
        if 'first_name' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                logger.info(f"User profile updated: {request.user.id}")
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('user_profile_management:list')
            else:
                logger.error(f"User profile update failed: {request.user.id}")
                messages.error(request, 'Please correct the error(s) below.')
            context = self.get_context_data()
            context['profile_form'] = profile_form
        elif 'card_number' in request.POST:
            credit_card_form = CreditCardForm(request.POST)
            if credit_card_form.is_valid():
                credit_card = credit_card_form.save(commit=False)
                credit_card.user = request.user
                credit_card.save()
                logger.info(f"User credit card added: {request.user.id}")
                messages.success(request, 'Your credit card was successfully updated!')
                return redirect('user_profile_management:list')
            else:
                logger.error(f"User credit card update failed: {request.user.id}")
                messages.error(request, 'Please correct the error(s) below.')
            context['credit_card_form'] = credit_card_form
        return self.render_to_response(context)
