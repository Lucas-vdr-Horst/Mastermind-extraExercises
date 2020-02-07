def reverse_string(string):
    return string[::-1]
    """new_string = ""
    for i in range(len(string)):
        new_string += string[len(string) - (i+1)]
    return new_string"""


def is_palindrome(string):
    return string.lower() == reverse_string(string).lower()


if __name__ == "__main__":
    print(is_palindrome("Racecar"))