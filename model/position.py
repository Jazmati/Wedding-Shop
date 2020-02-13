
class Position:

    def __init__(self, abscissa, ordinate):
        self.abscissa = abscissa
        self.ordinate = ordinate

    def __str__(self):
        return f'{self.abscissa} {self.ordinate}'

    def __eq__(self, other):
        return self.abscissa == other.abscissa and self.ordinate == other.ordinate
