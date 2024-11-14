class SmartTuple:

    tolerance: int
    items: list

    def __init__(self, items: list, tolerance: int):
        self.items = items
        self.tolerance = tolerance

    def __eq__(self, other) -> float:
        """
        Compares two tuples with a tolerance range and returns a score
        score shows how similar two tuples are 1 being the most similar and 0
        being the least

        >>> s1 = SmartTuple([20, 20, 20], 10)
        >>> s2 = SmartTuple([10, 10, 20], 10)
        >>> s1 == s2
        poop
        >>> s1 = SmartTuple([20, 20, 20], 10)
        >>> s2 = SmartTuple([20, 20, 20], 10)
        >>> s1 == s2
        1.0
        >>> s1 = SmartTuple([20, 20, 20], 6)
        >>> s2 = SmartTuple([10, 10, 15], 6)
        >>> s1 == s2
        0.3
        >>> s1 = SmartTuple([5], 20)
        >>> s2 = SmartTuple([355], 20)
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
        return len(self)

    def __str__(self):
        return str(self.items)


class BetterDict(dict):
    def __contains__(self, item):
        for k in self.keys():
            if item == k:
                return True
        return False

    def __getitem__(self, key):
        for thing in self.values():
            if thing[0] == key:
                return thing[1]
        return None

    def __setitem__(self, key, value):
        for thing in self.values():
            if thing[0] == key:
                thing[1] = value
                return
        dict.__setitem__(self, key, value)


class FrequencyDict:

    keys: list[SmartTuple]
    values: list[dict]

    def __init__(self):
        self.keys = []
        self.values = []

    def __add__(self, run: SmartTuple, result: int):
        for i in range(len(self.keys)):
            if (self.keys[i] == run) > 0.3:
                if result in self.values[i]:
                    self.values[i][result] += 1
                else:
                    self.values[i][result] = 1
                return
        self.keys.append(run)
        self.values.append({result: 1})

    def get_best_result(self, run: SmartTuple):
        max_value = 0
        max_num = None
        for i in range(len(self.keys)):
            if (self.keys[i] == run) > 0.3:
                for j in self.values[i]:
                    if self.values[i][j] > max_value:
                        max_value = self.values[i][j]
                        max_num = j
        return max_num

    def __str__(self):
        s = ""
        for i in range(len(self.keys)):
            s += f"{self.keys[i]} : {self.values[i]} \n"
        return s