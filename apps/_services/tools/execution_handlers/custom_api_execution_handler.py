from apps._services.multimodality.mm_api_executor import CustomAPIExecutor
from apps.mm_apis.models import CustomAPIReference


def execute_api_executor(custom_api_reference_id, endpoint_name: str, path_values=None, query_values=None, body_values=None):
    api_reference = CustomAPIReference.objects.filter(id=custom_api_reference_id).first()
    executor = CustomAPIExecutor(api=api_reference.custom_api, context_organization=api_reference.assistant.organization,
                                context_assistant=api_reference.assistant)
    response = executor.execute_custom_api(endpoint_name=endpoint_name,
                                           path_values=path_values,
                                           query_values=query_values,
                                           body_values=body_values)
    return response
