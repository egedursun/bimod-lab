#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_task_labels.py
#  Last Modified: 2024-10-27 00:33:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:33:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanBoard,
    MetaKanbanTaskLabel
)

from apps.metakanban.utils import (
    META_KANBAN_TASK_LABEL_COLOR_CHOICES
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaKanbanView_LabelList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_METAKANBAN_TASK_LABEL
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_METAKANBAN_TASK_LABEL
        ):
            messages.error(self.request, "You do not have permission to list kanban task labels.")
            return context
        ##############################

        board_id = self.kwargs.get("board_id")

        context['board'] = get_object_or_404(
            MetaKanbanBoard,
            id=board_id
        )

        context['labels'] = MetaKanbanTaskLabel.objects.filter(
            board_id=board_id
        ).order_by('-created_at')

        context['color_choices'] = META_KANBAN_TASK_LABEL_COLOR_CHOICES

        return context
