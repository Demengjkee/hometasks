#!/usr/bin/python


def merge(first_list, second_list):
    result = []
    for value in first_list:
        if value in second_list:
            result.append(value)

    return set(result)


if __name__ == "__main__":
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    print(merge(a, b))
