MODEL_TYPES = [
    ('gpt-4o-mini', 'GPT-4o Mini'),
    ('gpt-4o', 'GPT-4o'),
    ('gpt-4', 'GPT-4'),
]

FINE_TUNING_MODEL_PROVIDERS = [
    ('openai', 'OpenAI'),
]


class FineTunedModelTypesNames:
    GPT_4O_MINI = 'gpt-4o-mini'
    GPT_4O = 'gpt-4o'
    GPT_4 = 'gpt-4'

    @staticmethod
    def as_list():
        return [
            FineTunedModelTypesNames.GPT_4O_MINI,
            FineTunedModelTypesNames.GPT_4O,
            FineTunedModelTypesNames.GPT_4,
        ]


class FineTuningModelProvidersNames:
    OPENAI = 'openai'

    @staticmethod
    def as_list():
        return [
            FineTuningModelProvidersNames.OPENAI,
        ]
