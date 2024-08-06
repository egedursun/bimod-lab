import requests

from apps._services.chat_context.chat_context_manager import ChatContextManager
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat
import base64 as b64


class HistoryBuilder:

    class ChatRoles:
        SYSTEM = "SYSTEM"
        USER = "USER"
        ASSISTANT = "ASSISTANT"
        TOOL = "TOOL"

    @staticmethod
    def build(chat: MultimodalChat):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE
        chat_messages = chat.chat_messages.all().order_by("sent_at")
        context_history = []
        for chat_message in chat_messages:
            sender_type = chat_message.sender_type
            if sender_type == HistoryBuilder.ChatRoles.TOOL:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT
            message_text_content = chat_message.message_text_content
            message_image_urls = chat_message.message_image_contents
            message_file_urls = chat_message.message_file_contents

            message_object = {"role": sender_type.lower()}
            content_wrapper = [{"type": "text", "text": message_text_content}]
            if message_image_urls and sender_type == HistoryBuilder.ChatRoles.USER:
                for image_url in message_image_urls:
                    # get the object from local storage
                    full_uri = f"{image_url}"
                    try:
                        # download image from URL
                        response = requests.get(full_uri)
                        # read the file
                        image_bytes = response.content
                        image_b64 = b64.b64encode(image_bytes).decode("utf-8")
                    except Exception as e:
                        print(f"[HistoryBuilder.build] Error reading image file: {e}")
                        continue
                    image_content_wrapper = {"type": "image_url", "image_url": {"url": f"data:image/{image_url.split('.')[-1]};base64,{image_b64}"}}
                    image_uri_info_wrapper = {"type": "text", "text": f"Detected Image URLs: {image_url}"}
                    content_wrapper.append(image_content_wrapper)
                    content_wrapper.append(image_uri_info_wrapper)
            if message_file_urls and sender_type == HistoryBuilder.ChatRoles.USER:
                for file_url in message_file_urls:
                    # get the object from local storage
                    file_uri_info_wrapper = {"type": "text", "text": f"Detected File URLs: {file_url}"}
                    content_wrapper.append(file_uri_info_wrapper)

            message_object["content"] = content_wrapper

            if sender_type != HistoryBuilder.ChatRoles.SYSTEM:
                context_history.append(message_object)

            # Create the transactions and add them to the chat
            transaction = LLMTransaction.objects.create(
                organization=chat.organization,
                model=chat.assistant.llm_model,
                responsible_user=chat.user,
                responsible_assistant=chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
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
            print(f"[HistoryBuilder.build] Transaction has been saved.")

        # use the context manager to handle overflows
        context_history = ChatContextManager.handle_context(
            chat_history=context_history,
            assistant=chat.assistant,
            chat_object=chat
        )
        print(f"[HistoryBuilder.build] Context history has been built successfully.")
        return context_history
