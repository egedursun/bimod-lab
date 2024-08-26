from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.multimodal_chat.utils import BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, BIMOD_NO_TAG_PLACEHOLDER
from apps.orchestrations.models import OrchestrationQuery


def send_orchestration_message(log_message, query_id, stop_tag=BIMOD_STREAMING_END_TAG):
    channel_layer = get_channel_layer()
    group_name = f'orchestration_logs_{query_id}'
    query_object = OrchestrationQuery.objects.get(id=query_id)
    maestro_id = query_object.maestro.id
    generic_group_name = f'orchestration_generic_logs_{maestro_id}'

    async_to_sync(channel_layer.group_send)(group_name, {'type': 'send_log', 'message': log_message})
    # send to generic channel
    async_to_sync(channel_layer.group_send)(generic_group_name, {'type': 'send_log', 'message': log_message})
    if stop_tag == BIMOD_STREAMING_END_TAG:
        async_to_sync(channel_layer.group_send)(group_name, {'type': 'send_log', 'message': BIMOD_STREAMING_END_TAG})
        # send to generic channel
        async_to_sync(channel_layer.group_send)(generic_group_name,
                                                {'type': 'send_log', 'message': BIMOD_STREAMING_END_TAG})
    elif stop_tag == BIMOD_PROCESS_END:
        async_to_sync(channel_layer.group_send)(group_name, {'type': 'send_log', 'message': BIMOD_PROCESS_END})
        # send to generic channel
        async_to_sync(channel_layer.group_send)(generic_group_name, {'type': 'send_log', 'message': BIMOD_PROCESS_END})
    else:
        if stop_tag is None or stop_tag == "" or stop_tag == BIMOD_NO_TAG_PLACEHOLDER:
            pass
        else:
            async_to_sync(channel_layer.group_send)(group_name, {'type': 'send_log', 'message': stop_tag})
            # send to generic channel
            async_to_sync(channel_layer.group_send)(generic_group_name, {'type': 'send_log', 'message': stop_tag})


def embed_orchestration_tool_call_in_prompt(json_part):
    return f"""
        *Worker Tool Call:*

        ```
        {json_part}
        ```

    """
