
def get_structured_tone_prompt(tone: str):
    return f"""
        **YOUR TONE:**

        '''
        {tone}
        '''

        **NOTE**: This is the tone that you will be using while responding to the user's messages. Your use
        of language, the way you respond, and the way you interact with the user will be based on this tone.
        Make sure to keep this in mind while responding to the user's messages. If this part is EMPTY, you can
        use a standard tone, without any specific considerations.
    """
