#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-20 14:05:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:05:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


NOTIFICATION_FA_ICON_CHOICES = [
    ('fa fa-bell', 'fa fa-bell'),
    ('fa fa-bullseye', 'fa fa-bullseye'),
    ('fa fa-comment', 'fa fa-comment'),
    ('fa fa-envelope', 'fa fa-envelope'),
    ('fa fa-exclamation-triangle', 'fa fa-exclamation-triangle'),
    ('fa fa-info-circle', 'fa fa-info-circle'),
    ('fa fa-list', 'fa fa-list'),
    ('fa fa-paper-plane', 'fa fa-paper-plane'),
    ('fa fa-question-circle', 'fa fa-question-circle'),
    ('fa fa-building', 'fa fa-building'),
]


class NotificationFAIconChoicesNames:
    BELL = 'fa fa-bell'
    BULLSEYE = 'fa fa-bullseye'
    COMMENT = 'fa fa-comment'
    ENVELOPE = 'fa fa-envelope'
    EXCLAMATION_TRIANGLE = 'fa fa-exclamation-triangle'
    INFO_CIRCLE = 'fa fa-info-circle'
    LIST = 'fa fa-list'
    PAPER_PLANE = 'fa fa-paper-plane'
    QUESTION_CIRCLE = 'fa fa-question-circle'
    BUILDING = 'fa fa-building'

    @staticmethod
    def as_list():
        return [
            NotificationFAIconChoicesNames.BELL,
            NotificationFAIconChoicesNames.BULLSEYE,
            NotificationFAIconChoicesNames.COMMENT,
            NotificationFAIconChoicesNames.ENVELOPE,
            NotificationFAIconChoicesNames.EXCLAMATION_TRIANGLE,
            NotificationFAIconChoicesNames.INFO_CIRCLE,
            NotificationFAIconChoicesNames.LIST,
            NotificationFAIconChoicesNames.PAPER_PLANE,
            NotificationFAIconChoicesNames.QUESTION_CIRCLE,
            NotificationFAIconChoicesNames.BUILDING,
        ]


NOTIFICATION_SENDER_TYPES = [
    ('bimod-team', 'Bimod Team'),
    ('welcome', 'Welcome'),
    ('system', 'System'),
]


class NotificationSenderTypeNames:
    BIMOD_TEAM = 'bimod-team'
    WELCOME = 'welcome'
    SYSTEM = 'system'

    @staticmethod
    def as_list():
        return [
            NotificationSenderTypeNames.BIMOD_TEAM,
            NotificationSenderTypeNames.WELCOME,
            NotificationSenderTypeNames.SYSTEM,
        ]


NOTIFICATION_TITLE_CATEGORY_CHOICES = [
    ('announcement', 'Announcement'),
    ('info', 'Information'),
    ('warning', 'Warning'),
    ('error', 'System Error'),
    ('alert', 'Alert'),
]


class NotificationTitleCategoryChoicesNames:
    ANNOUNCEMENT = 'announcement'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    ALERT = 'alert'

    @staticmethod
    def as_list():
        return [
            NotificationTitleCategoryChoicesNames.ANNOUNCEMENT,
            NotificationTitleCategoryChoicesNames.INFO,
            NotificationTitleCategoryChoicesNames.WARNING,
            NotificationTitleCategoryChoicesNames.ERROR,
            NotificationTitleCategoryChoicesNames.ALERT,
        ]

    class HumanReadable:
        ANNOUNCEMENT = 'Announcement'
        INFO = 'Information'
        WARNING = 'Warning'
        ERROR = 'System Error'
        ALERT = 'Alert'

        @staticmethod
        def as_list():
            return [
                NotificationTitleCategoryChoicesNames.HumanReadable.ANNOUNCEMENT,
                NotificationTitleCategoryChoicesNames.HumanReadable.INFO,
                NotificationTitleCategoryChoicesNames.HumanReadable.WARNING,
                NotificationTitleCategoryChoicesNames.HumanReadable.ERROR,
                NotificationTitleCategoryChoicesNames.HumanReadable.ALERT,
            ]


NOTIFICATION_ITEM_ADMIN_LIST = ('notification_sender_type', 'notification_title_category', 'created_at')
NOTIFICATION_ITEM_ADMIN_FILTER = ('notification_sender_type', 'notification_title_category')
NOTIFICATION_ITEM_ADMIN_SEARCH = ('notification_message', 'created_at')
