from player import ThreadedPlayer
from board import Board
import time
import random
import heapq
import math

class Context:
    def __init__(self):
        # Policy:
        self.exploration = 2
        self.rave_threshold = 10
        # Move-local state:
        self.statsForMove = dict() # dict: move=>(enum,denom)

    def updateStatsForMove(self, move, value, weight):
        # TODO: Ought to include color as index & parameter.
        if weight==0:
            return
        oldFraction = self.statsForMove.get(move, None)
        if oldFraction==None:
            (a,b) = (0,0)
        else:
            (a,b) = oldFraction
        a += float(value)*weight
        b += weight
        self.statsForMove[move] = (a,b)
        
    def heuristicValueForMove(self, move):
        fraction = self.statsForMove.get(move, None)
        if fraction==None:
            return 0.95 # A move to be investigated
        else:
            (a,b) = fraction
            return a/b

class MCTSPlayer(ThreadedPlayer):
    TIME_PER_MOVE = 2.5
    LOW_EXPLORATION_TIME = 1.0
    BATCH_SIZE = 10

    def __init__(self, color, time=TIME_PER_MOVE):
        ThreadedPlayer.__init__(self, color)
        self.time_per_move = time
        # TODO: Retain state (relevant part of the tree) between moves.

    def selectMove(self):
        t0 = time.time()
        deadline = t0 + self.time_per_move

        ctx = Context()
        root = TreeNode(self._board, None, ctx)

        while time.time() < deadline:
            # if time.time() > deadline - MCTSPlayer.LOW_EXPLORATION_TIME:
            #     ctx.exploration = 0.1
            print("DB| Round with exploration=%f" % (ctx.exploration,))
            for i in xrange(MCTSPlayer.BATCH_SIZE):
                self.improveEvaluation(root, ctx)
            if root.canStopEarly():
                print "STOPPING EARLY"
                break
            time.sleep(0) # Yield.
            #break # TEST
        #print("Time's up - evaluations: %d" % self._n)
        #print("Heap at end: %s" % (sorted(self._heap)))

        print "State along best line:"
        n = root
        while n != None:
            entry = n.selectBestFinalEntry()
            print "== Chosen: %s ==" % (entry.move)
            childNode = entry.getTreeNode()
            if childNode==None: break
            print "Heap: %s" %  (sorted(childNode._heap))
            n = childNode
        print "===="
        
        move = root.selectBestFinalEntry().move
        print("Heap at end: %s" % (sorted(root._heap)))

        spent = time.time() - t0
        print "SPENT: %.3fs on %s" % (spent,move)
        return move

    def improveEvaluation(self, root, ctx):
        # Descend the tree:
        node = root
        b = Board(cloneOf = self._board)
        line = ""
        while True:
            entry = node.selectPromisingMove()
            childNode = entry.getTreeNode()
            b.move(entry.move)
            line += "%s(%d) " % (entry.move, entry._plays)
            if b.nextPlayer==None: # Leaf node
                break
            if childNode == None:
                #print "DB| Creating node at turn %d with color %s" % (b.turnNr, b.nextPlayer.name)
                node = entry.createTreeNode(b, node, ctx)
                break
            node = childNode
        print "Expanding line: %s" % (line,)

        # Playout/determine value:
        playoutMoves = None
        if b.nextPlayer==None:
            playoutWinner = b.winner
        else:
#            (playoutWinner, playoutMoves) = self.playout(b)
            (playoutWinner, playoutMoves) = self.playoutUsingHeuristics(b, ctx)
        if playoutWinner==None:
            playoutValue = 0.5
        else:
            playoutValue = (playoutWinner.weight() + 1) / 2 # (-1..1) -> (0..1)

        # Update global move stats:
        if playoutMoves != None:
            updateWeight = 1
            for m in playoutMoves:
                ctx.updateStatsForMove(m, playoutValue, updateWeight)
                updateWeight *= 0.99 # Decay reward.

        # Propagate change:
        while node!=None:
            node.addPlayoutResult(playoutValue, ctx)
            node = node.parent

    def playout(self, board):
        moveSeq = []
        while board.nextPlayer != None:
            possibleMoves = board.possibleMoves()
            move = random.choice(possibleMoves)
            board.move(move)
            moveSeq.append(move)
        # print("=> Winner: %s" % (b.winner,))
        return (board.winner, moveSeq)

    def playoutUsingHeuristics(self, board, ctx):
        N = 3 # How many moves to look at
        moveSeq = []
        while board.nextPlayer != None:
            possibleMoves = board.possibleMoves()
            move = random.choice(possibleMoves)
            bestHV = ctx.heuristicValueForMove(move)
            sign = board.nextPlayer.weight()
            for i in xrange(N-1):
                altMove = random.choice(possibleMoves)
                altHV = ctx.heuristicValueForMove(altMove)
                if sign*(altHV - bestHV) > 0:
                    #print("DB| playout: changing %s to %s (%.3f vs %.3f)" % (move, altMove, bestHV, altHV))
                    move = altMove
                    bestHV = altHV
            board.move(move)
            moveSeq.append(move)
        # print("=> Winner: %s" % (b.winner,))
        return (board.winner, moveSeq)

