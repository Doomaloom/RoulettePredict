class SmartTuple():

    items: tuple
    tolerance: int

    def __init__(self, items: tuple, tolerance: int):
        self.items = items
        self.tolerance = tolerance

    def __eq__(self, other) -> float:
        """
        Compares two tuples with a tolerance range and returns a score
        score shows how similar two tuples are 1 being the most similar and 0
        being the least

        >>> s1 = SmartTuple((20, 20, 20), 10)
        >>> s2 = SmartTuple((10, 10, 20), 10)
        >>> s1 == s2
        poop
        >>> s1 = SmartTuple((20, 20, 20), 10)
        >>> s2 = SmartTuple((20, 20, 20), 10)
        >>> s1 == s2
        1.0
        >>> s1 = SmartTuple((20, 20, 20), 6)
        >>> s2 = SmartTuple((10, 10, 15), 6)
        >>> s1 == s2
        0.3
        >>> s1 = SmartTuple((5,), 20)
        >>> s2 = SmartTuple((355,), 20)
        >>> s1 == s2
        1

        """
        score = 0

        compared_len = len(min(self.items, other.items))
        for i in range(compared_len):
            distance = abs(self.items[i] - other.items[i])
            if distance >= 360 - self.tolerance:
                distance = 360 - distance
            if distance <= self.tolerance:
                score += (self.tolerance - distance) / self.tolerance

        return score / compared_len

    def __len__(self):
        return len(self.items)


class FrequencyDict:

    items: list[any]
    freq: list[int]

    def __init__(self, items: list[any], freq: list[int]):
        self.items = items
        self.freq = freq

    def append(self, item: any, freq: int):
        if item in self:
            for i in range(len(self.items)):
                if self.items[i] == item > 0:
                    self.freq[i] += freq
        else:
            self.items.append(item)
            self.freq.append(freq)

    def __contains__(self, item: any):
        for i in self.items:
            if i == item:
                return True
        return False

