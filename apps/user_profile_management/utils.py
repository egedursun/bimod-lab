import re


def get_card_type(card_number):
    card_types = {
        'visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
        'mastercard': r'^5[1-5][0-9]{14}$',
        'amex': r'^3[47][0-9]{13}$',
    }
    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            return card_type
    return "visa"
