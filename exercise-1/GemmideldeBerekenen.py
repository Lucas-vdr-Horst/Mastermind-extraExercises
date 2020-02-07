def extract_list(lst):
    new_lst = []
    for i in range(len(lst)):
        if type(lst[i]) is list:
            new_lst.extend(lst[i])
        else:
            new_lst.append(lst[i])
    if any(isinstance(x, list) for x in new_lst):
        #   still lists in new_list
        new_lst = extract_list(new_lst)
    return new_lst


def gem(lst):
    return sum(lst) / len(lst)


if __name__ == "__main__":
    print(gem(extract_list([1, [2, 2], [[4, 6], [7, 2]], 9])))
