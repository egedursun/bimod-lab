from uuid import uuid4

from slugify import slugify


def generate_scheduled_job_chat_name(scheduled_job_name):
    uuid_1 = str(uuid4())
    uuid_2 = str(uuid4())
    return f"{slugify(scheduled_job_name)} - {uuid_1} - {uuid_2}"
