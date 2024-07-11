

VALUE_PLACEHOLDER = "<value>"


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
