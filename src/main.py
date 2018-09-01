#!/usr/bin/env python
from appJar.appjar import gui

app = None
def main():
    global app
    app = gui("ChromoDynamics", "600x450")
    board = createMainWindow(app)
    board.redraw()
    app.go()

def createMainWindow(app):
    app.startFrame("MENU", row=0, column=0)
    app.setBg("#ddd")
    app.setSticky("NEW")
    app.setStretch("COLUMN")

    app.addLabel("l1", "<menu>")
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    board = GuiBoard(app)

    app.stopLabelFrame()

    return board

class GuiBoard:
    SQR_SIZE = 48

    def __init__(self, app):
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

        self._app = app
        self._canvas = c

        self._mouseOver = None

    def onBoardClicked(self, event):
        print("onBoardClicked(%s; %s,%s)" % (event, event.x, event.y))
        # (x,y) = (event.x, event.y)
        # bx = int(x / GuiBoard.SQR_SIZE)
        # by = int(y / GuiBoard.SQR_SIZE)

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
        return (bx,by)

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
        dark_pawn_img = "../gfx/black-pawn.png"
        light_pawn_img = "../gfx/white-pawn.png"
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
                img = dark_pawn_img if y==1 else light_pawn_img if y==6 else None
                if img==None: continue
                app.addCanvasImage("c", x*size, y*size,
                                   img, anchor="nw")

        if self._mouseOver != None:
            (mx, my) = self._mouseOver
            color = "#090"
            app.addCanvasRectangle("c", mx*size, my*size, size, size,
                                   width=2, outline=color, fill=None)



main()
