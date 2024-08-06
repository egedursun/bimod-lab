from apps._services.multimodality.mm_functions_executor import CustomFunctionExecutor
from apps.mm_functions.models import CustomFunctionReference


def execute_custom_code_executor(custom_function_reference_id, input_values: dict):
    function_reference = CustomFunctionReference.objects.filter(id=custom_function_reference_id).first()
    print(f"[custom_function_execution_handler.execute_custom_code_executor] Executing the function: {function_reference.custom_function.name}.")
    try:
        executor = CustomFunctionExecutor(function=function_reference.custom_function,
                                          context_organization=function_reference.assistant.organization,
                                          context_assistant=function_reference.assistant)
        response = executor.execute_custom_function(input_data=input_values)
    except Exception as e:
        error = f"[custom_function_execution_handler.execute_custom_code_executor] Error occurred while executing the function: {str(e)}"
        return error
    print(f"[custom_function_execution_handler.execute_custom_code_executor] Function executed successfully.")
    return response
