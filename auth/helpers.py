import os

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.utils.html import strip_tags


def send_email(subject, email, html_content):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMultiAlternatives(subject, strip_tags(html_content), email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"[helpers.send_email] Failed to send email: {e}")


def get_absolute_url(path):
    return settings.BASE_URL + path


def render_html_template(file_path, context):
    with open(file_path, 'r') as file:
        html_content = file.read()
    for key, value in context.items():
        html_content = html_content.replace(f'<[[{key}]]>', value)
    return html_content


def send_verification_email(email, token):
    subject = "Bimod.io | Verify Email"
    verification_url = get_absolute_url(reverse('verify-email', kwargs={'token': token}))
    context = {'VERIFICATION_LINK': verification_url}
    file_path = os.path.join(os.path.dirname(__file__), 'helper_templates', 'verification_email_template.html')
    html_content = render_html_template(file_path, context)
    send_email(subject, email, html_content)


def send_password_reset_email(email, token):
    subject = "Bimod.io | Reset Password"
    reset_url = get_absolute_url(reverse('reset-password', kwargs={'token': token}))
    context = {'VERIFICATION_LINK': reset_url}
    file_path = os.path.join(os.path.dirname(__file__), 'helper_templates', 'reset_password_email_template.html')
    html_content = render_html_template(file_path, context)
    send_email(subject, email, html_content)
