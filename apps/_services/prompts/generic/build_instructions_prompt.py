

def get_structured_instructions_prompt(instructions: str):
    return f"""
        **YOUR INSTRUCTIONS:**

        '''
        {instructions}
        '''

        **NOTE**: Please make sure to follow these instructions VERY carefully, and never neglect them
        under any circumstances. This is very important to provide a good user experience and you are
        responsible for providing the best user experience. If this part is empty, your instructions are
        simply "You are a helpful assistant."
    """
