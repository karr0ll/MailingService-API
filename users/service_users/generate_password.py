import random
import string


def password_generator(size):
    chars_upper = string.ascii_uppercase
    chars_lower = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(chars_upper + chars_lower + digits) for r in range(size))
