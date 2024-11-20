#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_029_invite_users_create.py
#  Last Modified: 2024-11-18 22:28:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:28:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging
import uuid

from django.contrib.auth.models import User, Group

from apps.organization.models import Organization
from apps.quick_setup_helper.utils import extract_username_from_email, create_temporary_password
from auth.models import Profile
from auth.utils import send_invitation_email, send_verification_email
from config import settings

logger = logging.getLogger(__name__)


def action__029_invite_users_create(
    metadata__user,
    metadata__organization,
    response__invite_users_email_addresses
):

    invited_new_users = []
    try:
        for user_email in response__invite_users_email_addresses:

            try:
                invited_new_user = invite_user_naked(
                    user=metadata__user,
                    organization=metadata__organization,
                    username=extract_username_from_email(email=user_email),
                    email=user_email,
                    pw=create_temporary_password()
                )

                if invited_new_user:
                    invited_new_users.append(invited_new_user)

            except Exception as e:
                logger.error(f"Failed to invite user with email address {user_email}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__029_invite_users_create: {str(e)}")
        return False, []

    logger.info("action__029_invite_users_create completed successfully.")
    return True, invited_new_users


def invite_user_naked(organization: Organization, user: User, username: str, email: str, pw: str):
    try:
        created_user = User.objects.create_user(username=username, email=email, password=pw)
        created_user.set_password(pw)
        created_user.save()
        user_group, created = Group.objects.get_or_create(name="user")
        created_user.groups.add(user_group)
        token = str(uuid.uuid4())
        user_profile, created = Profile.objects.get_or_create(user=created_user)
        user_profile.email_token = token
        user_profile.email = email
        user_profile.username = username
        user_profile.first_name = ""
        user_profile.last_name = ""
        user_profile.phone_number = ""
        user_profile.address = ""
        user_profile.city = ""
        user_profile.country = ""
        user_profile.postal_code = ""
        user_profile.is_active = True
        user_profile.created_by_user = user
        user_profile.save()

        organization.users.add(created_user)
        organization.save()
        user.profile.sub_users.add(created_user)
        user.profile.save()

        send_verification_email(email, token)

        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            logger.info(f"Verification email sent to {email}")
        else:
            logger.error("Email settings are not configured. Unable to send verification email.")

        logger.info(f"User: {created_user.id} was created by User: {user.id}.")
        try:
            email = created_user.email
            send_invitation_email(email, token)

            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                logger.info(f"Invitation email sent to {email}")
            else:
                logger.error('Email settings are not configured. Unable to send invitation email.')

            logger.info(f"User: {created_user.id} was created by User: {user.id}.")

        except Exception as e:
            logger.error(f'Error sending invitation email to user: {str(e)}')

    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        return None

    logger.info("invite_user_naked completed user invitation process successfully.")
    return created_user
