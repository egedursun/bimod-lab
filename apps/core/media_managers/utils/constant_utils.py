#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#

FILE_EXTENSION_BIN = ".bin"

GENERATED_FILES_ROOT_MEDIA_PATH = "generated/files/"
GENERATED_IMAGES_ROOT_MEDIA_PATH = "generated/images/"
GENERATED_VIDEOS_ROOT_MEDIA_PATH = "generated/videos/"

MEDIA_PATH_FREEFORM_SKETCH = "free_form__user_sketch__"
MEDIA_PATH_EDIT_IMAGE_BASE = "edit_image__original_version__"
MEDIA_PATH_EDIT_IMAGE_MASK = "edit_image__masked_version__"


class ImageModes:
    RGBA = 'RGBA'
    RGB = 'RGB'
    JPG = "JPG"
    JPEG = "JPEG"


DEFAULT_IMAGE_COMPRESSION_JPEG = 80
