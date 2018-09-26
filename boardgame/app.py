# -*- Encoding: utf-8 -*-
from appJar.appjar import gui
from board import ChessBoard
from playercolor import WHITE, BLACK
from player import Player, HumanPlayer, RandomPlayer, SlowRandomPlayer
from flatmc_player import FlatMCPlayer
from mcts_player import MCTSPlayer

from guiboard import GuiBoard
from chessgui import ChessGui

from chromo import CDBoard
from chromogui import CDGui

class GameSpec:
    def __init__(self, name, boardCls, guiCls):
        self.name = name
        self.boardClass = boardCls
        self.guiClass = guiCls

PAWNS_ONLY_SPEC = GameSpec("Pawns-only Chess", ChessBoard, ChessGui)
CHROMODYNAMICS_SPEC = GameSpec("Chromodynamics", CDBoard, CDGui)

GAME_SPECS = [
    PAWNS_ONLY_SPEC,
    CHROMODYNAMICS_SPEC
]

app = None
board_ctor = None#ChessBoard
board = None
guiBoard = None
gameGui = None

def startApp():
    global app
    global board
    global guiBoard
    global gameGui

    app = gui("ChromoDynamics", "600x450")
    # selectPawnsOnlyAction()
    #board = board_ctor()
    #gameGui = ChessGui(app, "c", board)

    guiBoard = createMainWindow(app, [None, None])
    guiBoard.redraw()
    app.go()

def createMainWindow(app, players):
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

    app.addLabel("l2", "Games")
    for g in GAME_SPECS:
        action = lambda btnLabel, game=g: selectGame(game)
        app.addButton(g.name, action)
        
    app.setPadding((0,5))
    app.addLabel("l3a", "") # Spacer
    app.setPadding((0,0))

    app.addLabel("l3", "Other Options")
    app.addButton("Quit", quitAction)
    app.stopFrame()

    app.startLabelFrame("Board", row=0, column=1)
    app.setSticky("")

    selectGame(PAWNS_ONLY_SPEC)
    print "createMainWindow: board=%r" % (board,)
    guiboard = GuiBoard(app, gameGui, board, players)

    app.stopLabelFrame()

    return guiboard

def quitAction():
    app.stop()

def selectGame(spec):
    print "selectGame: %r" % (spec,)
    new_board_ctor = spec.boardClass
    new_gui_ctor =  spec.guiClass
    
    global board, board_ctor, gameGui
    if board_ctor == new_board_ctor:
        return
    board_ctor = new_board_ctor
    board = board_ctor()
    gameGui = new_gui_ctor(app, "c", board)
    if guiBoard != None:
        guiBoard.setGame(gameGui, board)
        guiBoard.redraw()

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
