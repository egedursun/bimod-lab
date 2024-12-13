#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-09 19:15:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:15:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


REFERRAL_DEFAULT_BONUS_PERCENTAGE = 50

USER_FORUM_ROLES = [
    ('bimod', 'Bimod'),
    ('client_admin', 'Client Admin'),
    ('client_user', 'Client User'),
]
USER_FORUM_RANKS = [
    ('unranked', 'Unranked'),
    ('wood', 'Wood'),
    ('iron', 'Iron'),
    ('bronze', 'Bronze'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
    ('platinum', 'Platinum'),
    ('diamond', 'Diamond'),
    ('master', 'Master'),
    ('grandmaster', 'Grandmaster'),
]
RANK_POINT_REQUIREMENTS = {
    'wood': 0,
    'iron': 50,
    'bronze': 100,
    'silver': 200,
    'gold': 500,
    'platinum': 1_000,
    'diamond': 2_000,
    'master': 5_000,
    'grandmaster': 10_000,
}
UNIT_REWARD_FOR_POINTS = {
    'wood': 0.030,
    'iron': 0.040,
    'bronze': 0.050,
    'silver': 0.060,
    'gold': 0.070,
    'platinum': 0.080,
    'diamond': 0.090,
    'master': 0.100,
    'grandmaster': 0.100,
}
POINT_REWARDS = {
    'ask_question': 1,
    'add_comment': 1,
    'get_like': 2,
    'get_merit': 5,
}


class ForumRewardActionsNames:
    ASK_QUESTION = 'ask_question'
    ADD_COMMENT = 'add_comment'
    GET_LIKE = 'get_like'
    GET_MERIT = 'get_merit'


MEMBER_ADMIN_LIST = (
    "user",
    "email",
    "is_verified",
    "is_accredited_by_staff",
    "created_at",
)

PROMO_CODE_ADMIN_LIST = (
    "user",
    "code",
    "bonus_percentage_referrer",
    "bonus_percentage_referee",
    "is_active",
    "current_referrals",
    "max_referral_limit",
    "datetime_limit",
    "created_at",
)

CREDIT_CARD_ADMIN_LIST = (
    "name_on_card",
    "card_number",
    "card_expiration_month",
    "card_expiration_year",
    "card_cvc",
    "created_at",
)

BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_LIST = [
    'email_subject_raw',
    'title_raw',
    'created_at'
]
BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_SEARCH = [
    'email_subject_raw',
    'title_raw',
    'body_raw'
]
BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_FILTER = [
    'created_at'
]
