#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.

from uuid import uuid4

from slugify import slugify


def generate_triggered_job_chat_name(triggered_job_name):
    uuid_1 = str(uuid4())
    uuid_2 = str(uuid4())
    return f"{slugify(triggered_job_name)} - {uuid_1} - {uuid_2}"
