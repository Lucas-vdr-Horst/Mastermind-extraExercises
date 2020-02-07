def ceasar(text, rot):
    for char_index in range(len(text)):
        char: str
        char = text[char_index]
        if char.isalpha():
            letter_number = ord(char.lower()) - 97
            letter_number = (letter_number + rot) % 26
            new_char = chr(letter_number + 97)
            if char.isupper():
                new_char = new_char.upper()
            text = text[:char_index] + new_char + text[char_index+1:]
    return text


if __name__ == "__main__":
    print(ceasar("Hello World", 4))
