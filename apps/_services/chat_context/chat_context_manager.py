

class ChatContextManager:

    # Create a summarizer prompt manager, we will pass these as a parameter to the chat system prompt

    def __init__(self):
        # needs a summarizer
        self.summarizer = None

    def forget_older_than_n_messages(self, chat_history, max_messages_to_keep):
        # If len(chat_history) > max_messages_to_keep
        # remove the overflow messages from the context
        # Agent forgets the older messages
        pass

    def summarize_older_than_n_messages(self, chat_history, max_messages_to_keep):
        """
            [1] **Using "forget", "summarize", or "vectorstore" will -> also be an assistant field ???
            [2] Let's assume the max_messages_to_keep is 25 (N) -> this will be an assistant field ???
            [3] We want to summarize by using every 5 messages. (X) -> this will be an assistant field ???

            1. when chat length surpasses 20 (N-X), we wait until there are 5 more messages.
            2. Then, we take the last 5 (X) messages, and summarize them.
            3. We save the summary in the DB, as a new data model.
            4. We remove the last 5 (X) messages from the chat history.
            5. Now, the chat again has 20 (N) messages.
            6. Now, we add the summaries to the system prompt as reminders to the agent.
            7. Now, we wait until the chat length surpasses 20 again. (N-5)
        """
        pass

    def store_older_than_n_messages_as_vector(self, chat_history, max_messages_to_keep):
        # If len(chat_history) > max_messages_to_keep
        # store the overflow messages as a vector, in a vector store.
        # Agent stores the older messages as a vector.
        # [1] every assistant has a vector store for this
        # [2] the messages will be chunked and saved into this knowledge base.
        # [3] the assistant will have a tool to retrieve his older messages from this knowledge base, whenever
        #      required, to help him in the conversation.
        pass
