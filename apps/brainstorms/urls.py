#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
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
#  File: urls.py
#  Last Modified: 2024-09-30 23:59:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 23:59:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.urls import path

from apps.brainstorms.views import CreateBrainstormingSessionView, ListBrainstormingSessionsView, \
    UpdateBrainstormingSessionView, DeleteBrainstormingSessionView, BrainstormingSessionDetailView, \
    BookmarkIdeaView, GenerateIdeasView, DeleteIdeaView, CreateLevelSynthesisView, CreateCompleteSynthesisView

app_name = 'brainstorms'

urlpatterns = [
    path("create/", CreateBrainstormingSessionView.as_view(
        template_name='brainstorms/session/create_brainstorming_session.html'
    ), name="create_session"),
    path("list/", ListBrainstormingSessionsView.as_view(
        template_name='brainstorms/session/list_brainstorming_sessions.html'
    ), name="list_sessions"),
    path("update/<int:session_id>/", UpdateBrainstormingSessionView.as_view(
        template_name='brainstorms/session/update_brainstorming_session.html'
    ), name="update_session"),
    path("delete/<int:session_id>/", DeleteBrainstormingSessionView.as_view(
        template_name='brainstorms/session/confirm_delete_brainstorming_session.html'
    ), name="delete_session"),
    path("session/<int:session_id>/", BrainstormingSessionDetailView.as_view(
        template_name='brainstorms/session/detail_brainstorming_session.html'
    ), name="detail_session"),
    #####
    path('idea/bookmark/<int:idea_id>/', BookmarkIdeaView.as_view(), name='bookmark_idea'),
    path('idea/generate/', GenerateIdeasView.as_view(), name='generate_idea'),
    path('idea/delete/<int:idea_id>/', DeleteIdeaView.as_view(), name='delete_idea'),
    path('synthesis/level/create/', CreateLevelSynthesisView.as_view(), name='create_level_synthesis'),
    path('synthesis/complete/create/', CreateCompleteSynthesisView.as_view(), name='create_complete_synthesis'),
]
