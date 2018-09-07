from board import Move
import random
import time

# A game player (abstract base class).
class Player:
    def __init__(self, color):
        self.color = color
        self._moveAction = None

    def resetGame(self, board, app):
        self._board = board
        self._app = app
        self._moveAction = None
        self.onResetGame()
    def onResetGame(self): pass # Hook for subclasses

    def enterTurn(self, moveAction):
        self._moveAction = moveAction
        self.onEnterTurn()
    def exitTurn(self):
        self._moveAction = None
        self.onExitTurn()

    def onEnterTurn(self): pass # Hook
    def onExitTurn(self): pass # Hook

    def onBoardClickedOnTurn(self, pos): pass # Hook
    def drawHighlightsOnTurn(self, app, id, size, mouseOver): pass # Hook

class RandomPlayer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def onEnterTurn(self):
        move = random.choice(self._board.possibleMoves())
        self._moveAction(move)

class ThreadedPlayer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def onEnterTurn(self):
        self._app.threadCallback(self.selectMove, self._afterMoveSelected)

    def _afterMoveSelected(self, move):
        self._moveAction(move)

    def selectMove(self):
        raise Exception("Abstract method not implemented")


class SlowRandomPlayer(ThreadedPlayer):
    def __init__(self, color):
        ThreadedPlayer.__init__(self, color)

    def selectMove(self):
        time.sleep(1)
        move = random.choice(self._board.possibleMoves())
        return move

# A human game player controlling pieces through the UI.
class HumanPlayer(Player):
    def __init__(self, color):
        Player.__init__(self, color)
        self._from = None

    def onResetGame(self): self._from = None
    def onEnterTurn(self): self._from = None
    def onExitTurn(self): self._from = None

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
                self._moveAction(theMove)
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
