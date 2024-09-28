import hashlib
import random
import string

from apps.orchestrations.models import Maestro
from config import settings


def generate_orchestration_endpoint(assistant: Maestro):
    assistant_id = assistant.id
    organization_id = assistant.organization.id
    organization_name = assistant.organization.name
    assistant_name = assistant.name
    llm_model_name = assistant.llm_model.model_name
    creation_date = assistant.created_at
    creation_year = creation_date.year
    creation_month = creation_date.month
    creation_day = creation_date.day
    randomness_constraint = "".join([str(random.choice(string.digits)) for _ in range(16)])
    return (f"{organization_id}/{''.join(ch for ch in organization_name if ch.isalnum())}/"
            f"{assistant_id}/{''.join(ch for ch in assistant_name if ch.isalnum())}/"
            f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/{creation_year}/{creation_month}/{creation_day}"
            f"/{randomness_constraint}")


def generate_orchestration_custom_api_key(assistant: Maestro):
    assistant_id = assistant.id
    organization_id = assistant.organization.id
    organization_name = assistant.organization.name
    assistant_name = assistant.name
    instructions = assistant.instructions
    llm_model_name = assistant.llm_model.model_name
    llm_model_temperature = assistant.llm_model.temperature
    llm_model_max_tokens = assistant.llm_model.maximum_tokens
    llm_temperature = assistant.llm_model.temperature
    salt = settings.ENCRYPTION_SALT
    randomness_constraint = [random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                             for _ in range(64)]

    # merge the strings
    merged_string = (f"{assistant_id}{assistant_name}{instructions}{llm_model_name}"
                     f"{llm_model_temperature}{llm_model_max_tokens}{llm_temperature}{salt}{randomness_constraint}")
    # encrypt the merged string with SHA-256
    encrypted_string = ("Bearer bimod/" +
                        f"{str(organization_id)}/" +
                        f"{''.join(ch for ch in organization_name if ch.isalnum())}/" +
                        f"{str(assistant_id)}/" +
                        f"{''.join(ch for ch in assistant_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())
    return str(encrypted_string)
