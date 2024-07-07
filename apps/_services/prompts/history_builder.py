from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


class HistoryBuilder:

    class ChatRoles:
        SYSTEM = "SYSTEM"
        USER = "USER"
        ASSISTANT = "ASSISTANT"

    @staticmethod
    def build(chat: MultimodalChat):
        chat_messages = chat.chat_messages.all().order_by("sent_at")
        context_history = []
        for chat_message in chat_messages:
            sender_type = chat_message.sender_type
            message_text_content = chat_message.message_text_content
            if sender_type != HistoryBuilder.ChatRoles.SYSTEM:
                context_history.append({
                    "role": sender_type.lower(),
                    "content": message_text_content
                })
        return context_history
