from player import ThreadedPlayer
from board import Board
import time
import random
import heapq
import math

class FlatMCPlayer(ThreadedPlayer):
    TIME_PER_MOVE = 2.5
    BATCH_SIZE = 10

    def __init__(self, color):
        ThreadedPlayer.__init__(self, color)

    def selectMove(self):
        t0 = time.time()
        deadline = t0 + FlatMCPlayer.TIME_PER_MOVE
        possibleMoves = self._board.possibleMoves()
        heap = [MoveEntry(m) for m in possibleMoves]
        heapq.heapify(heap) # Essentially a no-op when all priorities are identical.
        print("DB| FlatMC: number of moves: %d" % len(heap))
        self._heap = heap
        self._n = 0
        self._approxLog = 100

        while time.time() < deadline:
            for i in xrange(FlatMCPlayer.BATCH_SIZE):
                self.improveEvaluation()
            time.sleep(0) # Yield.
        print("Time's up - evaluations: %d" % self._n)
        print("Heap at end: %s" % (sorted(self._heap)))

        move = self.selectBestMoveFromHeap()
        self._heap = None
        return move

    def improveEvaluation(self):
        topItem = self._heap[0]
        topMove = topItem.move
        b = Board(cloneOf = self._board)
        # print("Investigating %s" % (topMove,))
        b.move(topMove)
        while b.nextPlayer != None:
            moves = b.possibleMoves()
            b.move(random.choice(moves))
        # print("=> Winner: %s" % (b.winner,))

        # Update variables:
        delta = 1 if b.winner == self.color else 0.5 if b.winner == None else 0
        self._n += 1
        topItem.addPlayResult(delta, self._approxLog)

        heapq.heapreplace(self._heap, topItem)

        # Update derived values:
        # (OBS - must be done after item replacement, as long as we use heapreplace())
        if self.timeToUpdateLog():
            self.updateLog()


    def timeToUpdateLog(self):
        return True # TODO: optimize - look at self._n
    def updateLog(self):
        self._approxLog = math.log(self._n)
        for item in self._heap:
            item.updateScore(self._approxLog)
        heapq.heapify(self._heap)

    def selectBestMoveFromHeap(self):
        print("DB| selectBestMoveFromHeap: heap-top=%s" % (self._heap[0],))
        topItem = self._heap[0]
        bestMove = topItem.move
        mostPlays = topItem.getPlays()
        for item in self._heap:
            plays = item.getPlays()
            if plays > mostPlays:
                bestMove = item.move
                mostPlays = plays
        print("DB| selectBestMoveFromHeap: bestMove=%s (%d)" % (bestMove, mostPlays))
        return bestMove

class MoveEntry:
    UNEXPLORED_SCORE = 1e9

    def __init__(self, move):
        self._score = MoveEntry.UNEXPLORED_SCORE
        self.move = move
        self._plays = 0
        self._wins = 0

    def getPlays(self): return self._plays

    def __lt__(self, other):
        return self._score > other._score # Reverse score comparison (to fit with heap order)
    
    def addPlayResult(self, delta, approxLog):
        self._plays += 1
        self._wins += delta
        self.updateScore(approxLog)
    
    def updateScore(self, approxLog):
        plays = self._plays
        wins = self._wins
        if plays==0:
            score = MoveEntry.UNEXPLORED_SCORE
        else:
            score = float(wins)/plays + math.sqrt(2*approxLog / plays)
        self._score = score


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
