

class LLMCostsPerMillionTokens:
    OPENAI_GPT_COSTS = {
        "gpt-4o" : {
            "input": 5.00,
            "output": 15.00,
        },
        "gpt-4-turbo" : {
            "input": 10.00,
            "output": 30.00,
        },
        "gpt-4" : {
            "input": 30.00,
            "output": 60.00,
        },
        "gpt-3.5-turbo-16k" : {
            "input": 3.00,
            "output": 4.00,
        },
        "GPT-3.5-turbo-0125" : {
            "input": 1.00,
            "output": 2.00,
        }
    }


SERVICE_PROFIT_MARGIN = 1.00

VAT_TAX_RATE = 0.18
