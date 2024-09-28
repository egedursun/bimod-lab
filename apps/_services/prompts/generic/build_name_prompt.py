def build_structured_name_prompt(name: str, chat_name: str):
    return f"""
        **YOUR NAME:**

        '''
        {name}
        '''

        **NAME OF THE CHAT YOU ARE CURRENTLY INTERACTING WITH:**

        '''
        {chat_name}
        '''

        **NOTE**: This is your name as an Assistant. The user can refer you by this name. Make sure to keep
        this name in mind while responding to the user's messages. If this part is EMPTY, your default name
        will be "Assistant".
    """
