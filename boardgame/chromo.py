# **************************************************
# * PURPOSE: Chromodynamics game logic             *
# **************************************************
from playercolor import WHITE, BLACK
#==================== Game logic ========================================
class CDChromo:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def bit(self):
        return 1 << self.index
    def containedIn(self, chromos):
        return (chromos & self.bit()) != 0

RED = CDChromo("red", 0)
GREEN = CDChromo("green", 1)
BLUE = CDChromo("blue", 2)
KING = CDChromo("king", 3)
CHROMOS = [RED, GREEN, BLUE, KING]

class Square:
    def __init__(self, color=None, chromos=0):
        self.color = color
        self.chromos = chromos

    def set(self, color, chromos):
        if chromos==None: color = None
        self.color = color
        self.chromos = chromos

def chromoSet(*args):
    sum=0
    for c in args: sum += c.bit()
    return sum

# Initial setup data:
ROW1 = [None, 7,7,7, 15,7,7, None]
ROW2 = [None,
        chromoSet(RED, GREEN), chromoSet(RED, BLUE), chromoSet(BLUE, GREEN),
        chromoSet(BLUE, GREEN), chromoSet(RED, BLUE), chromoSet(RED, GREEN),
        None
]

class CDBoard:
    def __init__(self, cloneOf=None):
        if cloneOf==None:
            self.board = [[None for x in xrange(8)] for y in xrange(8)]
            self.nextPlayer = None
            self.winner = None
        else:
            self.board = [[cloneOf.get(x,y) for x in xrange(8)] for y in xrange(8)]
            self.nextPlayer = cloneOf.nextPlayer
            self.winner = cloneOf.winner
            self.turnNr = cloneOf.turnNr
            self._moves = cloneOf._moves

    def clone(self):
        return CDBoard(cloneOf=self)

    def get(self, x, y):
        return self.board[y][x]

    def setup(self):
        self.board = [[Square() for x in xrange(8)] for y in xrange(8)]
        for x in xrange(8):
            self.board[0][x].set(WHITE, ROW1[x])
            self.board[1][x].set(WHITE, ROW2[x])
            self.board[6][x].set(BLACK, ROW2[x])
            self.board[7][x].set(BLACK, ROW1[x])
        self.turnNr = 0
        self._moves = None
        self.nextPlayer = WHITE

    def move(self, m):
        self._doMove(m)
        self.turnNr += 1
        self._moves = None
        won = (y2==7) if self.nextPlayer == WHITE else (y2==0)
        curPlayer = self.nextPlayer
        if won:
            self.winner = self.nextPlayer
            self.nextPlayer = None
        else:
            # Turn change:
            self.nextPlayer = WHITE if self.nextPlayer == BLACK else BLACK

            # Check for no-moves game termination:
            if len(self.possibleMoves()) == 0:
                # Are both sides blocked?
                self.nextPlayer = curPlayer
                if len(self._generateMoves()) == 0:
                    self.winner = None # Draw
                else:
                    self.winner = curPlayer # Won because other player has no moves
                self.nextPlayer = None

    def _doMove(self, m):
        color = None
        for ((x,y), chromoSet) in m.srcs:
            sqr = self.board[y][x]
            color = sqr.color
            sqr.chromos &= ~chromoSet
            if sqr.chromos == 0: sqr.color = None
        for ((x,y), chromoSet) in m.dsts:
            sqr = self.board[y][x]
            if sqr.color != color:
                sqr.chromos = 0 # Capture
                sqr.color = color
            sqr.chromos |= chromoSet

    
class CDMove:
    def __init__(srcs, dsts): # srcs,dsts: [((x,y), chromo)]
        self.srcs = srcs
        self.dsts = dsts
