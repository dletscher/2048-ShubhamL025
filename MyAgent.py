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

        def heuristic(self, state):
            board = state._board
            empty = board.count(0)
            maxTile = max(board)
            maxInCorner = 1 if maxTile in [board[0], board[3], board[12], board[15]] else 0
#Checking for monotonocity in the game.
            def monotonousrnc(board):
                totals = [0, 0, 0, 0]
                for i in range(4):
                    for j in range(3):
                        a = board[i*4 + j]
                        b = board[i*4 + j + 1]
                        if a > b:
                            totals[0] +=a - b
                        else:
                            totals[1] +=b - a
                for j in range(4):
                    for i in range(3):
                        a = board[i*4 + j]
                        b = board[(i+1)*4 + j]
                        if a >b:
                            totals[2] += a - b
                        else:
                            totals[3] +=b - a
                return -min(totals[0], totals[1]) - min(totals[2], totals[3])
#this section check the smoothnedd of movesin board.
            def smoothrnc(board):
                smooth =0
                for i in range(4):
                    for j in range(4):
                        rnc = i*4 + j
                        if board[rnc] == 0:
                            continue
                        if j < 3 and board[rnc+1] != 0:
                            smooth -= abs(board[rnc] - board[rnc+1])
                        if i < 3 and board[rnc+4] != 0:
                            smooth -= abs(board[rnc] - board[rnc+4])
                return smooth

            blockweight = [65536, 32768,16384, 8192,512, 1024, 2048,4096,256, 128, 64, 32,2, 4, 8,16]
            blockweightScore = sum(board[i]*blockweight[i] for i in range(16))

            center_penalty = sum(-board[i]*2 for i in [5, 6, 9, 10] if board[i] >= maxTile - 2)
            if maxInCorner==0:
                return -5000
            maxone = board.index(maxTile)

#Giving a penalty for blocking the tiles.
            tileblocker = []
            if maxone == 0:
                tileblocker = [1, 4]
            elif maxone == 3:
                tileblocker = [2,7]
            elif maxone == 12:
                tileblocker = [8, 13]
            elif maxone ==15:
                tileblocker = [11, 14]
            avoidmove = 0
            for n in tileblocker:
                if board[n] != 0 and board[n] != board[maxone]:
                    avoidmove -=7000
            finalscore = empty * 500+ monotonousrnc(board) *200+ smoothrnc(board) * 200+ center_penalty+ blockweightScore * 10+ avoidmove
            return (finalscore)

        def moveOrder(self, state):
            board = state._board
            maxTile = max(board)
            maxone = board.index(maxTile)
            if maxone == 0:
                movingrule = ['U', 'L', 'R', 'D']
            elif maxone in [1, 2, 3]:
                movingrule = ['L', 'U', 'R', 'D']
            elif maxone in [4, 8, 12]:
                movingrule =['U', 'L', 'D', 'R']
            else:
                movingrule = ['U', 'L', 'R', 'D']
            actions = list(state.actions())
            return [move for move in movingrule if move in actions]

        def stats(self):
            print(f'Average depth: {self._depthCount/self._count:.2f}')
            print(f'Branching factor: {self._childCount / self._parentCount:.2f}')
