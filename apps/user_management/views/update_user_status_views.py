#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_user_status_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames


@method_decorator(require_POST, name='dispatch')
class UserManagementView_UserUpdateStatus(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        is_active = request.POST.get('is_active') == 'true'

        ##############################
        # PERMISSION CHECK FOR - UPDATE_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_USERS):
            messages.error(self.request, "You do not have permission to update/modify user accounts.")
            return redirect('user_management:list')
        ##############################

        try:
            user = User.objects.get(id=user_id)
            user.profile.is_active = is_active
            user.profile.save()
            return redirect('user_management:list')
        except Exception as e:
            messages.error(request, f'Error updating user status')
            return redirect('user_management:list')
