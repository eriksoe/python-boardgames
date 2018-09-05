from board import Move, Color, WHITE, BLACK

class Icons:
    dark_square_img = "gfx/dark-square.png"
    light_square_img = "gfx/light-square.png"

    empty_icon = "gfx/empty.png"
    idle_icon = "gfx/idle.png"
    white_turn_icon = "gfx/white-circle.png"
    black_turn_icon = "gfx/black-circle.png"
    white_won_icon = "gfx/white-circle-glow2.png"
    black_won_icon = "gfx/black-circle-glow2.png"

class GuiBoard:
    SQR_SIZE = 48

    def __init__(self, app, board):
        self._app = app
        self._board = board

        c = app.addCanvas("c")
        app.setCanvasWidth("c", 8 * GuiBoard.SQR_SIZE)
        app.setCanvasHeight("c", 8 * GuiBoard.SQR_SIZE)
        app.setCanvasBg("c", "#999")
        app.setCanvasRelief("c", "sunken")

        c.bind("<Button-1>", self.onBoardClicked)
        c.bind("<Double-Button-1>", self.onBoardDoubleClicked)
        c.bind("<B1-Motion>", self.onBoardDrag)
        c.bind("<ButtonRelease-1>", self.onBoardReleased)
        c.bind("<Motion>", self.onBoardMotion)
        c.bind("<Leave>", self.onBoardLeave)

        self._canvas = c

        app.startFrame("stateIconsFrame", row=0, column=1)
        stateCanvas = app.addCanvas("stateCanvas")
        app.setCanvasWidth("stateCanvas", 36)
        app.setCanvasHeight("stateCanvas", 3*36)
        app.stopFrame()
        self._stateCanvas = stateCanvas

        self._mouseOver = None
        self._from = None

    def onBoardClicked(self, event):
        if self._board.nextPlayer==None:
            return
        pos = self.eventSquare(event)
        piece = self._board.get(pos[0],pos[1])
        if self._from == None:
            # Select
            if piece == self._board.nextPlayer:
                self._from = pos
                self.redraw()
        else:
            #self._board.move(Move(self._from, pos))
            theMove = Move(self._from, pos)
            if theMove in self._board.possibleMoves():
                self._board.move(theMove)
                self._from = None
                self.redraw()
            else:
                # Unselect
                self._from = None
                self.redraw()

    def onBoardDoubleClicked(self, event):
        pass #print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    def onBoardDrag(self, event):
        pass #print("onBoardDrag(%s; %s,%s)" % (event, event.x, event.y))

    def onBoardDoubleClicked(self, event):
        pass #print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    def onBoardDrag(self, event):
        pass #print("onBoardDrag(%s; %s,%s)" % (event, event.x, event.y))

    def onBoardDoubleClicked(self, event):
        self.onBoardClicked(event)
        pass #print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    # def onBoardDrag(self, event):
    #     pass #print("onBoardDrag(%d,%d)" % (event.x, event.y))
    def onBoardReleased(self, event):
        pass #print("onBoardReleased(%d,%d)" % (event.x, event.y))
    def onBoardMotion(self, event):
        self.setMouseOver(self.eventSquare(event))
    def onBoardLeave(self, event):
        self.setMouseOver(None)

    def eventSquare(self, event):
        bx = int(event.x / GuiBoard.SQR_SIZE)
        by = int(event.y / GuiBoard.SQR_SIZE)
        return (bx, 7-by)

    def setMouseOver(self, pos):
        if pos == self._mouseOver:
            return
        self._mouseOver = pos
        self.redraw()

    def redraw(self):
        app = self._app
        c = self._canvas
        app.clearCanvas("c")

        self.updateIcon()
        self._drawBoardBackground()
        self._drawBoardPieces()
        self._drawSquareHighlights()

    def _drawBoardBackground(self):
        size = GuiBoard.SQR_SIZE
        app = self._app

        for y in xrange(8):
            for x in xrange(8):
                parity = ((x+y) & 1) > 0
                img = Icons.dark_square_img if parity else Icons.light_square_img
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

    def _drawBoardPieces(self):
        size = GuiBoard.SQR_SIZE
        app = self._app

        for y in xrange(8):
            for x in xrange(8):
                b = self._board.get(x, 7-y)
                if b==None: continue
                img = b.pawn_img()
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

    def _drawSquareHighlights(self):
        size = GuiBoard.SQR_SIZE
        app = self._app

        if self._from != None:
            (mx, my) = self._from
            my = 7-my
            color = "#ee0"
            app.addCanvasRectangle("c", mx*size, my*size, size, size,
                                   width=3, outline=color, fill=None)
        if self._mouseOver != None:
            (mx, my) = self._mouseOver
            color = "#090"
            if self._from != None and Move(self._from, self._mouseOver) in self._board.possibleMoves():
                color = "#ee0" # Possible move
            elif self._board.nextPlayer != None and self._board.get(mx, my) == self._board.nextPlayer:
                color = "#cc0" # Possible piece to move
            app.addCanvasRectangle("c", mx*size, (7-my)*size, size, size,
                                   width=2, outline=color, fill=None)

    def updateIcon(self):
        app = self._app
        curPlayer = self._board.nextPlayer

        id = "stateCanvas"
        app.clearCanvas(id)
        c = self._stateCanvas

        app.addCanvasCircle(id, 0, 0, 36, fill="#999", outline="#999")
        app.addCanvasCircle(id, 0, 72, 36, fill="#999", outline="#999")
        app.addCanvasRectangle(id, 0, 18, 36, 2*36, fill="#999", outline="#999")

        (x,y,icon) = (0,0, Icons.empty_icon)
        if curPlayer==WHITE:
            y = 2*36
            icon = Icons.white_turn_icon
        elif curPlayer==BLACK:
            y = 0
            icon = Icons.black_turn_icon
        else:
            winner = self._board.winner
            if winner==WHITE:
                y = 2*36
                icon = Icons.white_won_icon
            elif winner==BLACK:
                y = 0
                icon = Icons.black_won_icon
            else:
                y = 36
                icon = Icons.idle_icon

        app.addCanvasImage(id, x, y, icon, anchor="nw")
