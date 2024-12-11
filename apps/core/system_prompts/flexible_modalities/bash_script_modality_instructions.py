#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_scripts_multimodality_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json

from apps.assistants.models import Assistant

from apps.mm_scripts.models import (
    CustomScriptReference
)


def build_scripts_multi_modality_prompt(assistant: Assistant):
    script_refs = CustomScriptReference.objects.filter(
        assistant=assistant
    )

    response_prompt = """
            ### **CUSTOM SCRIPTS:**

            '''
            """

    for i, custom_script_reference in enumerate(script_refs):
        custom_script = custom_script_reference.custom_script

        response_prompt += f"""
                [Custom Script Reference ID: {custom_script_reference.id}]
                    Script Name: {custom_script.name}
                    Script Description: {custom_script.description}
                    Step Guide (What the script does step-by-step):
                    '''
                    {json.dumps(custom_script.script_step_guide, indent=4)}
                    '''
                """

    response_prompt += """
            -------

            '''

            #### **THE NOTE ABOUT THE FORMAT OF THE AVAILABLE SOURCES:**

                - This information is shared for you to have a more clear understanding about the custom scripts.
                    You can use this information to execute the custom scripts properly by providing the necessary
                    inputs and use the script ID more easily.

            - *Script Name:*
                - The script name field will be shared as a string that represents the name of the script.

            - *Script Description:*
                - The script description field will be shared as a string that represents the description of it.

            - *Script Step Guide:*
                - The step guide field will be shared as an ordered list where each item represents a step in the
                    execution process. Each item means to describe a step within the script for you to better
                    understand what is the purpose of the script. Here is an example:
                    '''
                    [
                        "Moves to the Desktop folder.",
                        "Creates a folder named 'Outdated' in Desktop.",
                        "Checks which files are older than 30 days.",
                        "Moves the outdated files to 'Outdated' folder.",
                        "Deletes the empty folders in Desktop."
                    ]
                    '''

            -------

            #### **NOTE**: You might need to choose a Script you would like to use depending on the use case. You can
            then receive the contents of the script to be able to operate on it and help the user. For example, the
            user can ask you to put the script on a SSH File System, and then run it, and you can choose a relevant
            script from your available Scripts, take the content, and create a file within the SSH file system, then
            run it. This will be a process handled by YOU, so you need to pick a script ID from the available Scripts
            and then use the tool to retrieve the contents of it. Then you should understand this content, and put it
            yourself in a file on the SSH file system by using relevant tool(s).

            -------
            """

    return response_prompt


def build_semantor_scripts_multi_modality_prompt(
    temporary_sources: dict
):
    script_refs = temporary_sources.get("tools").get("scripts")

    response_prompt = """
            ### **CUSTOM SCRIPTS:**

            '''
            """

    for i, custom_script_reference in enumerate(script_refs):
        custom_script = custom_script_reference.custom_script

        response_prompt += f"""
                [Custom Script Reference ID: {custom_script_reference.id}]
                    Script Name: {custom_script.name}
                    Script Description: {custom_script.description}
                    Step Guide (What the script does step-by-step):
                    '''
                    {json.dumps(custom_script.script_step_guide, indent=4)}
                    '''
                """

    response_prompt += """
            -------

            '''

            #### **THE NOTE ABOUT THE FORMAT OF THE AVAILABLE SOURCES:**

                - This information is shared for you to have a more clear understanding about the custom scripts.
                    You can use this information to execute the custom scripts properly by providing the necessary
                    inputs and use the script ID more easily.

            - *Script Name:*
                - The script name field will be shared as a string that represents the name of the script.

            - *Script Description:*
                - The script description field will be shared as a string that represents the description of it.

            - *Script Step Guide:*
                - The step guide field will be shared as an ordered list where each item represents a step in the
                    execution process. Each item means to describe a step within the script for you to better
                    understand what is the purpose of the script. Here is an example:
                    '''
                    [
                        "Moves to the Desktop folder.",
                        "Creates a folder named 'Outdated' in Desktop.",
                        "Checks which files are older than 30 days.",
                        "Moves the outdated files to 'Outdated' folder.",
                        "Deletes the empty folders in Desktop."
                    ]
                    '''

            -------

            #### **NOTE**: You might need to choose a Script you would like to use depending on the use case. You can
            then receive the contents of the script to be able to operate on it and help the user. For example, the
            user can ask you to put the script on a SSH File System, and then run it, and you can choose a relevant
            script from your available Scripts, take the content, and create a file within the SSH file system, then
            run it. This will be a process handled by YOU, so you need to pick a script ID from the available Scripts
            and then use the tool to retrieve the contents of it. Then you should understand this content, and put it
            yourself in a file on the SSH file system by using relevant tool(s).

            -------
            """

    return response_prompt


def build_lean_scripts_multi_modality_prompt():
    response_prompt = """
            ### **CUSTOM SCRIPTS:**

            '''
            <This information is redacted as you won't need it to serve your goal.>
            '''

            #### **THE NOTE ABOUT THE FORMAT OF THE AVAILABLE SOURCES:**
            - This information is shared with you for you to have a more clear understanding about the custom scripts
            given in the system. You can use this information to execute the custom scripts properly by providing the
            necessary input data and the script ID more easily.

            - *Script Name:*
                - The script name field will be shared as a string that represents the name of the script.

            - *Script Description:*
                - The script description will be shared as a string that represents the description of the script.

            - *Script Step Guide:*
                 - The script step guide will be shared as an ordered list where each item represents a step in the
                    execution process. Each item means to describe a step of the script for you to understand
                    what is the purpose of the script. Here is an example:
                    '''
                    [
                        "Moves to the Desktop.",
                        "Creates a folder named 'Outdated' in Desktop.",
                        "Checks which files are older than 30 days in Desktop.",
                        "Moves the outdated files to 'Outdated' folder.",
                        "Deletes the empty folders in Desktop."
                    ]
                    '''

            -------

            #### **NOTE**: You might need to choose a Script you would like to use depending on the use case. You can
            then receive the contents of the script to be able to operate on it and help the user. For example, the
            user can ask you to put the script on a SSH File System, and then run it, and you can choose a relevant
            script from your available Scripts, take the content, and create a file within the SSH file system, then
            run it. This will be a process handled by YOU, so you need to pick a script ID from the available Scripts
            and then use the tool to retrieve the contents of it. Then you should understand this content, and put it
            yourself in a file on the SSH file system by using relevant tool(s).

            -------
            """

    return response_prompt
