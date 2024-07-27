from apps._services.multimodality.mm_scripts_content_retriever import CustomScriptsContentRetriever
from apps.mm_scripts.models import CustomScriptReference


def retrieve_script_content(custom_script_reference_id):
    script_reference = CustomScriptReference.objects.filter(id=custom_script_reference_id).first()
    executor = CustomScriptsContentRetriever(script=script_reference.custom_script,
                                             context_organization=script_reference.assistant.organization,
                                             context_assistant=script_reference.assistant)
    response = executor.retrieve_custom_script_content()
    return response
