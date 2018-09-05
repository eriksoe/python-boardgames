from appJar.appjar import gui
from board import Board
from guiboard import GuiBoard

app = None
board = None
guiBoard = None

def startApp():
    global app
    global board
    global guiBoard

    app = gui("ChromoDynamics", "600x450")
    board = Board()
    #board.setup()
    guiBoard = createMainWindow(app, board)
    guiBoard.redraw()
    app.go()

def createMainWindow(app, board):
    app.startFrame("MENU", row=0, column=0)
    app.setBg("#ddd")
    app.setSticky("NEW")
    app.setStretch("COLUMN")

    app.addLabel("l1", "Menu")
    app.addButton("New game", newGameAction)
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    guiboard = GuiBoard(app, board)

    app.stopLabelFrame()

    return guiboard

def newGameAction(btn):
    board.setup()
    guiBoard.redraw()
