#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: media_migration.py
#  Last Modified: 2024-12-17 04:58:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-17 04:58:33
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
from PIL import Image


def resize_images_in_directory(directory, max_resolution):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    print(f"Processing files in: {directory}")

    for filename in os.listdir(directory):
        filepath = os.path.join(
            directory,
            filename
        )

        if (
            os.path.isfile(filepath) and
            filename.lower().endswith(".png")
        ):
            try:
                with Image.open(filepath) as img:
                    img.thumbnail(
                        max_resolution,
                        Image.Resampling.LANCZOS
                    )

                    img.save(filepath, "PNG")

                    print(f"Resized and saved: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    target_directory = "../src/assets/img/aws_s3_config/course_thumbnail_images"
    width = 500
    height = 500

    resize_images_in_directory(
        target_directory,
        (
            width,
            height
        )
    )
