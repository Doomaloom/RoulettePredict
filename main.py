# a subclass of a python tuple that checks equality of two tuples using a range of tolerance
class ToleranceTuple(tuple):
    def __eq__(self, other):
        return all(abs(a - b) <= 20 for a, b in zip(self, other))
    
