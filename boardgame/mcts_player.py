from player import ThreadedPlayer
from board import Board
import time
import random
import heapq
import math

class MCTSPlayer(ThreadedPlayer):
    TIME_PER_MOVE = 2.5
    BATCH_SIZE = 10

    def __init__(self, color):
        ThreadedPlayer.__init__(self, color)
        # TODO: Retain state (relevant part of the tree) between moves.

    def selectMove(self):
        t0 = time.time()
        deadline = t0 + MCTSPlayer.TIME_PER_MOVE

        root = TreeNode(self._board, None)

        while time.time() < deadline:
            for i in xrange(MCTSPlayer.BATCH_SIZE):
                self.improveEvaluation(root)
            time.sleep(0) # Yield.
            #break # TEST
        #print("Time's up - evaluations: %d" % self._n)
        #print("Heap at end: %s" % (sorted(self._heap)))

        move = root.selectBestFinalMove()
        print("Heap at end: %s" % (sorted(root._heap)))
        return move

    def improveEvaluation(self, root):
        # Descend the tree:
        node = root
        b = Board(cloneOf = self._board)
        while True:
            entry = node.selectPromisingMove()
            childNode = entry.getTreeNode()
            b.move(entry.move)
            if b.nextPlayer==None: # Leaf node
                break
            if childNode == None:
                #print "DB| Creating node at turn %d with color %s" % (b.turnNr, b.nextPlayer.name)
                node = entry.createTreeNode(b, node)
                break
            node = childNode

        # Playout/determine value:
        if b.nextPlayer==None:
            playoutWinner = b.winner
        else:
            playoutWinner = self.playout(b)
        if playoutWinner==None:
            playoutValue = 0.5
        else:
            playoutValue = (playoutWinner.weight() + 1) / 2 # (-1..1) -> (0..1)

        # Propagate change:
        while node!=None:
            node.addPlayoutResult(playoutValue)
            node = node.parent

    def playout(self, board):
        while board.nextPlayer != None:
            moves = board.possibleMoves()
            board.move(random.choice(moves))
        # print("=> Winner: %s" % (b.winner,))
        return board.winner
            
    def improveEvaluation_OLD(self):
        topItem = self._heap[0]
        topMove = topItem.move
        b = Board(cloneOf = self._board)
        # print("Investigating %s" % (topMove,))
        b.move(topMove)
        while b.nextPlayer != None:
            moves = b.possibleMoves()
            b.move(random.choice(moves))
        # print("=> Winner: %s" % (b.winner,))

class TreeNode:
    def __init__(self, board, parent):
        self.parent = parent
        self.color = board.nextPlayer
        
        possibleMoves = board.possibleMoves()
        heap = [MoveEntry(m) for m in possibleMoves]
        heapq.heapify(heap) # Essentially a no-op when all priorities are identical.
        #print("DB| MCTS.TreeNode: number of moves: %d" % len(heap))
        self._heap = heap
        self._n = 0
        self._approxLog = 100

    def timeToUpdateLog(self):
        return True # TODO: optimize - look at self._n
    def updateLog(self):
        self._approxLog = math.log(self._n)
        for item in self._heap:
            item.updateScore(self._approxLog, self.color.weight())
        heapq.heapify(self._heap)

    def addPlayoutResult(self, value):
        # Update variables:
        self._n += 1
        topItem = self._heap[0]
        topItem.addPlayResult(value, self._approxLog, self.color.weight())
        heapq.heapreplace(self._heap, topItem)

        # Update derived values:
        # (OBS - must be done after item replacement, as long as we use heapreplace())
        if self.timeToUpdateLog():
            self.updateLog()

        # Returns (move, childNode)
    def selectPromisingMove(self):
        topItem = self._heap[0]
        return topItem

    def selectBestFinalMove(self):
        topItem = self._heap[0]
        bestMove = topItem.move
        bestItem = topItem
        mostPlays = topItem.getPlays()
        for item in self._heap:
            plays = item.getPlays()
            if plays > mostPlays:
                bestMove = item.move
                bestItem = item
                mostPlays = plays
        print("DB| selectBestMoveFromHeap: bestMove=%s (%d)" % (bestMove, mostPlays))
        print("DB| selectBestMoveFromHeap: bestItem=%s" % (bestItem,))
        return bestMove

        
    
class MoveEntry:
    UNEXPLORED_SCORE = -1e9

    def __init__(self, move):
        self._score = MoveEntry.UNEXPLORED_SCORE
        self.move = move
        self._plays = 0
        self._wins = 0
        self._treeNode = None

    def getPlays(self): return self._plays

    def __lt__(self, other):
        #print "MoveEntry.lt: %s vs %s" % (self._score, other._score)
        return self._score < other._score # Reverse score comparison (to fit with heap order)
    
    def addPlayResult(self, delta, approxLog, sign):
        self._plays += 1
        self._wins += delta
        self.updateScore(approxLog, sign)
    
    def updateScore(self, approxLog, sign):
        plays = self._plays
        wins = self._wins
        if plays==0:
            score = MoveEntry.UNEXPLORED_SCORE
        else:
            score = -(sign*float(wins)/plays + math.sqrt(2*approxLog / plays))
        self._score = score

    def getTreeNode(self):
        return self._treeNode
    
    def createTreeNode(self, board, parent):
        self._treeNode = TreeNode(board, parent)
        return self._treeNode


    def __repr__(self):
        return self.__str__()
    def __str__(self):
        plays = self._plays
        wins = self._wins
        return "MoveE(%s, %s/%s=%.3f, UCB=%.3f)" % (self.move,
                                                  wins,
                                                  plays,
                                                  0.5 if plays==0 else float(wins)/plays,
                                                  self._score)