class TreeNode:
    def __init__(self, board, parent, ctx):
        self.parent = parent
        self.color = board.nextPlayer
        
        possibleMoves = board.possibleMoves()
        heap = [MoveEntry(m, ctx) for m in possibleMoves]
        heapq.heapify(heap) # Essentially a no-op when all priorities are identical.
        #print("DB| MCTS.TreeNode: number of moves: %d" % len(heap))
        self._heap = heap
        self._n = 0
        self._approxLog = 100

    def timeToUpdateLog(self):
        return True # TODO: optimize - look at self._n
    def updateLog(self, ctx):
        self._approxLog = math.log(self._n)
        for item in self._heap:
            item.updateScore(self._approxLog, self.color.weight(), ctx)
        heapq.heapify(self._heap)

    def canStopEarly(self):
        if len(self._heap)<2: return True # Forced move
        # top = self._heap[0]
        # ru1 = self._heap[1]
        # ru2 = self._heap[2]
        # if top._plays>10 and top._plays > 2*ru1._plays and top._plays > 2*ru2._plays:
        #     return True # TEST CRITERION
        return False

    def addPlayoutResult(self, value, ctx):
        # Update variables:
        self._n += 1
        topItem = self._heap[0]
        topItem.addPlayResult(value, self._approxLog, self.color.weight(), ctx)
        heapq.heapreplace(self._heap, topItem)

        # Update derived values:
        # (OBS - must be done after item replacement, as long as we use heapreplace())
        if self.timeToUpdateLog():
            self.updateLog(ctx)

        # Returns (move, childNode)
    def selectPromisingMove(self):
        topItem = self._heap[0]
        return topItem

    def selectBestFinalEntry(self):
        topEntry = self._heap[0]
        bestMove = topEntry.move
        bestEntry = topEntry
        mostPlays = topEntry.getPlays()
        for entry in self._heap:
            plays = entry.getPlays()
            if plays > mostPlays:
                bestMove = entry.move
                bestEntry = entry
                mostPlays = plays
        print("DB| selectBestMoveFromHeap: bestMove=%s (%d)" % (bestMove, mostPlays))
        print("DB| selectBestMoveFromHeap: bestEntry=%s" % (bestEntry,))
        return bestEntry

        
    
class MoveEntry:
    UNEXPLORED_SCORE = 1e6

    def __init__(self, move, ctx):
        self._score = MoveEntry.UNEXPLORED_SCORE
        self.move = move
        self._plays = 0
        self._wins = 0
        self._treeNode = None
        
        self._heuristicValue = ctx.heuristicValueForMove(move)

    def getPlays(self): return self._plays

    def __lt__(self, other):
        #print "MoveEntry.lt: %s vs %s" % (self._score, other._score)
        return self._score > other._score # Reverse score comparison (to fit with heap order)
    
    def addPlayResult(self, delta, approxLog, sign, ctx):
        self._plays += 1
        self._wins += delta
        self.updateScore(approxLog, sign, ctx)
    
    def updateScore(self, approxLog, sign, ctx):
        plays = self._plays
        wins = self._wins
        if plays==0:
            score = 0
            spread = MoveEntry.UNEXPLORED_SCORE
        else:
            exploration = ctx.exploration
            spread = math.sqrt(exploration*approxLog / plays)
            score = float(wins)/plays
            
        if plays < ctx.rave_threshold:
            alpha = plays / float(ctx.rave_threshold)
            score = alpha*score + (1-alpha)*self._heuristicValue
        score = sign*score + spread
                
        self._score = score

    def getTreeNode(self):
        return self._treeNode
    
    def createTreeNode(self, board, parent, ctx):
        self._treeNode = TreeNode(board, parent, ctx)
        return self._treeNode


    def __repr__(self):
        return self.__str__()
    def __str__(self):
        plays = self._plays
        wins = self._wins
        return "MoveE(%s, %s/%s=%.3f, heu=%.3f, score=%.3f)" % (
            self.move,
            wins,
            plays,
            0.5 if plays==0 else float(wins)/plays,
            self._heuristicValue,
            self._score)
