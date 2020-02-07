def fibonaci(n):
    if n in (1, 2):
        return 1
    return fibonaci(n-1) + fibonaci(n-2)


if __name__ == "__main__":
    print(fibonaci(5))