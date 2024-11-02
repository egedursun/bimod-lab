#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:14:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

FORMICA_TOOL_CALL_MAXIMUM_ATTEMPTS = 3

FORMICA_GOOGLE_FORMS_QUESTION_TYPES = [
    "short_open_ended",
    "long_open_ended",
    "multiple_choice",
    "checkboxes",
    "dropdown_choices",
    "linear_scale",
    "rating_stars",
    "date",
    "time"
]


class FormicaGoogleFormsQuestionTypesNames:
    SHORT_OPEN_ENDED = "short_open_ended"
    LONG_OPEN_ENDED = "long_open_ended"
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOXES = "checkboxes"
    DROPDOWN_CHOICES = "dropdown_choices"
    LINEAR_SCALE = "linear_scale"
    RATING_STARS = "rating_stars"
    DATE = "date"
    TIME = "time"

    @staticmethod
    def as_list():
        return [
            FormicaGoogleFormsQuestionTypesNames.SHORT_OPEN_ENDED,
            FormicaGoogleFormsQuestionTypesNames.LONG_OPEN_ENDED,
            FormicaGoogleFormsQuestionTypesNames.MULTIPLE_CHOICE,
            FormicaGoogleFormsQuestionTypesNames.CHECKBOXES,
            FormicaGoogleFormsQuestionTypesNames.DROPDOWN_CHOICES,
            FormicaGoogleFormsQuestionTypesNames.LINEAR_SCALE,
            FormicaGoogleFormsQuestionTypesNames.RATING_STARS,
            FormicaGoogleFormsQuestionTypesNames.DATE,
            FormicaGoogleFormsQuestionTypesNames.TIME
        ]

    class ShortOpenEnded:
        PARAMETERS = {}

    class LongOpenEnded:
        PARAMETERS = {}

    class MultipleChoice:
        CHOICES = "choices <list of strings including the choices themselves>"

    class Checkboxes:
        CHOICES = "choices <list of strings including the choices themselves>"

    class DropdownChoices:
        CHOICES = "choices <list of strings including the choices themselves>"

    class LinearScale:
        INTERVAL_START = "interval_start <integer either 0 or 1>"
        INTERVAL_END = "interval_end <integer from 2 to 10>"

    class RatingStars:
        INTERVAL_SIZE = "interval_size <integer from 3 to 10>"

    #####

    class Config_OutputFinalResponseSpecifiers:
        QUESTION_TYPE = "question_type"
        PARAMETERS = "parameters"

        @staticmethod
        def as_list():
            return [
                FormicaGoogleFormsQuestionTypesNames.Config_OutputFinalResponseSpecifiers.QUESTION_TYPE,
                FormicaGoogleFormsQuestionTypesNames.Config_OutputFinalResponseSpecifiers.PARAMETERS
            ]
