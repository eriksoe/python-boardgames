#!/usr/bin/env python
from appJar.appjar import gui

def main():
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
    app.setCanvasDragFunction("c", (onStartDrag, onStopDrag))

    app.stopLabelFrame()

    return c

def drawBoard(app):
    c = app.getCanvas("c")
    app.clearCanvas("c")
    size = 40
    c.create_line(0,0, 8*size, 8*size)

    for y in xrange(8):
        for x in xrange(8):
            parity = ((x+y) & 1) > 0
            color = "#f99" if parity else "#99f"
            # app.addCanvasRectangle("c", x*size, y*size, size, size,
            #                        width=0, fill=color)


def onStartDrag(event):
    print("onStartDrag(%s)" % (event,))
def onStopDrag(event):
    print("onStop(%s)" % (event,))

main()
