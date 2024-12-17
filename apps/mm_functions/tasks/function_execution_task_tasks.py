#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_execution_task_tasks.py
#  Last Modified: 2024-10-05 01:39:48
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

import json
import logging
import os
import shutil
import subprocess

from celery import shared_task

from apps.mm_functions.models import (
    CustomFunction
)

logger = logging.getLogger(__name__)


@shared_task
def mm_function_execution_task(
    custom_function_id,
    input_values: dict
):
    from apps.mm_functions.tasks import (
        generate_venv_uuid_string
    )

    custom_function = CustomFunction.objects.get(
        id=custom_function_id
    )

    packages = custom_function.packages
    input_fields = custom_function.input_fields
    output_fields = custom_function.output_fields
    package_imports = "\n".join([f"import {package['name']}" for package in packages])

    secrets = ""

    for secret_item in custom_function.secrets:
        name = secret_item["name"]
        key = secret_item["key"]
        secrets += f"{name} = '{key}'\n"

    variables = ""

    for field in input_fields:
        name = field["name"]

        if name not in input_values:

            if field["required"] is True:
                logger.error(f"Input field '{name}' is missing.")

                return {
                    "stout": None,
                    "stderr": f"Input field '{name}' is missing."
                }

            value = None

        else:
            value = input_values[name]

        variables += f"{name} = {json.dumps(value) if value is not None else 'None'}\n"

    output_names = []

    for field in output_fields:
        name = field["name"]
        output_names.append(name)

    output_printer_string = "\n".join([f"print('{name}:', {name})" for name in output_names])

    venv_path = f"sandbox/venv_{generate_venv_uuid_string()}"

    code_to_execute = custom_function.code_text

    stdout, stderr = None, None
    try:
        subprocess.run(
            [
                "python3", "-m", "venv", venv_path
            ], check=True
        )

        for package in packages:
            package_name = package["name"]
            package_version = package["version"]

            subprocess.run(
                [
                    os.path.join(
                        venv_path,
                        "bin",
                        "pip3"
                    ),
                    (
                        "install --retries 1", f"{package_name}~={package_version}" if (
                            package_version is not None and package_version != ""
                        ) else package_name
                    )
                ],
                check=False
            )

        script_path = os.path.join(
            venv_path,
            "script.py"
        )

        with open(script_path, "w") as script_file:
            script_file.write(f"""
######################################
# Import the Packages
######################################
{package_imports}
print("[INFO] Loaded the Packages:", {packages})
######################################
# Assign the secrets
{secrets}
print("[INFO] Loaded the Secrets: ********")
######################################
# Auto-Generated Variables from Inputs
######################################
{variables}
print("[INFO] Loaded the Inputs:", {input_values})
######################################
# User's Custom Function Code Starts Here
######################################
{code_to_execute}
print("[INFO] Custom Function Code Executed Successfully.")
######################################
# Print the Outputs
######################################
print("[INFO] Outputs for the Custom Execution:")
{output_printer_string}
######################################
""")

        result = subprocess.run(
            [
                os.path.join(
                    venv_path,
                    "bin",
                    "python"
                ),
                script_path
            ],
            capture_output=True,
            text=True,
            check=True
        )

        stdout = result.stdout
        stderr = result.stderr

        logger.info(f"Custom Function executed successfully.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error while executing the custom function: {e}")
        pass

    finally:
        shutil.rmtree(venv_path)

    response = {
        "stdout": stdout,
        "stderr": stderr
    }

    return response
