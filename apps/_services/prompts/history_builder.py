from apps._services.chat_context.chat_context_manager import ChatContextManager
from apps.assistants.models import Assistant
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat


class HistoryBuilder:

    class ChatRoles:
        SYSTEM = "SYSTEM"
        USER = "USER"
        ASSISTANT = "ASSISTANT"
        TOOL = "TOOL"

    @staticmethod
    def build(chat: MultimodalChat):
        chat_messages = chat.chat_messages.all().order_by("sent_at")
        context_history = []
        for chat_message in chat_messages:
            sender_type = chat_message.sender_type
            if sender_type == HistoryBuilder.ChatRoles.TOOL:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT
            message_text_content = chat_message.message_text_content

            if sender_type != HistoryBuilder.ChatRoles.SYSTEM:
                context_history.append({
                    "role": sender_type.lower(),
                    "content": message_text_content
                })

            # Create the transactions and add them to the chat
            transaction = LLMTransaction.objects.create(
                organization=chat.organization,
                model=chat.assistant.llm_model,
                responsible_user=chat.user,
                responsible_assistant=chat.assistant,
                encoding_engine="cl100k_base",
                transaction_context_content=message_text_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=sender_type.lower(),
                transaction_source=chat.chat_source
            )
            chat.transactions.add(transaction)
            chat.save()
            chat_message.save()

        # use the context manager to handle overflows
        context_history = ChatContextManager.handle_context(
            chat_history=context_history,
            assistant=chat.assistant,
            chat_object=chat
        )

        return context_history
