import random
import string


def generate_random_string(length=16):
    print(f"[utils.generate_random_string] Generating a random string with the length: {length}.")
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
