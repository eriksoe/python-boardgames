from board import Move

# A game player.
# This is currently a human player; this is to become a class hierarchy.
class Player:
    def __init__(self, color):
        self.color = color
        self._from = None

    def resetGame(self, board):
        self._from = None
        self._board = board

    def enterTurn(self):
        pass

    def exitTurn(self):
        self._from = None

    # Return whether to redraw.
    def onBoardClickedOnTurn(self, pos):
        piece = self._board.get(pos[0],pos[1])
        if self._from == None:
            # Select
            if piece == self.color:
                self._from = pos
                return True
        else:
            theMove = Move(self._from, pos)
            if theMove in self._board.possibleMoves():
                self._board.move(theMove)
                self._from = None
                return True
            else:
                # Unselect
                self._from = None
                return True

    def drawHighlightsOnTurn(self, app, id, size, mouseOver):
        if self._from != None:
            (mx, my) = self._from
            my = 7-my
            color = "#ee0"
            app.addCanvasRectangle(id, mx*size, my*size, size, size,
                                   width=3, outline=color, fill=None)
        if mouseOver != None:
            (mx, my) = mouseOver
            color = "#090"
            if self._from != None and Move(self._from, mouseOver) in self._board.possibleMoves():
                color = "#ee0" # Possible move
            elif self._board.get(mx, my) == self.color:
                color = "#cc0" # Possible piece to move
            app.addCanvasRectangle(id, mx*size, (7-my)*size, size, size,
                                   width=2, outline=color, fill=None)
