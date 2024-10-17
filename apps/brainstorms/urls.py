#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.brainstorms.views import BrainstormingView_SessionCreate, BrainstormingView_SessionList, \
    BrainstormingView_SessionUpdate, BrainstormingView_SessionConfirmDelete, BrainstormingView_SessionDetail, \
    BrainstormingView_IdeaBookmark, BrainstormingView_IdeasGenerate, BrainstormingView_IdeaDelete, BrainstormingView_LevelSynthesis, BrainstormingView_PerformCompleteSynthesis, \
    BrainstormingView_IdeaDeepen

app_name = 'brainstorms'

urlpatterns = [
    path("create/", BrainstormingView_SessionCreate.as_view(
        template_name='brainstorms/session/create_brainstorming_session.html'
    ), name="create_session"),
    path("list/", BrainstormingView_SessionList.as_view(
        template_name='brainstorms/session/list_brainstorming_sessions.html'
    ), name="list_sessions"),
    path("update/<int:session_id>/", BrainstormingView_SessionUpdate.as_view(
        template_name='brainstorms/session/update_brainstorming_session.html'
    ), name="update_session"),
    path("delete/<int:session_id>/", BrainstormingView_SessionConfirmDelete.as_view(
        template_name='brainstorms/session/confirm_delete_brainstorming_session.html'
    ), name="delete_session"),
    path("session/<int:session_id>/", BrainstormingView_SessionDetail.as_view(
        template_name='brainstorms/session/detail_brainstorming_session.html'
    ), name="detail_session"),
    #####
    path('idea/bookmark/<int:idea_id>/', BrainstormingView_IdeaBookmark.as_view(), name='bookmark_idea'),
    path('idea/generate/', BrainstormingView_IdeasGenerate.as_view(), name='generate_idea'),
    path('idea/deepen/<int:idea_id>/', BrainstormingView_IdeaDeepen.as_view(), name='deepen_idea'),
    path('idea/delete/<int:idea_id>/', BrainstormingView_IdeaDelete.as_view(), name='delete_idea'),
    path('synthesis/level/create/', BrainstormingView_LevelSynthesis.as_view(), name='create_level_synthesis'),
    path('synthesis/complete/create/', BrainstormingView_PerformCompleteSynthesis.as_view(), name='create_complete_synthesis'),
]
