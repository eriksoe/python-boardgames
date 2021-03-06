# **********************************************************************
# * PURPOSE: Graphics and UI for Chromodynamics
# **********************************************************************
from chromo import CDBoard, CDMove, CHROMOS
from guiboard import GameGui
from playercolor import WHITE, BLACK

class CDGfx:
    dark_square_img = "gfx/dark-square.png"
    light_square_img = "gfx/light-square.png"

def imageFor(color, chromo):
    playerStr = "W" if color==WHITE else "B"
    return "gfx/CD-%s-%s.gif" % (chromo.name, playerStr)

class CDGui(GameGui):
    SQR_SIZE = 48

    def __init__(self, app, canvasID, board):
        GameGui.__init__(self, app, canvasID, board)
        self._mouseOverSqr = None
        self._from = None
        self._currentColor = None

    def onEnterTurn(self, playerColor, moveAction):
        self._from = None
        self._currentColor = playerColor
        self._moveAction = moveAction
    def onExitTurn(self, playerColor):
        self._from = None
        self._currentColor = None
        self._moveAction = None
        
    def _eventSquare(self, event):
        bx = int(event.x / CDGui.SQR_SIZE)
        by = int(event.y / CDGui.SQR_SIZE)
        if bx>=8 or by>=8: return None
        return (bx, 7-by)

    # Return whether to redraw.
    def setMouseOver(self, event):
        pos = self._eventSquare(event) if event!=None else None
        if pos == self._mouseOverSqr:
            return
        self._mouseOverSqr = pos
        return True

    def onBoardClicked(self, color, event):
        (cx,cy) = pos = self._eventSquare(event)
        piece = self._board.get(cx, cy)
        if self._from == None:
            # Select
            if piece == self._currentColor:
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


    def drawBoard(self):
        self._drawBoardBackground()
        self._drawBoardPieces()
        self._drawSquareHighlights()

    def _drawBoardBackground(self):
        size = CDGui.SQR_SIZE
        app = self._app

        for y in xrange(8):
            for x in xrange(8):
                parity = ((x+y) & 1) > 0
                img = CDGfx.dark_square_img if parity else CDGfx.light_square_img
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

    def _drawBoardPieces(self):
        size = CDGui.SQR_SIZE
        app = self._app

        for y in xrange(8):
            for x in xrange(8):
                sqr = self._board.get(x, 7-y)
                if sqr==None: continue
                color = sqr.color
                if color==None: continue
                chromos = sqr.chromos
                for c in CHROMOS:
                    if c.containedIn(chromos):
                        img = imageFor(color, c)
                        app.addCanvasImage("c", x*size, y*size,
                                           img, anchor="nw")

    def _drawSquareHighlights(self):
        size = CDGui.SQR_SIZE
        app = self._app
        id = self._canvas

        if self._from != None:
            (mx, my) = self._from
            my = 7-my
            color = "#ee0"
            app.addCanvasRectangle(id, mx*size, my*size, size, size,
                                   width=3, outline=color, fill=None)
        if self._mouseOverSqr != None:
            (mx, my) = self._mouseOverSqr
            color = "#090"
            if self._from != None and Move(self._from, self._mouseOverSqr) in self._board.possibleMoves():
                color = "#ee0" # Possible move
            elif self._board.get(mx, my) == self._currentColor:
                color = "#cc0" # Possible piece to move
            app.addCanvasRectangle(id, mx*size, (7-my)*size, size, size,
                                   width=2, outline=color, fill=None)

        # curPlayer = self.currentPlayer()
        # if curPlayer != None:
        #     curPlayer.drawHighlightsOnTurn(self, self._app, id, size, self._mouseOver)
