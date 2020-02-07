def count(lst, element):
    return lst.count(element)
    """lst: list
    amount = 0
    for i in lst:
        if i == element:
            amount += 1
    return amount"""


def largest_diff(lst):
    diffs = []
    for i in range(len(lst)):
        diff = abs(lst[i] - lst[(i+1) % len(lst)])
        diffs.append(diff)
    return max(diffs)


def is_list_valid(lst):
    amount_1, amount_0 = count(lst, 1), count(lst, 0)
    return amount_1 > amount_0 and amount_0 <= 12


if __name__ == "__main__":
    test_list = [1, 5, 4, 3, 7, 8, 2, 1, 3, 4]
    print(count(test_list, 3))
    print(largest_diff(test_list))
