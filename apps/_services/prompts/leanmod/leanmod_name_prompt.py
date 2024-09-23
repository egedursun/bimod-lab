

def build_structured_name_prompt_leanmod(assistant_name, chat_name):
    return f"""
        *YOUR NAME*

        '''
        {assistant_name}
        '''

        *NAME OF THE ACTIVE CHAT*

        '''
        {chat_name}
        '''
    """
