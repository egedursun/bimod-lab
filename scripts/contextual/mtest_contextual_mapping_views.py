#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mtest_contextual_mapping_views.py
#  Last Modified: 2024-11-17 00:08:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 00:08:45
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


def process_views(
    directory,
    output_dir
):
    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_views_path = os.path.join(
        output_dir,
        "data_views.txt"
    )

    with open(
        output_views_path,
        'w',
        encoding='utf-8'
    ) as views_file:

        for root, dirs, files in os.walk(
            directory
        ):

            if 'views' in root.split(os.sep):

                for file in files:

                    if file.endswith('.py'):
                        file_path = os.path.join(
                            root,
                            file
                        )

                        write_file_contents(
                            file_path,
                            views_file
                        )

    print(f"Views data written to: {output_views_path}")


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

process_views(
    apps_directory,
    output_directory
)
