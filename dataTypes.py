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


        """
        score = 0

        compared_len = len(min(self.items, other.items))
        for i in range(compared_len):
            distance = abs(self.items[i] - other.items[i])
            score += (distance / self.tolerance) * i / 0.5
        return score / compared_len

    def __len__(self):
        return len(self.items)




class FrequencyDict:
    pass
