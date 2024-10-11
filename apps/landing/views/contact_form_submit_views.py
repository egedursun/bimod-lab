#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: contact_form_submit_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail

from config import settings
from web_project import TemplateLayout, TemplateHelper


class LandingView_ContactFormSubmit(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "blank", "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            "display_customizer": False,})
        TemplateHelper.map_context(context)
        return context

    def post(self, request, *args, **kwargs):
        full_name = request.POST['fullname']
        email = request.POST['email']
        msg = request.POST['message']
        username = request.POST['username']
        usernames = User.objects.values_list('username', flat=True)
        email_msg = f"""
        Full Name: {full_name}
        Email: {email}

        Message:

        ```
        {msg}
        ```
        """

        if username and username in usernames:
            client = User.objects.get(username=username)
            if client.email == email:
                subject = f"[IMPORTANT] VERIFIED CLIENT QUERY: Message from {username} ({full_name})"
            else:
                subject = f"[IMPORTANT] UNVERIFIED CLIENT QUERY: Message from {username} ({full_name}) - Email Mismatch"
                email_msg += f"""
                [WARNING:] The email address provided does not match the email address in the database.
                Database Email: {client.email}
                Provided Email: {email}
                ------------------
                """

            email_msg += f"""

                CLIENT SIGNATURE:
                -----------------
                User: {client.username}
                First Name: {client.profile.first_name}
                Last Name: {client.profile.last_name}
                Email: {client.email}
                Phone: {client.profile.phone_number}
                Address: {client.profile.address}
                City: {client.profile.city}
                Country: {client.profile.country}
                Postal Code: {client.profile.postal_code}
                ------------------
                """
        else:
            subject = f"VISITOR QUERY: Message from {full_name}"
        send_mail(
            subject, email_msg, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL, email],
            fail_silently=False,
        )
        return redirect("landing:contact_form_submit", )
