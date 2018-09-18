class Color:
    def __init__(self, name, index, weight):
        self.name = name
        self.index = index
        self._weight = weight
        self._homeRow = int((7 - 5*weight)/2)

    def pawn_img(self):
        return "gfx/%s-pawn.png" % (self.name,)

    def forwardY(self):
        return self._weight

    def weight(self):
        return self._weight

    def homeRow(self):
        # TODO: move to chess Board class.
        return self._homeRow

    def turnIcon(self):
        return "gfx/%s-circle.png" % (self.name,)
    def wonIcon(self):
        return "gfx/%s-circle-glow.png" % (self.name,)

    def __str__(self):
        return self.name

WHITE = Color("white", 0, 1)
BLACK = Color("black", 1, -1)
