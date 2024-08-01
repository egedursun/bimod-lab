from apps._services.multimodality.mm_scripts_content_retriever import CustomScriptsContentRetriever
from apps.mm_scripts.models import CustomScriptReference


def retrieve_script_content(custom_script_reference_id):
    script_reference = CustomScriptReference.objects.filter(id=custom_script_reference_id).first()

    try:
        executor = CustomScriptsContentRetriever(script=script_reference.custom_script,
                                                 context_organization=script_reference.assistant.organization,
                                                 context_assistant=script_reference.assistant)
        response = executor.retrieve_custom_script_content()
    except Exception as e:
        error = f"[custom_script_content_retrieval_handler.retrieve_script_content] Error occurred while retrieving the script content: {str(e)}"
        return error
    return response
