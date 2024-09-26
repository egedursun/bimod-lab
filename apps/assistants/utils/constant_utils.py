

ASSISTANT_RESPONSE_LANGUAGES = [
    # User's question language
    ("auto", "Auto (Detect)"),
    ("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German"), ("it", "Italian"),
    ("pt", "Portuguese"), ("nl", "Dutch"), ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
    ("zh", "Chinese"), ("ar", "Arabic"), ("tr", "Turkish"), ("pl", "Polish"), ("sv", "Swedish"),
    ("da", "Danish"), ("fi", "Finnish"), ("no", "Norwegian"), ("he", "Hebrew"), ("id", "Indonesian"),
    ("ms", "Malay"), ("th", "Thai"), ("hi", "Hindi"), ("hu", "Hungarian"), ("cs", "Czech"),
    ("sk", "Slovak"), ("uk", "Ukrainian"), ("ro", "Romanian"), ("bg", "Bulgarian"), ("el", "Greek"),
    ("fi", "Finnish"), ("et", "Estonian"), ("lv", "Latvian"), ("lt", "Lithuanian"), ("hr", "Croatian"),
    ("sr", "Serbian"), ("sl", "Slovenian"), ("mk", "Macedonian"), ("sq", "Albanian"), ("bs", "Bosnian"),
    ("is", "Icelandic"), ("cy", "Welsh"), ("ga", "Irish"),
]
ASSISTANT_RESPONSE_LANGUAGES = [ASSISTANT_RESPONSE_LANGUAGES[0]] + sorted(ASSISTANT_RESPONSE_LANGUAGES[1:],
                                                                          key=lambda x: x[1])

CONTEXT_OVERFLOW_STRATEGY = [
    ("stop", "Stop Conversation"),
    ("forget", "Forget Oldest Messages"),
    ("vectorize", "Vectorize Oldest Messages"),
]


class ContextOverflowStrategyNames:
    STOP = "stop"
    FORGET = "forget"
    VECTORIZE = "vectorize"

    @staticmethod
    def as_dict():
        return {"stop": "Stop Conversation", "forget": "Forget Oldest Messages",
                "vectorize": "Vectorize Oldest Messages"}


VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class VectorizerNames:
    TEXT2VEC_OPENAI = "text2vec-openai"

    @staticmethod
    def as_dict():
        return {"text2vec-openai": "Text2Vec (OpenAI)"}
