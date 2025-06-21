from Game2048 import *

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0
#Expectimac used.
    def findMove(self, state):
        self._count += 1
        actions = self.moveOrder(state)
        depth = 1
        while self.timeRemaining():
            self._depthCount += 1
            self._parentCount += 1
            self._nodeCount += 1
            print('Search depth', depth)
            best = -10000
            bestMove = None 
            for a in actions:
                result = state.move(a)
                if not self.timeRemaining(): return
                v = self.minPlayer(result, depth - 1)
                if v is None: return
                if v > best:
                    best = v
                    bestMove = a
            if bestMove is None and actions:
                bestMove = actions[0]
            self.setMove(bestMove)
            print('\tBest value', best, bestMove)
            depth += 1

    def maxPlayer(self, state, depth):
        self._nodeCount += 1
        self._childCount += 1
        if state.gameOver():
            return state.getScore()
        actions = self.moveOrder(state)
        if depth == 0:
            return self.heuristic(state)
        self._parentCount += 1
        value = float('-inf')
        for a in actions:
            if not self.timeRemaining(): return None
            result = state.move(a)
            v = self.minPlayer(result, depth - 1)
            if v is None:
                continue
            if v >value:
                value = v
        return value

    def minPlayer(self, state, depth):
        self._nodeCount += 1
        self._childCount += 1
        if state.gameOver():
            return state.getScore()
        if depth ==0:
            return self.heuristic(state)
        self._parentCount += 1
        total =0
        count =0
        for (t, v) in state.possibleTiles():
            if not self.timeRemaining(): return None
            result = state.addTile(t, v)
            prob = 0.9 if v == 1 else 0.1
            val = self.maxPlayer(result, depth - 1)
            if val is None:
                continue
            total += prob * val
            count +=1
        if count == 0:
            return self.heuristic(state)
        return total / count
#with empty cell heuristic.
    def heuristic(self, state):
        board = state._board
        empty = board.count(0)
        return state.getScore() + empty * 1000
		
    def moveOrder(self, state):
	    return state.actions()

    def stats(self):
        print(f'Average depth: {self._depthCount/self._count:.2f}')
        print(f'Branching factor: {self._childCount / self._parentCount:.2f}')
