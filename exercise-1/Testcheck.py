def difference_index(str_1, str_2):
    for i in range(min(len(str_1), len(str_2))):
        if str_1[i] != str_2[i]:
            return i


if __name__ == "__main__":
    string_1 = input("Geef een string: ")
    string_2 = input("Geef een string: ")
    print("Het eerste verschil zit op index:", difference_index(string_1, string_2))
