import os


def process_directory(directory, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(output_dir, "data_models.txt")

    # Open the output file once and write contents of all files
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(directory):
            # Check if the current directory's base name is 'models'
            if os.path.basename(root) == "models":
                for file in files:
                    if file.endswith('.py') or file.endswith('_models.py'):
                        file_path = os.path.join(root, file)
                        read_and_write_file(file_path, output_file)
    print(f"All data written to: {output_file_path}")


def read_and_write_file(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    # Write the contents to the single output file
    output_file.write(f"Contents of {file_path}:\n{contents}\n\n")


# Replace '../../apps' with the actual path to your apps directory if it differs
process_directory('../../apps', 'output')
