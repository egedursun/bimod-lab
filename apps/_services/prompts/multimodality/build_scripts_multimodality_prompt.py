import json

from apps.assistants.models import Assistant
from apps.mm_scripts.models import CustomScriptReference


def build_scripts_multimodality_prompt(assistant: Assistant):
    response_prompt = ""

    # Retrieve the scripts of the assistant
    custom_script_references = CustomScriptReference.objects.filter(assistant=assistant)

    # Build the prompt
    response_prompt = """
            **CUSTOM SCRIPTS:**

            '''
            """

    for i, custom_script_reference in enumerate(custom_script_references):
        custom_script = custom_script_reference.custom_script
        response_prompt += f"""
                [Custom Script Reference ID: {custom_script_reference.id}]
                    Custom Script Name: {custom_script.name}
                    Custom Script Description: {custom_script.description}
                    Script Step Guide (What the script does step by step):
                    '''
                    {json.dumps(custom_script.script_step_guide, indent=4)}
                    '''
                """

    response_prompt += """
            -------

            '''

            **THE NOTE ABOUT THE FORMAT OF THE SCRIPT NAME, DESCRIPTION, AND STEP GUIDE ARE DELIVERED:**
            - This information is shared with you for you to have a more clear understanding about the custom scripts
            given in the system. You can use this information to execute the custom scripts properly by providing the
            necessary input data and the script ID more easily.

            *Script Name:*
            - The script name field will be shared as a string that represents the name of the custom script.

            *Script Description:*
            - The script description field will be shared as a string that represents the description of the custom script.

            *Script Step Guide:*
            - The script step guide field will be shared as an ordered list where each item represents a step in the
            script execution process. Each item means to describe a step within the script for you to better understand
            what exactly is the purpose of the script and what it does. Here is an example:
            '''
            [
                "Moves to the Desktop folder.",
                "Creates a folder named 'Outdated' in the Desktop folder.",
                "Checks which files are older than 30 days in the Desktop folder.",
                "Moves the outdated files to the 'Outdated' folder.",
                "Deletes the empty folders in the Desktop folder."
            ]
            '''

            -------

            **NOTE**: You need to primarily choose a Script you would like to use depending on the use case. You can
            then receive the contents for the script to be able to operate on it to provide help for the user. For
            example, the user can ask you to put this script on a File System, and then run it, and you can choose
            a relevant script from your Custom Scripts, take the contents of it, and create such a file within the
            file system, then run it. This will be a process handled by YOU, so you need to pick a script ID from the
            custom Scripts and then use the tool to retrieve the contents of the script. Then you should understand
            this content, and put it yourself in a file within the file system by using the relevant tool(s).

            -------
            """

    return response_prompt


def build_lean_scripts_multimodality_prompt():
    # Build the prompt
    response_prompt = """
            **CUSTOM SCRIPTS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **THE NOTE ABOUT THE FORMAT OF THE SCRIPT NAME, DESCRIPTION, AND STEP GUIDE ARE DELIVERED:**
            - This information is shared with you for you to have a more clear understanding about the custom scripts
            given in the system. You can use this information to execute the custom scripts properly by providing the
            necessary input data and the script ID more easily.

            *Script Name:*
            - The script name field will be shared as a string that represents the name of the custom script.

            *Script Description:*
            - The script description field will be shared as a string that represents the description of the custom script.

            *Script Step Guide:*
            - The script step guide field will be shared as an ordered list where each item represents a step in the
            script execution process. Each item means to describe a step within the script for you to better understand
            what exactly is the purpose of the script and what it does. Here is an example:
            '''
            [
                "Moves to the Desktop folder.",
                "Creates a folder named 'Outdated' in the Desktop folder.",
                "Checks which files are older than 30 days in the Desktop folder.",
                "Moves the outdated files to the 'Outdated' folder.",
                "Deletes the empty folders in the Desktop folder."
            ]
            '''

            -------

            **NOTE**: You need to primarily choose a Script you would like to use depending on the use case. You can
            then receive the contents for the script to be able to operate on it to provide help for the user. For
            example, the user can ask you to put this script on a File System, and then run it, and you can choose
            a relevant script from your Custom Scripts, take the contents of it, and create such a file within the
            file system, then run it. This will be a process handled by YOU, so you need to pick a script ID from the
            custom Scripts and then use the tool to retrieve the contents of the script. Then you should understand
            this content, and put it yourself in a file within the file system by using the relevant tool(s).

            -------
            """

    return response_prompt
