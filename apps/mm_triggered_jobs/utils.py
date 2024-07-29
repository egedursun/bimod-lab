from uuid import uuid4

from slugify import slugify


def generate_triggered_job_chat_name(triggered_job_name):
    uuid_1 = str(uuid4())
    uuid_2 = str(uuid4())
    return f"{slugify(triggered_job_name)} - {uuid_1} - {uuid_2}"
