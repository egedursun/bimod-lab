import datetime
import random
import string


def generate_random_string(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_referral_code(length=16):
    alphas = string.ascii_uppercase # 26
    numerics = string.digits  # 10
    year = datetime.datetime.now().year.__str__()
    month = datetime.datetime.now().month.__str__()
    day = datetime.datetime.now().day.__str__()
    generated_alpha = ''.join(random.choice(alphas) for _ in range(length // 2))
    generated_numeric = ''.join(random.choice(numerics) for _ in range(length // 2))
    generated_date = f"{year}-{month}{day}"
    return f"{generated_alpha[0:4]}-{generated_alpha[4:]}-{generated_numeric[0:4]}-{generated_numeric[4:]}-{generated_date}0"
