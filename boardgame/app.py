# -*- Encoding: utf-8 -*-
from appJar.appjar import gui
from board import Board, WHITE, BLACK
from guiboard import GuiBoard
from player import Player, HumanPlayer, RandomPlayer, SlowRandomPlayer
from flatmc_player import FlatMCPlayer
from mcts_player import MCTSPlayer

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

    app.addLabel("l1", "New Game")
    app.addButton("2 player", new2PGameAction)
    app.addButton("AI 'Random'", newRandomPlayerGameAction)
    app.addButton("AI 'SlowRandom'", newSlowRandomPlayerGameAction)
    app.addButton("AI 'FlatMC'", newFlatMCPlayerGameAction)
    app.addButton("AI 'MCTS'", newMCTSPlayerGameAction)
    app.addButton("AI vs AI 'MCTS'", newMCTSPlayer2GameAction)

    app.setPadding((0,5))
    app.addLabel("l2a", "") # Spacer
    #app.addHorizontalSeparator()
    app.setPadding((0,0))
    app.addLabel("l2", "Other Options")
    app.addButton("Quit", quitAction)
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    guiboard = GuiBoard(app, board, players)

    app.stopLabelFrame()

    return guiboard

def quitAction():
    app.stop()

def new2PGameAction(btn):
    setupBoard(HumanPlayer, HumanPlayer)
def newRandomPlayerGameAction(btn):
    setupBoard(HumanPlayer, RandomPlayer)
def newSlowRandomPlayerGameAction(btn):
    setupBoard(HumanPlayer, SlowRandomPlayer)
def newFlatMCPlayerGameAction(btn):
    setupBoard(HumanPlayer, FlatMCPlayer)
def newMCTSPlayerGameAction(btn):
    setupBoard(HumanPlayer, MCTSPlayer, args2={"time":2.0})
def newMCTSPlayer2GameAction(btn):
    setupBoard(MCTSPlayer, MCTSPlayer, args1={"time":2.0}, args2={"time":1.0})

def setupBoard(p1Class, p2Class, args1={}, args2={}):
    board.setup()
    p1 = p1Class(WHITE, **args1)
    p2 = p2Class(BLACK, **args2)
    guiBoard.setPlayers([p1, p2])
    guiBoard.resetGame()
