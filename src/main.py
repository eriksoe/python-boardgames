#!/usr/bin/env python
from appJar.appjar import gui

SQR_SIZE = 40

app = None
def main():
    global app
    app = gui("ChromoDynamics", "600x400")
    createMainWindow(app)
    drawBoard(app)
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

    c = app.addCanvas("c")
    app.setCanvasWidth("c", 320)
    app.setCanvasHeight("c", 320)
    app.setCanvasBg("c", "#999")
    app.setCanvasRelief("c", "sunken")
    #app.setCanvasInPadding("c", (2,5))
    #app.setCanvasPadding("c", (4,10))
    #app.setCanvasEvent("c", item, event, function, add=None)
    c.bind("<Button-1>", onBoardClicked)
    c.bind("<Double-Button-1>", onBoardDoubleClicked)
    c.bind("<B1-Motion>", onBoardDrag)
    c.bind("<ButtonRelease-1>", onBoardReleased)
    c.bind("<Motion>", onBoardMotion)

    app.stopLabelFrame()

    return c

def drawBoard(app):
    c = app.getCanvas("c")
    app.clearCanvas("c")

    for y in xrange(8):
        for x in xrange(8):
            parity = ((x+y) & 1) > 0
            color = "#f99" if parity else "#99f"
            app.addCanvasRectangle("c", x*SQR_SIZE, y*SQR_SIZE, SQR_SIZE, SQR_SIZE,
                                   width=0, fill=color)


def onBoardClicked(event):
    print("onBoardClicked(%s; %s,%s)" % (event, event.x, event.y))
    (x,y) = (event.x, event.y)
    bx = int(x / SQR_SIZE)
    by = int(y / SQR_SIZE)
    print("Square clicked: %d,%d" % (bx,by))

def onBoardDoubleClicked(event):
    print("onBoardDoubleClicked(%d,%d)" % (event.x, event.y))
def onBoardDrag(event):
    print("onBoardDrag(%d,%d)" % (event.x, event.y))
def onBoardReleased(event):
    print("onBoardReleased(%d,%d)" % (event.x, event.y))
def onBoardMotion(event):
    print("onBoardMotion(%d,%d)" % (event.x, event.y))


main()
