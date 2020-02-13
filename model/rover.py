
class Rover:

    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def __str__(self):
        return f'{self.position} {self.orientation}'

    def __eq__(self, other):
        return self.position == other.position and self.orientation == other.orientation
