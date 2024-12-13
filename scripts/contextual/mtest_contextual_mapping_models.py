import os


def process_directory(
    directory,
    output_dir
):
    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_file_path = os.path.join(
        output_dir,
        "data_models.txt"
    )

    with open(
        output_file_path,
        'w',
        encoding='utf-8'
    ) as output_file:

        for root, dirs, files in os.walk(directory):

            if os.path.basename(root) == "models":

                for file in files:

                    if (
                        file.endswith('.py') or
                        file.endswith('_models.py')
                    ):
                        file_path = os.path.join(
                            root,
                            file
                        )

                        read_and_write_file(
                            file_path,
                            output_file
                        )

    print(f"All data written to: {output_file_path}")


def read_and_write_file(
    file_path,
    output_file
):
    with open(
        file_path,
        'r',
        encoding='utf-8'
    ) as file:
        contents = file.read()

    output_file.write(
        f"Contents of {file_path}:\n{contents}\n\n"
    )


# Replace '../../apps' with the actual path to your apps directory if it differs

process_directory(
    '../../apps',
    'output'
)
