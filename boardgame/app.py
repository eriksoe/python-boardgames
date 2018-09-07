from appJar.appjar import gui
from board import Board, WHITE, BLACK
from guiboard import GuiBoard
from player import Player, HumanPlayer

app = None
board = None
guiBoard = None

def startApp():
    global app
    global board
    global guiBoard

    app = gui("ChromoDynamics", "600x450")
    board = Board()

    guiBoard = createMainWindow(app, board, [None, None])
    guiBoard.redraw()
    app.go()

def createMainWindow(app, board, players):
    app.startFrame("MENU", row=0, column=0)
    app.setBg("#ddd")
    app.setSticky("NEW")
    app.setStretch("COLUMN")

    app.addLabel("l1", "Menu")
    app.addButton("New game", newGameAction)
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    guiboard = GuiBoard(app, board, players)

    app.stopLabelFrame()

    return guiboard

def newGameAction(btn):
    board.setup()
    p1 = HumanPlayer(WHITE)
    p2 = HumanPlayer(BLACK)
    guiBoard.setPlayers([p1, p2])
    guiBoard.resetGame()
