
import tiktoken
import wonderwords

from apps.llm_transaction.costs import LLMCostsPerMillionTokens, SERVICE_PROFIT_MARGIN, VAT_TAX_RATE


def calculate_number_of_tokens(encoding_engine, text):
    # Tokenize the text
    encoding = tiktoken.get_encoding(encoding_engine)
    tokens = encoding.encode(str(text))
    return len(tokens)


def calculate_llm_cost(model, number_of_tokens):
    costs = LLMCostsPerMillionTokens.OPENAI_GPT_COSTS[model]
    tokens_divided_by_million = number_of_tokens / 1_000_000
    apx_input_cost = (tokens_divided_by_million / 2) * costs["input"]
    apx_output_cost = (tokens_divided_by_million / 2) * costs["output"]
    llm_cost = (apx_input_cost + apx_output_cost)
    return llm_cost


def calculate_internal_service_cost(llm_cost):
    return llm_cost * SERVICE_PROFIT_MARGIN


def calculate_tax_cost(internal_service_cost):
    tax_cost = internal_service_cost * VAT_TAX_RATE
    return tax_cost


def calculate_billable_cost(internal_service_cost, tax_cost):
    return internal_service_cost + tax_cost


def calculate_total_cost(llm_cost, billable_cost):
    return llm_cost + billable_cost


def sum_costs(transactions):
    llm_cost = 0
    internal_service_cost = 0
    tax_cost = 0
    total_cost = 0
    billable_cost = 0
    for transaction in transactions:
        llm_cost += transaction.llm_cost
        internal_service_cost += transaction.internal_service_cost
        tax_cost += transaction.tax_cost
        total_cost += transaction.total_cost
        billable_cost += transaction.total_billable_cost
    return {
        "llm_cost": llm_cost,
        "internal_service_cost": internal_service_cost,
        "tax_cost": tax_cost,
        "total_cost": total_cost,
        "total_billable_cost": billable_cost,
    }


def generate_chat_name():
    # use a library to generate a random chat name
    chat_name_1 = wonderwords.RandomWord().word(
        word_max_length=8,
        include_categories = ["verb"]
    )
    chat_name_2 = wonderwords.RandomWord().word(
        word_max_length=8,
        include_categories = ["adjective"]
    )
    chat_name_3 = wonderwords.RandomWord().word(
        word_max_length=8,
        include_categories = ["noun"]
    )
    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()
    return " ".join([chat_name_1, chat_name_2, chat_name_3])
