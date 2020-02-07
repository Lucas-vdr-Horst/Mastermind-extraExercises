def cycle_bits(ch, n):
    string = str(ch)
    for i in range(abs(n)):
        if n > 0:
            string = string[1:] + string[0]
        else:
            string = string[-1] + string[:-1]
    return string


if __name__ == "__main__":
    print(cycle_bits('1011100', -4))
