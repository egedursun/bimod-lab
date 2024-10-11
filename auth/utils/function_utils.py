#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-09 19:15:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:15:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


import datetime
import os
import random
import string

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.html import strip_tags


def send_email(subject, email, html_content):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMultiAlternatives(subject, strip_tags(html_content), email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        pass


def get_absolute_url(path):
    return settings.BASE_URL + path


def render_html_template(file_path, context):
    with open(file_path, 'r') as file:
        html_content = file.read()
    for key, value in context.items():
        html_content = html_content.replace(f'<[[{key}]]>', value)
    return html_content


def send_verification_email(email, token):
    subject = "Br6.in | Verify Email"
    verification_url = get_absolute_url(reverse('verify-email', kwargs={'token': token}))
    context = {'VERIFICATION_LINK': verification_url}
    file_path = os.path.join(os.path.dirname(__file__), 'helper_templates', 'verification_email_template.html')
    html_content = render_html_template(file_path, context)
    send_email(subject, email, html_content)


def send_invitation_email(email, token):
    subject = "Br6.in | Invitation"
    set_password_url = get_absolute_url(reverse('reset-password', kwargs={'token': token}))
    context = {'VERIFICATION_LINK': set_password_url}
    file_path = os.path.join(os.path.dirname(__file__), 'helper_templates', 'invitation_email_template.html')
    html_content = render_html_template(file_path, context)
    send_email(subject, email, html_content)


def send_password_reset_email(email, token):
    subject = "Br6.in | Reset Password"
    reset_url = get_absolute_url(reverse('reset-password', kwargs={'token': token}))
    context = {'VERIFICATION_LINK': reset_url}
    file_path = os.path.join(os.path.dirname(__file__), 'helper_templates', 'reset_password_email_template.html')
    html_content = render_html_template(file_path, context)
    send_email(subject, email, html_content)


def generate_random_string(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_referral_code(length=16):
    alphas = string.ascii_uppercase  # 26
    numerics = string.digits  # 10
    year = datetime.datetime.now().year.__str__()
    month = datetime.datetime.now().month.__str__()
    day = datetime.datetime.now().day.__str__()
    generated_alpha = ''.join(random.choice(alphas) for _ in range(length // 2))
    generated_numeric = ''.join(random.choice(numerics) for _ in range(length // 2))
    generated_date = f"{year}-{month}{day}"
    return f"{generated_alpha[0:4]}-{generated_alpha[4:]}-{generated_numeric[0:4]}-{generated_numeric[4:]}-{generated_date}0"


def is_valid_password(password: str) -> (bool, str):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in string.punctuation for char in password):
        return False, "Password must contain at least one special character."
    return True, None
