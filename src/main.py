#!/usr/bin/env python
from appJar.appjar import gui

app = None
def main():
    global app
    app = gui("ChromoDynamics", "600x450")
    board = Board()
    board.setup()
    guiboard = createMainWindow(app, board)
    guiboard.redraw()
    app.go()

def createMainWindow(app, board):
    app.startFrame("MENU", row=0, column=0)
    app.setBg("#ddd")
    app.setSticky("NEW")
    app.setStretch("COLUMN")

    app.addLabel("l1", "<menu>")
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    guiboard = GuiBoard(app, board)

    app.stopLabelFrame()

    return guiboard

class Color:
    def __init__(self, name):
        self.name = name

    def pawn_img(self):
        return "../gfx/%s-pawn.png" % (self.name,)

WHITE = Color("white")
BLACK = Color("black")

class Board:
    def __init__(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]

    def get(self, x, y):
        return self.board[y][x]

    def move(self, pos1, pos2):
        (x1,y1) = pos1
        (x2, y2) = pos2
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None

    def setup(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]
        for x in xrange(8):
            self.board[1][x] = WHITE
            self.board[6][x] = BLACK

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

        self._mouseOver = None
        self._from = None

    def onBoardClicked(self, event):
        print("onBoardClicked(%s; %s,%s)" % (event, event.x, event.y))
        pos = self.eventSquare(event)
        if self._from == None:
            if self._board.get(pos[0],pos[1]) != None:
                self._from = pos
                self.redraw()
        else:
            self._board.move(self._from, pos)
            self._from = None
            self.redraw()

    def onBoardDoubleClicked(self, event):
        print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    def onBoardDrag(self, event):
        print("onBoardDrag(%s; %s,%s)" % (event, event.x, event.y))

    def onBoardDoubleClicked(self, event):
        print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    def onBoardDrag(self, event):
        print("onBoardDrag(%s; %s,%s)" % (event, event.x, event.y))

    def onBoardDoubleClicked(self, event):
        print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))

    def onBoardDrag(self, event):
        print("onBoardDrag(%d,%d)" % (event.x, event.y))
    def onBoardReleased(self, event):
        print("onBoardReleased(%d,%d)" % (event.x, event.y))
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
        size = GuiBoard.SQR_SIZE
        app = self._app
        c = self._canvas
        app.clearCanvas("c")

        dark_img = "../gfx/dark-square.png"
        light_img = "../gfx/light-square.png"
        #black_pawn_img = "../gfx/black-pawn.png"
        #white_pawn_img = "../gfx/white-pawn.png"
        for y in xrange(8):
            for x in xrange(8):
                parity = ((x+y) & 1) > 0
                color = "#f99" if parity else "#99f"
                img = dark_img if parity else light_img
                # app.addCanvasRectangle("c", x*size, y*size, size, size,
                #                        width=0, fill=color)
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

        for y in xrange(8):
            for x in xrange(8):
                b = self._board.get(x, 7-y)
                if b==None: continue
                img = b.pawn_img()
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

        if self._from != None:
            (mx, my) = self._from
            my = 7-my
            color = "#ee0"
            app.addCanvasRectangle("c", mx*size, my*size, size, size,
                                   width=3, outline=color, fill=None)
        if self._mouseOver != None:
            (mx, my) = self._mouseOver
            my = 7-my
            color = "#090"
            app.addCanvasRectangle("c", mx*size, my*size, size, size,
                                   width=2, outline=color, fill=None)



main()
