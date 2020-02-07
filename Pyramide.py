def print_pyramide(size):
    for i in range(size):
        print('*' * (i + 1))
    for i in reversed(range(size - 1)):
        print('*' * (i + 1))


if __name__ == "__main__":
    print_pyramide(int(input("Hoe groot? ")))
