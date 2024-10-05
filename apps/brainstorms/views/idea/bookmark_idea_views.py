#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: bookmark_idea_views.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
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
#  File: bookmark_idea_views.py
#  Last Modified: 2024-10-01 01:04:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 01:05:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingIdea
from apps.user_permissions.utils import PermissionNames


class BookmarkIdeaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        idea_id = self.kwargs.get('idea_id')
        idea = get_object_or_404(BrainstormingIdea, id=idea_id, created_by_user=request.user)

        ##############################
        # PERMISSION CHECK FOR - BOOKMARK_BRAINSTORMING_IDEAS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.BOOKMARK_BRAINSTORMING_IDEAS):
            messages.error(self.request, "You do not have permission to bookmark ideas.")
            return redirect('brainstorms:detail_session', session_id=idea.brainstorming_session.id)
        ##############################

        idea.is_bookmarked = not idea.is_bookmarked
        idea.save()
        status = "bookmarked" if idea.is_bookmarked else "unbookmarked"
        messages.success(request, f'Idea "{idea.idea_title}" has been {status}.')
        return redirect('brainstorms:detail_session', session_id=idea.brainstorming_session.id)
