#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mtest_contextual_mapping_html.py
#  Last Modified: 2024-11-17 00:13:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 00:13:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


import os


def process_html_files(
    directory,
    output_dir
):
    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_html_path = os.path.join(
        output_dir,
        "data_html.txt"
    )

    with open(
        output_html_path,
        'w',
        encoding='utf-8'
    ) as html_file:

        for root, dirs, files in os.walk(directory):

            for file in files:

                if file.endswith('.html'):
                    file_path = os.path.join(
                        root,
                        file
                    )

                    write_file_contents(
                        file_path,
                        html_file
                    )

    print(f"HTML data written to: {output_html_path}")


def write_file_contents(
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

apps_directory = '../../apps'
output_directory = 'output'

process_html_files(
    apps_directory,
    output_directory
)
