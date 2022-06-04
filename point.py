class Point:

    def __init__(self, coords):
        self.coords = coords[:-1]
        self.label = coords[-1]
