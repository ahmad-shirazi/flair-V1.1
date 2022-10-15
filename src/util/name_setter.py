import random
import string


def get_random_name(length=10):
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for _ in range(length))
    return name
