import random
import string


def code_generator(size):
    chars_upper = string.ascii_uppercase
    digits = string.digits
    return ''.join(random.choice(chars_upper + digits) for r in range(size))
