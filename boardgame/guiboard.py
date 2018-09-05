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

    def __init__(self, app, board, players):
        self._app = app
        self._board = board
        self._players = players

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

    def setPlayers(self, players):
        self._players = players

    def playerOfColor(self, color):
        if color==None: return None
        return self._players[color.index]

    def currentPlayer(self):
        curPlayerColor = self._board.nextPlayer
        return self.playerOfColor(curPlayerColor)

    def onBoardClicked(self, event):
        curPlayer = self.currentPlayer()
        if curPlayer != None:
            pos = self.eventSquare(event)
            change = curPlayer.onBoardClickedOnTurn(pos)
            if change:
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

        curPlayer = self.currentPlayer()
        if curPlayer != None:
            curPlayer.drawHighlightsOnTurn(app, "c", size, self._mouseOver)

    def updateIcon(self):
        app = self._app
        curPlayerColor = self._board.nextPlayer

        id = "stateCanvas"
        app.clearCanvas(id)
        c = self._stateCanvas

        app.addCanvasCircle(id, 0, 0, 36, fill="#999", outline="#999")
        app.addCanvasCircle(id, 0, 72, 36, fill="#999", outline="#999")
        app.addCanvasRectangle(id, 0, 18, 36, 2*36, fill="#999", outline="#999")

        (x,y,icon) = (0,0, Icons.empty_icon)
        if curPlayerColor==WHITE:
            y = 2*36
            icon = Icons.white_turn_icon
        elif curPlayerColor==BLACK:
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
