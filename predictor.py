# class that contains a prediction object for roulette
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


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


def region_to_name(reg: int):
    if reg == 0:
        return 'zero'
    elif reg == 1:
        return 'tier'
    elif reg == 2:
        return 'orphins'
    elif reg == 3:
        return 'other'


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


def get_diff(spot1: float, spot2: float) -> float:
    diff = spot1 - spot2
    if diff > 180:
        diff -= 180
        diff *= -1
    elif diff < -180:
        diff += 180
        diff *= -1
    return diff


class Predictor:
    window_size: int
    window: list[float]
    model: any([LinearRegression, LogisticRegression])
    last_spin: float
    x: np.array
    y: np.array
    next_prediction: any
    file: any

    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = []
        #self.model = LinearRegression()
        self.model = LogisticRegression()
        self.last_spin = 0
        self.x = np.array([self.window[i] for i in range(len(
            self.window) - 1)]).reshape(-1, 1)
        self.y = np.array([self.window[i] - self.window[i + 1] for i in range(
            len(
                self.window) - 1)])
        self.next_prediction = None
        self.file = open("nums.txt", "w")

    def add_spin(self, number: float):
        if self.window_size <= len(self.window):
            self.window.pop(0)
        self.window.append(number)
        self.file.write(f"{degrees_to_number(number)}\n")

    def ready_to_predict(self) -> bool:
        if self.window_size == 77:
            return len(self.window) >= 10

        return len(self.window) >= self.window_size

    def predict(self) -> tuple[float, float]:
        # prediction will be returned as predicted number, confidence
        if len(self.window) % 2 == 0:
            self.x = np.array([self.window[i] for i in range(0, len(
                self.window), 2)]).reshape(-1, 1)
            self.y = np.array([get_diff(self.window[i + 1], self.window[i])
                               for i in range(0, len(self.window) - 1, 2)])
        else:
            self.x = np.array([self.window[i] for i in range(1, len(
                self.window) - 1, 2)]).reshape(-1, 1)
            self.y = np.array([get_diff(self.window[i + 1], self.window[i])
                               for i in range(1, len(self.window), 2)])

        self.model.fit(self.x, self.y)
        self.next_prediction = self.model.predict(self.x)
        answer = self.last_spin + self.next_prediction[-1]

        return answer, self.model.score(self.x, self.y)

    def predict2(self) -> tuple[float, float]:
        # prediction will be returned as predicted number, confidence
        if len(self.window) % 2 == 0:
            self.x = np.array([self.window[i] for i in range(0, len(
                self.window), 2)]).reshape(-1, 1)
            self.y = np.array([numbers_to_region(degrees_to_number(
                self.window[i])) for i in
                               range(0, len(self.window) - 1, 2)])
        else:
            self.x = np.array([self.window[i] for i in range(1, len(
                self.window) - 1, 2)]).reshape(-1, 1)
            self.y = np.array([numbers_to_region(degrees_to_number(
                self.window[i + 1]))
                               for i in range(1, len(self.window), 2)])

        self.model.fit(self.x, self.y)
        self.next_prediction = self.model.predict(self.x)
        answer = region_to_name(self.next_prediction[-1])

        return answer, self.model.score(self.x, self.y)

    def graph(self):

        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.next_prediction)
        plt.title(str(self.window_size))
        plt.xlabel("degrees")
        plt.show()

    def __str__(self) -> str:
        return f"Predictor with window size {self.window_size}: "
