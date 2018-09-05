class Color:
    def __init__(self, name, dy):
        self.name = name
        self._dy = dy
        self._homeRow = int((7 - 5*dy)/2)

    def pawn_img(self):
        return "../gfx/%s-pawn.png" % (self.name,)

    def forwardY(self):
        return self._dy

    def homeRow(self):
        return self._homeRow

    def turnIcon(self):
        return "../gfx/%s-circle.png" % (self.name,)
    def wonIcon(self):
        return "../gfx/%s-circle-glow.png" % (self.name,)

    def __str__(self):
        return self.name

WHITE = Color("white", 1)
BLACK = Color("black", -1)

class Board:
    def __init__(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]
        self.nextPlayer = None
        self.winner = None

    def get(self, x, y):
        return self.board[y][x]

    def move(self, m):
        (x1,y1) = m.src
        (x2, y2) = m.dst
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None
        self.turnNr += 1
        self._moves = None
        won = (y2==7) if self.nextPlayer == WHITE else (y2==0)
        if won:
            self.winner = self.nextPlayer
            self.nextPlayer = None
        else:
            self.nextPlayer = WHITE if self.nextPlayer == BLACK else BLACK

    def setup(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]
        for x in xrange(8):
            self.board[1][x] = WHITE
            self.board[6][x] = BLACK
        self.turnNr = 0
        self._moves = None
        self.nextPlayer = WHITE

    def possibleMoves(self):
        if self._moves == None:
            self._moves = self._generateMoves()
        return self._moves

    def _generateMoves(self):
        # For now, we generate for both colors.
        moves = []
        for y in xrange(8):
            for x in xrange(8):
                p = self.board[y][x]
                if p != self.nextPlayer:
                    continue
                dy = p.forwardY()
                # Add normal moves:
                y1 = y + dy
                if y1<0 or y1>=8: continue
                if self.board[y1][x] == None:
                    moves.append(Move((x,y), (x,y1)))
                    if y == p.homeRow():
                        y2 = y1 + dy
                        if y2<0 or y2>=8: continue
                        if self.board[y2][x] == None:
                            moves.append(Move((x,y), (x,y2)))
                # Add taking moves:
                x1 = x+1
                if x1<8:
                    p2 = self.board[y1][x1]
                    if p2!=None and p2!=p:
                        moves.append(Move((x,y), (x1,y1)))

                x1 = x-1
                if x1>=0:
                    p2 = self.board[y1][x1]
                    if p2!=None and p2!=p:
                        moves.append(Move((x,y), (x1,y1)))
        return moves

class Move:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst
