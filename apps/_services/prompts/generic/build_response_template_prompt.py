

def build_structured_response_template_prompt(response_template: str):
    return f"""
        **YOUR RESPONSE TEMPLATE:**

        '''
        {response_template}
        '''

        **NOTE**: This is the template that you will use to respond to the user's messages. Make sure to
        follow this template under any circumstances and do not deviate from it. If this part is EMPTY,
        you can respond to the user's messages in any way you would like.
    """
