from board import Move
import random
import time

# A game player (abstract base class).
class Player:
    def __init__(self, color):
        self.color = color
        self._moveAction = None

    def resetGame(self, board, app, gameGui):
        self._board = board
        self._app = app         # Used by ThreadedPlayer to access threading
        self._gameGui = gameGui # Used by HumanPlayer to handle GUI
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

    def onBoardClickedOnTurn(self, event): pass # Hook

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
        self._app.threadCallback(self._aroundSelectMove, self._afterMoveSelected)

    def _aroundSelectMove(self):
        time.sleep(1) # To prevent initial GUI freeze. Don't know why necessary.
        return self.selectMove()

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

    def onEnterTurn(self):
        self._gameGui.onEnterTurn(self.color, self._moveAction)
    def onExitTurn(self):
        self._gameGui.onExitTurn(self.color)

    # Return whether to redraw.
    def onBoardClickedOnTurn(self, event):
        return self._gameGui.onBoardClicked(self.color, event)
        # piece = self._board.get(pos[0],pos[1])
        # if self._from == None:
        #     # Select
        #     if piece == self.color:
        #         self._from = pos
        #         return True
        # else:
        #     theMove = Move(self._from, pos)
        #     if theMove in self._board.possibleMoves():
        #         self._moveAction(theMove)
        #         self._from = None
        #         return True
        #     else:
        #         # Unselect
        #         self._from = None
        #         return True

    def drawHighlightsOnTurn(self, id, size, mouseOver):
        return self._gameGui.drawHighlightsOnTurn(id, size, mouseOver)

        # if self._from != None:
        #     (mx, my) = self._from
        #     my = 7-my
        #     color = "#ee0"
        #     app.addCanvasRectangle(id, mx*size, my*size, size, size,
        #                            width=3, outline=color, fill=None)
        # if mouseOver != None:
        #     (mx, my) = mouseOver
        #     color = "#090"
        #     if self._from != None and Move(self._from, mouseOver) in self._board.possibleMoves():
        #         color = "#ee0" # Possible move
        #     elif self._board.get(mx, my) == self.color:
        #         color = "#cc0" # Possible piece to move
        #     app.addCanvasRectangle(id, mx*size, (7-my)*size, size, size,
        #                            width=2, outline=color, fill=None)
