#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: function_execution_task_tasks.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import json
import os
import shutil
import subprocess

from celery import shared_task

from apps.mm_functions.models import CustomFunction


@shared_task
def mm_function_execution_task(custom_function_id, input_values: dict):
    from apps.mm_functions.tasks import generate_venv_uuid_string

    # Retrieve custom function
    custom_function = CustomFunction.objects.get(id=custom_function_id)
    packages = custom_function.packages
    input_fields = custom_function.input_fields
    output_fields = custom_function.output_fields
    print(f"[tasks.mm_function_execution_task] custom_function: {custom_function}")
    print(f"[tasks.mm_function_execution_task] packages: {packages}")
    print(f"[tasks.mm_function_execution_task] input_fields: {input_fields}")
    print(f"[tasks.mm_function_execution_task] output_fields: {output_fields}")

    package_imports = "\n".join([f"import {package['name']}" for package in packages])
    print(f"[tasks.mm_function_execution_task] package_imports: {package_imports}")

    # Secrets
    secrets = ""
    for secret_item in custom_function.secrets:
        name = secret_item["name"]
        key = secret_item["key"]
        secrets += f"{name} = '{key}'\n"
    print(f"[tasks.mm_function_execution_task] Loaded the Secrets: ********")

    # Convert inputs dictionary to variable declarations
    variables = ""
    for field in input_fields:
        name = field["name"]
        if name not in input_values:
            if field["required"] is True:
                return {"stout": None, "stderr": f"Input field '{name}' is missing."}
            value = None
        else:
            value = input_values[name]
        variables += f"{name} = {json.dumps(value) if value is not None else 'None'}\n"
    print(f"[tasks.mm_function_execution_task] Loaded the Inputs: {input_values}")

    # Gather output names
    output_names = []
    for field in output_fields:
        name = field["name"]
        output_names.append(name)
    print(f"[tasks.mm_function_execution_task] Loaded the Output Names: {output_names}")
    output_printer_string = "\n".join([f"print('{name}:', {name})" for name in output_names])
    print(f"[tasks.mm_function_execution_task] Output Printer String: {output_printer_string}")

    # Define paths
    venv_path = f"sandbox/venv_{generate_venv_uuid_string()}"
    print(f"[tasks.mm_function_execution_task] Virtual Environment Path: {venv_path}")
    code_to_execute = custom_function.code_text
    print(f"[tasks.mm_function_execution_task] Custom Function Code: {code_to_execute}")

    stdout, stderr = None, None
    try:
        # Step 1: Create a virtual environment
        subprocess.run(["python3", "-m", "venv", venv_path], check=True)
        print(f"[tasks.mm_function_execution_task] Created the Virtual Environment: {venv_path}")

        # Step 2: Install required packages (modify the list of packages as needed)
        for package in packages:
            package_name = package["name"]
            package_version = package["version"]
            subprocess.run(
                [os.path.join(venv_path, "bin", "pip3"), "install --retries 1", f"{package_name}~={package_version}"
                if (package_version is not None and package_version != "") else package_name],
                check=False)
        print(f"[tasks.mm_function_execution_task] Installed the Packages: {packages}")

        # Step 3: Write the code to a temporary script file
        script_path = os.path.join(venv_path, "script.py")
        print(f"[tasks.mm_function_execution_task] Script Path: {script_path}")
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
        print(f"[tasks.mm_function_execution_task] Wrote the Custom Function Code to the Script File: {script_path}")
        # Step 4: Execute the code within the virtual environment and capture outputs
        result = subprocess.run(
            [os.path.join(venv_path, "bin", "python"), script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[tasks.mm_function_execution_task] Executed the Custom Function Code: {result}")

        # Step 5: Process the outputs
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.CalledProcessError as e:
        # Handle errors (logging, notification, etc.)
        print(f"An error occurred: {e}")
    finally:
        # Step 6: Clean up the virtual environment
        shutil.rmtree(venv_path)
        print(f"[tasks.mm_function_execution_task] Cleaned up the Virtual Environment: {venv_path}")

    # Handle outputs as needed (e.g., save to database, logging, etc.)
    response = {"stdout": stdout, "stderr": stderr}
    print(f"[tasks.mm_function_execution_task] Response: {response}")
    return response
