def sort_list(lst):
    lst: list
    new_list = []
    while len(lst) > 0:
        new_list.append(min(lst))
        lst.remove(min(lst))
    return new_list


if __name__ == "__main__":
    print(sort_list([3, 5, 2, 1, 8, 4]))
