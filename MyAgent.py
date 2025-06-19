from Game2048 import *

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0

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
            for a in actions:
                result = state.move(a)
                if not self.timeRemaining(): return
                v = self.minPlayer(result, depth - 1)
                if v is None: return
                if v > best:
                    best = v
                    bestMove = a
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
        best = -10000
        for a in actions:
            if not self.timeRemaining(): return None
            result = state.move(a)
            v = self.minPlayer(result, depth - 1)
            if v is None: return None
            if v > best:
                best = v
        return best

    def minPlayer(self, state, depth):
        self._nodeCount += 1
        self._childCount += 1
        if state.gameOver():
            return state.getScore()
        if depth == 0:
            return self.heuristic(state)
        self._parentCount += 1
        best = 1e6
        for (t,v) in state.possibleTiles():
            if not self.timeRemaining(): return None
            result = state.addTile(t,v)
            v = self.maxPlayer(result, depth - 1)
            if v is None: return None
            if v < best:
                best = v
        return best

    def heuristic(self, state):
        board = state._board

        emptycells = 0
        maxTile = 0
        cornerBonus = 0
        mergecells = 0
        combining = 0

        for i in range(16):
            if board[i] == 0:
                emptycells += 1
            if board[i] > maxTile:
                maxTile = board[i]

        if maxTile == board[0] or maxTile == board[3] or maxTile == board[12] or maxTile == board[15]:
            cornerBonus = 1

        for r in range(0, 16, 4):
            for c in range(3):
                tile1 = board[r + c]
                tile2 = board[r + c + 1]
                if tile1 == tile2 and tile1 != 0:
                    mergecells += 1
                if tile1 != 0 and tile2 != 0:
                    combining -= abs((2 ** tile1) - (2 ** tile2))

        for c in range(4):
            for r in range(3):
                tile1 = board[c + r * 4]
                tile2 = board[c + (r + 1) * 4]
                if tile1 == tile2 and tile1 != 0:
                    mergecells += 1
                if tile1 != 0 and tile2 != 0:
                    combining -= abs((2 ** tile1) - (2 ** tile2))

        totalScore =  emptycells *50 + maxTile *25 + cornerBonus *50 + mergecells*20 + combining*10


        return totalScore

    def moveOrder(self, state):
        return state.actions()

    def stats(self):
        print(f'Average depth: {self._depthCount/self._count:.2f}')
        print(f'Branching factor: {self._childCount / self._parentCount:.2f}')
