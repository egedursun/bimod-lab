
from apps.orchestrations.models import OrchestrationQuery, Maestro


def run_worker_tool(maestro_id, query_id, worker_assistant_id, query_text, file_urls, image_urls):
    from apps._services.orchestration.orchestration_executor import OrchestrationExecutor, \
        DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

    maestro = Maestro.objects.get(id=maestro_id)
    query_chat = OrchestrationQuery.objects.get(id=query_id)

    try:
        executor = OrchestrationExecutor(
            maestro=maestro,
            query_chat=query_chat,
        )
    except Exception as e:
        print('[worker_tool_runner.run_worker_tool] An error occurred while creating the executor:', e)
        return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

    try:
        final_response = executor.ask_worker_assistant(
            assistant_id=worker_assistant_id,
            maestro_query=query_text,
            file_urls=file_urls,
            image_urls=image_urls,
        )
    except Exception as e:
        print('[worker_tool_runner.run_worker_tool] An error occurred while asking the worker assistant:', e)
        return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

    print('[worker_tool_runner.run_worker_tool] The final response is retrieved from the worker assistant.')
    print('[worker_tool_runner.run_worker_tool] The final response is:', final_response)
    return final_response

