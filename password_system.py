import random
import string


def generate_password(length: int, complexity: int) -> str:
    """Generate a random password with given length and complexity

    Complexity levels (modified):
        Complexity == 1: return a password with only lowercase chars and at least one lowercase char
        Complexity == 2: Previous level plus at least 1 digit
        Complexity == 3: Previous levels plus at least 1 uppercase char
        Complexity == 4: Previous levels plus at least 1 punctuation char

    :param length: number of characters
    :param complexity: complexity level
    :returns: generated password
    """

    if length < complexity or length > 100:
        print('Length can\'t be negative or smaller than complexity or bigger than 100.')
        return ""

    password = ""
    lower = string.ascii_lowercase
    lower_number = string.ascii_lowercase + string.digits
    letters_number = string.ascii_letters + string.digits
    letters_number_punctuation = string.ascii_letters + string.digits + string.punctuation

    # use while loop to make sure the password contains at least one required element
    if complexity == 1:
        password = ""
        for i in range(length):
            password += random.choice(lower)
    elif complexity == 2:
        while not (any(c.isdigit() for c in password) and any(c.islower() for c in password)):
            password = ""
            for i in range(length):
                password += random.choice(lower_number)
    elif complexity == 3:
        while not (any(c.isdigit() for c in password) and any(c.islower() for c in password) and
                   any(c.isupper() for c in password)):
            password = ""
            for i in range(length):
                password += random.choice(letters_number)
    elif complexity == 4:
        while not (any(c.isdigit() for c in password) and any(c.islower() for c in password) and
                   any(c.isupper() for c in password) and any(c in string.punctuation for c in password)):
            password = ""
            for i in range(length):
                password += random.choice(letters_number_punctuation)
    else:
        print('Complexity can only be 1 ~ 4. Got ', complexity)

    return password


def check_password_level(password: str) -> int:
    """Return the password complexity level for a given password

    Complexity levels (modified)::
        Return complexity 1: If password has only lowercase chars and at least one lowercase char
        Return complexity 2: Previous level condition and at least 1 digit
        Return complexity 3: Previous levels condition and at least 1 uppercase char
        Return complexity 4: Previous levels condition and at least 1 punctuation
        Return complexity 1: All other conditions

    Complexity level exceptions (override previous results):
        Return complexity 2: password has length >= 8 chars and complexity 1
        Return complexity 3: password has length >= 8 chars and complexity 2

    :param password: password
    :returns: complexity level
    """

    contain_digit = any(c.isdigit() for c in password)
    contain_lower = any(c.islower() for c in password)
    contain_upper = any(c.isupper() for c in password)
    contain_punctuation = any(c in string.punctuation for c in password)
    longer_than_eight = len(password) >= 8

    if contain_lower and contain_upper and contain_digit and contain_punctuation:
        return 4
    elif contain_lower and contain_digit and (contain_upper or longer_than_eight):
        return 3
    elif contain_lower and (contain_digit or longer_than_eight):
        return 2
    elif contain_lower:
        return 1
    else:
        return 1

