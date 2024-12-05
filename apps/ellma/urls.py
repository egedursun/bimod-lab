#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-30 17:28:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:28:26
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

from apps.ellma.views import (
    EllmaScriptView_CreateScript,
    EllmaScriptView_DeleteScript,
    EllmaScriptView_ScriptEditor,
    EllmaScriptView_CompileScript,
    EllmaScriptView_ManageScripts
)

app_name = 'ellma'

urlpatterns = [

    # Headless, templateless POST views

    path(
        'create/',
        EllmaScriptView_CreateScript.as_view(

        ),
        name='create-script'
    ),

    path(
        'delete/<int:pk>/',
        EllmaScriptView_DeleteScript.as_view(

        ),
        name='delete-script'
    ),

    path(
        'compile/<int:pk>/',
        EllmaScriptView_CompileScript.as_view(

        ),
        name='compile-script'
    ),

    # TemplateView based views

    path(
        'editor/<int:pk>/',
        EllmaScriptView_ScriptEditor.as_view(
            template_name='ellma/ellma_script_editor.html'
        ),
        name='script-editor'
    ),

    path(
        'manage/',
        EllmaScriptView_ManageScripts.as_view(
            template_name='ellma/ellma_script_manager.html'
        ),
        name='manage-scripts'
    ),
]
