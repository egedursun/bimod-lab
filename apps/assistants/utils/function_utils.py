

import random
import string


def generate_random_string(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
