
def build_structured_audience_prompt(audience: str):
    return f"""
        **YOUR AUDIENCE:**

        '''
        {audience}
        '''

        **NOTE**: This is the audience that you will be targeting with your responses. Make sure to keep
        this in mind while preparing the responses for to the user's messages. If this part is EMPTY, you can
        target a general audience, without any specific target.
    """
