from dataTypes import FrequencyDict
from dataTypes import SmartTuple


def number_to_degrees(num):
    """
    Converts a number to degrees on a roulette wheel

    >>> number_to_degrees(0)
    4.85
    >>> number_to_degrees(32)
    14.549999999999999
    >>> number_to_degrees(35)
    334.65

    """
    nums = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8,
            23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12,
            35, 3, 26]
    return (nums.index(num) + 1) * 9.7 - 4.85


if __name__ == '__main__':

    results = FrequencyDict()
    window = []
    user_input = ''

    while user_input != 'q':
        user_input = input('Enter a number or q to quit: ')
        if user_input == 'q':
            break
        converted = number_to_degrees(int(user_input))

        if len(window) == 3:
            s = SmartTuple(window.copy(), 20)
            results.__add__(s, int(user_input))
            window.pop(0)

        window.append(converted)
        print(window)
        print(results)
        s = SmartTuple(window, 20)
        print(results.get_best_result(s))
