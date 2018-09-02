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

WHITE = Color("white", 1)
BLACK = Color("black", -1)

class Board:
    def __init__(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]
        self.turnNr = 0
        self._moves = None

    def get(self, x, y):
        return self.board[y][x]

    def move(self, m):
        (x1,y1) = m.src
        (x2, y2) = m.dst
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None
        self.turnNr += 1
        self._moves = None

    def setup(self):
        self.board = [[None for x in xrange(8)] for y in xrange(8)]
        for x in xrange(8):
            self.board[1][x] = WHITE
            self.board[6][x] = BLACK

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
                if p == None:
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
        pos = self.eventSquare(event)
        piece = self._board.get(pos[0],pos[1])
        if self._from == None:
            # Select
            if piece != None:
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
            if self._from != None and Move(self._from, self._mouseOver) in self._board.possibleMoves():
                color = "#ee0" # Possible move
            app.addCanvasRectangle("c", mx*size, my*size, size, size,
                                   width=2, outline=color, fill=None)



main()
