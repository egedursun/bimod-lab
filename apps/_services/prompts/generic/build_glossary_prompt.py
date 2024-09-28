def build_structured_glossary_prompt(glossary: str):
    return f"""
        **YOUR GLOSSARY AND TERMINOLOGY:**

        '''
        {glossary}
        '''

        **NOTE**: This is the glossary and terminology that you will be aware of to understand the internal
        language and jargon of the organizations and domains. Make sure to keep this in mind while preparing
        the responses for the user's messages. If this part is EMPTY, you can use the general terminology that
        you are aware of.
    """
