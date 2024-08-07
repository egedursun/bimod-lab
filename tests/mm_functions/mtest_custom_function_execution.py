import os
import subprocess
import shutil
import json


def mm_function_execution_task(custom_function_id, input_values: dict):
    # Retrieve custom function
    packages = [
        {"name": "numpy", "version": None},
        {"name": "pandas", "version": None},
    ]
    input_fields = [
        {"name": "x", "type": "float", "required": True},
        {"name": "y", "type": "float", "required": True},
        {"name": "z", "type": "float", "required": False},
    ]
    output_fields = [
        {"name": "calculation_result", "type": "float", "required": True},
    ]

    # Convert packages to import statements
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
    venv_path = f"venv_test_001"
    code_to_execute = """
calculation_result = x + y
"""

    stdout, stderr = None, None
    try:
        # Step 1: Create a virtual environment
        subprocess.run(["python3", "-m", "venv", venv_path], check=True)

        # Step 2: Install required packages (modify the list of packages as needed)
        for package in packages:
            package_name = package["name"]
            package_version = package["version"]
            subprocess.run([os.path.join(venv_path, "bin", "pip"), "install", f"{package_name}~={package_version}" if package_version else package_name],
                           check=True)

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
        pass

    # Handle outputs as needed (e.g., save to database, logging, etc.)
    response = {"stdout": stdout, "stderr": stderr}
    return response


# Test the function
input_values = {"x": 10, "y": 20}
response = mm_function_execution_task(1, input_values)
print(response)
