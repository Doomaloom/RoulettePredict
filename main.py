import numpy as np

from dataTypes import FrequencyDict
from dataTypes import SmartTuple
from sklearn.linear_model import SGDRegressor as sgdr
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


NUMBERS = 0
REGIONS = 1
DISTANCE = 2

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


def degrees_to_number(num):
    """
        Converts degrees on a roulette wheel back to the number.

        >>> degrees_to_number(4.85)
        0
        >>> degrees_to_number(14.55)
        32
        >>> degrees_to_number(334.65)
        35
        """
    nums = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8,
            23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12,
            35, 3, 26]

    if num - 360 >= 0:
        num -= 360
    elif num + 360 <= 360:
        num += 360

    index = round((num + 4.85) / 9.7) - 1
    return nums[index]


def numbers_to_region(num):
    zero = [12, 35, 3, 26, 0, 32, 15]
    tier = [33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27]
    orphins = [9, 31, 14, 20, 1, 17, 34, 6]
    other = [28, 7, 29, 18, 22, 19, 4, 21, 2, 25]
    if num in zero:
        return 0
    if num in tier:
        return 1
    if num in orphins:
        return 2
    if num in other:
        return 3


if __name__ == '__main__':

    results = FrequencyDict(0.9)
    window = []
    window = [number_to_degrees(window[i]) for i in range(len(window))]
    user_input = ''
    mode = DISTANCE
    #model = sgdr(max_iter=1000, tol=1e-3)
    model = LinearRegression()

    while user_input != 'q':
        user_input = input('Enter a number or q to quit: ')
        if user_input == 'q':
            break
        converted = -1
        if mode == NUMBERS or DISTANCE:
            converted = number_to_degrees(int(user_input))
        elif mode == REGIONS:
            converted = numbers_to_region(int(user_input))

        s = ()
        r = 4
        answer = None
        window2 = []
        if len(window) == 30:
            window2 = [converted] + window[:2]
            print(window2)
            print()
            if mode == NUMBERS:

                #s = SmartTuple(window2, 20)
                s2 = SmartTuple(window.copy(), 20)
                #r = results.get_best_result(s)
                results.__add__(s2, int(user_input))
                window.insert(0, converted)
                window.pop()
                s = SmartTuple(window.copy(), 20)

            elif mode == REGIONS:
                #s = SmartTuple(window2, 0)
                s2 = SmartTuple(window.copy(), 0)
                #r = results.get_best_result(s)
                results.__add__(s2, numbers_to_region(int(user_input)))
                window.insert(0, converted)
                window.pop()
                s = SmartTuple(window.copy(), 0)

            elif mode == DISTANCE:
                # TODO: NEED TO MAKE THIS BASED ON DISTANCE
                # TODO: CURRENTLY USING JUST SPIN POSITION
                # TODO: x should represent the number it was on
                # TODO: y should show the degrees change from it previous number
                x = np.array([window[i] for i in range(len(
                    window) - 1)]).reshape(-1, 1)
                y = np.array([window[i] - window[i + 1] for i in range(len(
                    window) - 1)])
                model.fit(x, y)
                print(x, "\n", y)
                last_spin = np.array([window[-1]]).reshape(-1, 1)
                next_prediction = model.predict(x)
                answer = converted + next_prediction[-1]
                window.insert(0, converted)
                window.pop()

                plt.scatter(x, y)
                plt.plot(x, next_prediction)
                plt.show()




            r = results.get_best_result(s)
            #window.pop(0)

            #window = window2
        else:
            window.insert(0, converted)
        print(window)
        print(results)

        if mode == NUMBERS:
            print(results.get_best_result(s))
        if mode == DISTANCE:
            if answer:
                print(answer)
                print(degrees_to_number(answer))

        if mode == REGIONS:

            if r == 0:
                print('zero')
            elif r == 1:
                print('tier')
            elif r == 2:
                print('orphins')
            elif r == 3:
                print('other')
            else:
                print("none")
