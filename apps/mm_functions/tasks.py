import json
import os
import shutil
import subprocess
import uuid
from random import shuffle

from celery import shared_task

from apps.mm_functions.models import CustomFunction


NUMBER_OF_RANDOM_FEATURED_FUNCTIONS = 5


def generate_venv_uuid_string():
    return str(uuid.uuid4())


@shared_task
def mm_function_execution_task(custom_function_id, input_values: dict):
    # Retrieve custom function
    custom_function = CustomFunction.objects.get(id=custom_function_id)
    packages = custom_function.packages
    input_fields = custom_function.input_fields
    output_fields = custom_function.output_fields

    package_imports = "\n".join([f"import {package['name']}" for package in packages])

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

    # Gather output names
    output_names = []
    for field in output_fields:
        name = field["name"]
        output_names.append(name)

    output_printer_string = "\n".join([f"print('{name}:', {name})" for name in output_names])

    # Define paths
    venv_path = f"sandbox/venv_{generate_venv_uuid_string()}"
    code_to_execute = custom_function.code_text

    stdout, stderr = None, None
    try:
        # Step 1: Create a virtual environment
        subprocess.run(["python3", "-m", "venv", venv_path], check=True)

        # Step 2: Install required packages (modify the list of packages as needed)
        for package in packages:
            package_name = package["name"]
            package_version = package["version"]
            subprocess.run([os.path.join(venv_path, "bin", "pip3"), "install --retries 1", f"{package_name}~={package_version}"
            if (package_version is not None and package_version != "") else package_name],
                           check=False)

        # Step 3: Write the code to a temporary script file

        script_path = os.path.join(venv_path, "script.py")
        with open(script_path, "w") as script_file:
            script_file.write(f"""
######################################
# Import the Packages
######################################
{package_imports}
print("[INFO] Loaded the Packages:", {packages})
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

        # Step 4: Execute the code within the virtual environment and capture outputs
        result = subprocess.run(
            [os.path.join(venv_path, "bin", "python"), script_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Step 5: Process the outputs
        stdout = result.stdout
        stderr = result.stderr

    except subprocess.CalledProcessError as e:
        # Handle errors (logging, notification, etc.)
        print(f"An error occurred: {e}")

    finally:
        # Step 6: Clean up the virtual environment
        shutil.rmtree(venv_path)

    # Handle outputs as needed (e.g., save to database, logging, etc.)
    response = {"stdout": stdout, "stderr": stderr}
    return response


@shared_task
def randomize_featured_functions():
    # first switch all function's is_featured field to false
    all_functions = CustomFunction.objects.all()
    for function in all_functions:
        function.is_featured = False
        function.save()

    # then select 5 random functions and set the is_featured field to true
    featured_functions = CustomFunction.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_FUNCTIONS]
    for function in featured_functions:
        function.is_featured = True
        function.save()
