import tiktoken

VALUE_PLACEHOLDER = "<value>"


GPT_DEFAULT_ENCODING_ENGINE = "cl100k_base"


def get_simplified_mongodb_schema(data):
    """Recursively traverses the document to build a simplified schema."""
    if isinstance(data, dict):
        return {key: get_simplified_mongodb_schema(value) for key, value in data.items()}
    elif isinstance(data, list):
        if data:
            return [get_simplified_mongodb_schema(data[0])]
        else:
            return []
    else:
        return VALUE_PLACEHOLDER


def calculate_number_of_tokens(encoding_engine, text):
    # Tokenize the text
    encoding = tiktoken.get_encoding(encoding_engine)
    tokens = encoding.encode(str(text))
    return len(tokens)


def trim_according_to_token_limit(text, current_tokens, token_limit):
    encoding = tiktoken.get_encoding(GPT_DEFAULT_ENCODING_ENGINE)
    overflow_rate = (current_tokens - token_limit) / current_tokens
    overflow_characters = int(len(text) * overflow_rate)
    trimmed_text = text[:-overflow_characters]
    return trimmed_text
