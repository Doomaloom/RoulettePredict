# class that contains a prediction object for roulette
import numpy as np

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


class Predictor:
    window_size: int
    window: list[float]
    model: LinearRegression
    last_spin: float
    x: np.array
    y: np.array
    next_prediction: any

    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = []
        self.model = LinearRegression()
        self.last_spin = 0
        self.x = np.array([self.window[i] for i in range(len(
            self.window) - 1)]).reshape(-1, 1)
        self.y = np.array([self.window[i] - self.window[i + 1] for i in range(
            len(
                self.window) - 1)])
        self.next_prediction = None

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
        if len(self.window) % 2 == 0:
            self.x = np.array([self.window[i * 2] for i in range(len(
                self.window) // 2 - 1)]).reshape(-1, 1)
            self.y = np.array([self.window[i * 2] - self.window[i * 2 + 1] for i
                               in range(len(self.window) // 2 - 1)])
        else:
            self.x = np.array([self.window[i * 2 + 1] for i in range(len(
                self.window) // 2 - 1)]).reshape(-1, 1)
            self.y = np.array([self.window[i * 2 + 1] - self.window[i * 2 + 2]
                               for i in range(len(self.window) // 2 - 1)])

        self.model.fit(self.x, self.y)
        self.next_prediction = self.model.predict(self.x)
        answer = self.last_spin + self.next_prediction[-1]

        return answer, self.model.score(self.x, self.y)

    def graph(self):

        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.next_prediction)
        plt.title(str(self.window_size))
        plt.xlabel("degrees")
        plt.show()

    def __str__(self) -> str:
        return f"Predictor with window size {self.window_size}: "
