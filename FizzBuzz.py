for i in range(1, 100):
    fizz, buzz = i % 3 == 0, i % 5 == 0
    if fizz:
        print('Fizz', end='')
    if buzz:
        print('Buzz', end='')
    if not(fizz or buzz):
        print(i, end='')
    print()
