# class that contains a prediction object for roulette
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

class Predictor:

    window_size: int
    window: list[float]
    model: LinearRegression
    last_spin: float

    def __init__(self, window_size:int):
        self.window_size = window_size
        self.window = []
        self.model = LinearRegression()
        self.last_spin = 0

    def add_spin(self, number: float):
        if self.window_size <= len(self.window):
            self.window.pop(0)
        self.window.append(number)

    def ready_to_predict(self) -> bool:
        if self.window_size == 77:
            return len(self.window) >= 10

        return len(self.window) >= self.window_size

    def predict(self) -> tuple[float, float]:
        # prediction will be returned as predicted number, confidence

        x = np.array([self.window[i] for i in range(len(
            self.window) - 1)]).reshape(-1, 1)
        y = np.array([self.window[i] - self.window[i + 1] for i in range(len(
            self.window) - 1)])
        self.model.fit(x, y)
        next_prediction = self.model.predict(x)
        answer = self.last_spin + next_prediction[-1]

        # plt.scatter(x, y)
        # plt.plot(x, next_prediction)
        # plt.show()

        return answer, self.model.score(x, next_prediction)

    def graph(self):
        pass

    def __str__(self) -> str:
        return f"Predictor with window size {self.window_size}: "
