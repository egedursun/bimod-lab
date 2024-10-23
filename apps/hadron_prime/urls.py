#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-17 21:40:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:40:20
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

from apps.hadron_prime.views import (HadronPrimeView_CreateHadronSystem, HadronPrimeView_DeleteHadronSystem,
                                     HadronPrimeView_UpdateHadronSystem, HadronPrimeView_ListHadronSystem,
                                     HadronPrimeView_CreateHadronNode, HadronPrimeView_DeleteHadronTopic,
                                     HadronPrimeView_CreateHadronTopic, HadronPrimeView_DeleteHadronNode,
                                     HadronPrimeView_UpdateHadronNode, HadronPrimeView_UpdateHadronTopic,
                                     HadronPrimeView_TriggerActiveHadronNode, HadronPrimeView_DetailHadronNode,
                                     HadronPrimeView_DetailHadronSystem, HadronPrimeView_DetailHadronTopic,
                                     HadronPrimeView_RegenerateNodeApiKey, HadronPrimeView_DeleteAllNodeExecutionLogs,
                                     HadronPrimeView_DeleteAllNodePublishHistoryLogs,
                                     HadronPrimeView_DeleteAllTopicMessages, HadronPrimeView_DeleteAllNodeSASELogs,
                                     HadronPrimeView_TriggerActiveHadronNodeViaForm,
                                     HadronPrimeView_DeleteAllNodeSpeechLogs, HadronPrimeView_SpeakWithHadronNode,
                                     HadronPrimeView_SpeakWithHadronNodeViaForm)

app_name = "hadron_prime"

urlpatterns = [
    path("hadron_system/list/", HadronPrimeView_ListHadronSystem.as_view(
        template_name="hadron_prime/system/list_hadron_systems.html"
    ), name="list_hadron_system"),
    path("hadron_system/create/", HadronPrimeView_CreateHadronSystem.as_view(
        template_name="hadron_prime/system/create_hadron_system.html"
    ), name="create_hadron_system"),
    path("hadron_system/delete/<int:pk>/", HadronPrimeView_DeleteHadronSystem.as_view(
        template_name="hadron_prime/system/confirm_delete_hadron_system.html"
    ), name="delete_hadron_system"),
    path("hadron_system/update/<int:pk>/", HadronPrimeView_UpdateHadronSystem.as_view(
        template_name="hadron_prime/system/update_hadron_system.html"
    ), name="update_hadron_system"),
    path("hadron_system/detail/<int:pk>/", HadronPrimeView_DetailHadronSystem.as_view(
        template_name="hadron_prime/system/detail_hadron_system.html"), name="detail_hadron_system"),

    path("hadron_topic/create/", HadronPrimeView_CreateHadronTopic.as_view(
        template_name="hadron_prime/topic/create_hadron_topic.html"
    ), name="create_hadron_topic"),
    path("hadron_topic/delete/<int:pk>/", HadronPrimeView_DeleteHadronTopic.as_view(
        template_name="hadron_prime/topic/confirm_delete_hadron_topic.html"
    ), name="delete_hadron_topic"),
    path("hadron_topic/update/<int:pk>/", HadronPrimeView_UpdateHadronTopic.as_view(
        template_name="hadron_prime/topic/update_hadron_topic.html"
    ), name="update_hadron_topic"),
    path("hadron_topic/detail/<int:pk>/", HadronPrimeView_DetailHadronTopic.as_view(
        template_name="hadron_prime/topic/detail_hadron_topic.html"), name="detail_hadron_topic"),

    path("hadron_node/create/", HadronPrimeView_CreateHadronNode.as_view(
        template_name="hadron_prime/node/create_hadron_node.html"
    ), name="create_hadron_node"),
    path("hadron_node/delete/<int:pk>/", HadronPrimeView_DeleteHadronNode.as_view(
        template_name="hadron_prime/node/confirm_delete_hadron_node.html"
    ), name="delete_hadron_node"),
    path("hadron_node/update/<int:pk>/", HadronPrimeView_UpdateHadronNode.as_view(
        template_name="hadron_prime/node/update_hadron_node.html"
    ), name="update_hadron_node"),
    path("hadron_node/detail/<int:pk>/", HadronPrimeView_DetailHadronNode.as_view(
        template_name="hadron_prime/node/detail_hadron_node.html"), name="detail_hadron_node"),
    path("hadron_node/regenerate_api_key/<int:pk>/", HadronPrimeView_RegenerateNodeApiKey.as_view(),
         name="regenerate_node_api_key"),

    path("hadron_Node/activate/manual/<int:pk>/<str:hash>/", HadronPrimeView_TriggerActiveHadronNodeViaForm.as_view(),
         name="trigger_activate_hadron_node_via_form"),
    path("hadron_node/activate/<int:pk>/<str:hash>/", HadronPrimeView_TriggerActiveHadronNode.as_view(),
         name="trigger_activate_hadron_node"),
    path("hadron_Node/activate/speak/<int:pk>/<str:hash>/", HadronPrimeView_SpeakWithHadronNodeViaForm.as_view(),
         name="speak_with_hadron_node_via_form"),
    path("hadron_node/speak/<int:pk>/<str:hash>/", HadronPrimeView_SpeakWithHadronNode.as_view(),
         name="speak_with_hadron_node"),

    path("hadron_node/delete_all_execution_logs/<int:pk>/", HadronPrimeView_DeleteAllNodeExecutionLogs.as_view(),
         name="delete_all_execution_logs"),
    path("hadron_node/delete_all_publish_history_logs/<int:pk>/",
         HadronPrimeView_DeleteAllNodePublishHistoryLogs.as_view(),
         name="delete_all_publish_history_logs"),
    path("hadron_node/delete_all_sase_logs/<int:pk>/", HadronPrimeView_DeleteAllNodeSASELogs.as_view(),
         name="delete_all_sase_logs"),
    path("hadron_topic/delete_all_messages/<int:pk>/", HadronPrimeView_DeleteAllTopicMessages.as_view(),
         name="delete_all_messages"),
    path("hadron_node/delete_all_speech_logs/<int:pk>/", HadronPrimeView_DeleteAllNodeSpeechLogs.as_view(),
         name="delete_all_speech_logs"),
]
