from playercolor import Color, WHITE, BLACK
from board import Move

class Icons:
    dark_square_img = "gfx/dark-square.png"
    light_square_img = "gfx/light-square.png"

    empty_icon = "gfx/empty.png"
    idle_icon = "gfx/idle.png"
    white_turn_icon = "gfx/white-circle.png"
    black_turn_icon = "gfx/black-circle.png"
    white_won_icon = "gfx/white-circle-glow2.png"
    black_won_icon = "gfx/black-circle-glow2.png"

# Abstract class.
class GameGui:
    def __init__(self, app, canvasID, board):
        self._app = app
        self._canvas = canvasID
        self._board = board

    def drawBoard(self):
        raise Exception("Not implemented")        
        
    def onEnterTurn(self, moveAction):
        raise Exception("Not implemented")        
    def onBoardClicked(self, color, event):
        raise Exception("Not implemented")

    
class GuiBoard:
    SQR_SIZE = 48 #TODO: Replace with total size

    def __init__(self, app, gameGui, board, players):
        self._app = app
        self._gameGui = gameGui
        self._board = board
        self._players = players

        c = app.addCanvas("c")
        app.setCanvasWidth("c", 8 * GuiBoard.SQR_SIZE)
        app.setCanvasHeight("c", 8 * GuiBoard.SQR_SIZE)
        app.setCanvasBg("c", "#999")
        app.setCanvasRelief("c", "sunken")

        c.bind("<Button-1>", self.onBoardClicked)
#        c.bind("<Double-Button-1>", self.onBoardDoubleClicked)
#        c.bind("<B1-Motion>", self.onBoardDrag)
#        c.bind("<ButtonRelease-1>", self.onBoardReleased)
        c.bind("<Motion>", self.onBoardMotion)
        c.bind("<Leave>", self.onBoardLeave)

        self._canvas = c

        app.startFrame("stateIconsFrame", row=0, column=1)
        stateCanvas = app.addCanvas("stateCanvas")
        app.setCanvasWidth("stateCanvas", 36)
        app.setCanvasHeight("stateCanvas", 3*36)
        app.stopFrame()
        self._stateCanvas = stateCanvas

    def setPlayers(self, players):
        self._players = players

    def resetGame(self):
        for p in self._players:
            p.resetGame(self._board, self._app, self._gameGui)
        self.redraw()

        p = self.currentPlayer()
        if p != None: self.currentPlayer().enterTurn(self._performMove)

    def _performMove(self, move):
        p = self.currentPlayer()
        if p != None: self.currentPlayer().exitTurn()

        self._board.move(move)
        self.redraw()

        p = self.currentPlayer()
        if p != None: self.currentPlayer().enterTurn(self._performMove)

    def playerOfColor(self, color):
        if color==None: return None
        return self._players[color.index]

    def currentPlayer(self):
        curPlayerColor = self._board.nextPlayer
        return self.playerOfColor(curPlayerColor)

    def onBoardClicked(self, event):
        curPlayer = self.currentPlayer()
        if curPlayer != None:
            change = curPlayer.onBoardClickedOnTurn(event)
            if change:
                self.redraw()

    # def onBoardDoubleClicked(self, event):
    #     pass #print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))
    # def onBoardDrag(self, event):
    #     pass #print("onBoardDrag(%s; %s,%s)" % (event, event.x, event.y))

    # def onBoardDoubleClicked(self, event):
    #     self.onBoardClicked(event)
    #    pass #print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    # def onBoardDrag(self, event):
    #     pass #print("onBoardDrag(%d,%d)" % (event.x, event.y))
    # def onBoardReleased(self, event):
    #     pass #print("onBoardReleased(%d,%d)" % (event.x, event.y))
    def onBoardMotion(self, event):
        r = self._gameGui.setMouseOver(event)
        if r: self.redraw()
    def onBoardLeave(self, event):
        r = self._gameGui.setMouseOver(None)
        if r: self.redraw()

    def redraw(self):
        app = self._app
        c = self._canvas
        app.clearCanvas("c")

        self.updateIcon()
        self._gameGui.drawBoard()

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
