class Location:
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.predecessor = None

    def __str__(self):
        return str(self.label)

