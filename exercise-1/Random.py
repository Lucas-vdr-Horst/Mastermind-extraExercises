import random


if __name__ == "__main__":
    cor = str(random.randint(0, 10))
    while True:
        if input("Guess a number: ") == cor:
            break
        else:
            print("Unfortunately incorrect :(")
    print("That's correct, it was {}!".format(cor))