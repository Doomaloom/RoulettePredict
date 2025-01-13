from predictor import Predictor


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


if __name__ == '__main__':

    user_input = ''
    predictor1 = Predictor(10)
    predictor2 = Predictor(20)
    predictor3 = Predictor(50)
    # window keeps growing. will predict starting from 10 spins
    predictor4 = Predictor(77)

    predictors = [predictor1, predictor2, predictor3, predictor4]

    while user_input != 'q':
        user_input = input('Enter a number or q to quit: ')
        if user_input == 'q':
            break

        converted = number_to_degrees(int(user_input))

        for p in predictors:
            p.add_spin(converted)

            if p.ready_to_predict():
                prediction = p.predict()
                next_number = degrees_to_number(prediction[0])
                print(f"{p}next number: {next_number}, confidence: "
                      f"{prediction[1]}")

