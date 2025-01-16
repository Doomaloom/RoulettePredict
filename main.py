import numpy as np

from dataTypes import FrequencyDict
from dataTypes import SmartTuple
from sklearn.linear_model import SGDRegressor as sgdr
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from statsmodels.miscmodels.ordinal_model import OrderedModel



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

    index = round((num + 4.85) / 9.7) - 2
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

    window_size = 20
    results = FrequencyDict(0.9)
    window = [36, 8, 9, 20, 20, 26, 25, 0, 16, 2, 1, 11, 13, 4, 4, 28, 26,
              31, 13, 23, 0, 12, 18, 27, 8, 14, 28, 10, 13, 1]
    window = []

    window = [number_to_degrees(window[i]) for i in range(len(window))]
    user_input = ''
    mode = DISTANCE
    model1 = LinearRegression()
    model2 = LinearRegression()

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
        if len(window) == window_size:

            if mode == DISTANCE:
                # TODO: NEED TO MAKE THIS BASED ON DISTANCE
                # TODO: CURRENTLY USING JUST SPIN POSITION
                # TODO: x should represent the number it was on
                # TODO: y should show the degrees change from it previous number
                x1 = np.array([window[i*2] for i in range(len(
                    window) // 2 - 1)]).reshape(-1, 1)
                y1 = np.array([window[i*2] - window[i*2 + 1] for i in range(len(
                    window) // 2 - 1)])

                x2 = np.array([window[i*2+1] for i in range(len(
                    window) // 2 - 1)]).reshape(-1, 1)
                y2 = np.array([window[i*2+1] - window[i*2 + 2] for i in range(
                    len(window) // 2 - 1)])
                model1.fit(x1, y1)
                model2.fit(x2, y2)
                #print(x, "\n", y)
                last_spin = np.array([window[-1]]).reshape(-1, 1)
                next_prediction1 = model1.predict(x1)
                next_prediction2 = model2.predict(x2)
                if len(window) % 2 != 0:
                    confidence = model1.score(x1, y1)
                    print(f"confidence: {confidence}")
                    answer = [converted - next_prediction1[-1], converted +
                              next_prediction1[-1]]
                else:
                    confidence = model2.score(x2, y2)
                    print(f"confidence: {confidence}")
                    answer = [converted - next_prediction2[-1], converted +
                              next_prediction2[-1]]
                window.insert(0, converted)
                window.pop()

                plt.scatter(x1, y1)
                plt.plot(x1, next_prediction1)
                plt.show()
                plt.scatter(x2, y2)
                plt.plot(x2, next_prediction2)
                plt.show()

        else:
            window.insert(0, converted)
        #print(window)
        #print(results)

        if mode == DISTANCE:
            if answer:
                print(f"degrees moved: {answer}")

                print(f"predicted best bet: "
                      f"{degrees_to_number(answer[0]), degrees_to_number(answer[1])}")
