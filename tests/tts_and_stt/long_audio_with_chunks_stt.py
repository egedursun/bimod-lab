#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: long_audio_with_chunks_stt.py
#  Last Modified: 2024-09-23 12:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

# NOTE: Implement this test
#   ========================
#   - Long audio files (more than 25MBs) are not supported to directly get transcribed, so they need to be split
#     into chunks
#   ========================

"""
    from pydub import AudioSegment

    song = AudioSegment.from_mp3("good_morning.mp3")

    # PyDub handles time in milliseconds
    ten_minutes = 10 * 60 * 1000

    first_10_minutes = song[:ten_minutes]

    first_10_minutes.export("good_morning_10.mp3", format="mp3")
"""
