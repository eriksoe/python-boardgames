from player import ThreadedPlayer
from board import Board
import time
import random
import heapq
import math

UNEXPLORED_SCORE = -1e9

class FlatMCPlayer(ThreadedPlayer):
    TIME_PER_MOVE = 2.5
    BATCH_SIZE = 10

    def __init__(self, color):
        ThreadedPlayer.__init__(self, color)

    def selectMove(self):
        t0 = time.time()
        deadline = t0 + FlatMCPlayer.TIME_PER_MOVE
        possibleMoves = self._board.possibleMoves()
        heap = [(UNEXPLORED_SCORE, m, 0, 0) for m in possibleMoves]
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
        (oldScore, topMove, plays, wins) = topItem
        b = Board(cloneOf = self._board)
        # print("Investigating %s" % (topMove,))
        b.move(topMove)
        while b.nextPlayer != None:
            moves = b.possibleMoves()
            b.move(random.choice(moves))
        # print("=> Winner: %s" % (b.winner,))

        # Update variables:
        delta = 1 if b.winner == self.color else 0.5 if b.winner == None else 0
        plays += 1
        wins += delta
        self._n += 1

        topItem = self.scoredTuple(topMove, plays, wins)
        heapq.heapreplace(self._heap, topItem)
        # print("Investigated %s: %.3f -> %.3f" % (topMove, oldScore, topItem[0]))
        # Update derived values:
        # (OBS - must be done after item replacement, as long as we use heapreplace())
        if self.timeToUpdateLog():
            self.updateLog()


    def timeToUpdateLog(self):
        return True # TODO: optimize - look at self._n
    def updateLog(self):
        self._approxLog = math.log(self._n)
        newHeap = [self.scoredTuple(move, plays, wins)
                   for (oldScore, move, plays, wins) in self._heap]
        heapq.heapify(newHeap)
        self._heap = newHeap

    def scoredTuple(self, move, plays, wins):
        # Because of heap order, better score must be more negative
        if plays==0:
            score = UNEXPLORED_SCORE
        else:
            score = -(float(wins)/plays + math.sqrt(2*self._approxLog / plays))
        return (score, move, plays, wins)

    def selectBestMoveFromHeap(self):
        print("DB| selectBestMoveFromHeap: heap-top=%s" % (self._heap[0],))
        #(score, move, _, _) = self._heap[0]
        (_, bestMove, mostPlays, _) = self._heap[0]
        for item in self._heap:
            (_, move, plays, _) = item
            if plays > mostPlays:
                bestMove = move
                mostPlays = plays
        print("DB| selectBestMoveFromHeap: bestMove=%s (%d)" % (bestMove, mostPlays))
        return bestMove
