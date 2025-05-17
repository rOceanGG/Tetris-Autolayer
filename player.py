from board import Direction, Rotation, Action, Shape
from random import Random

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class RoshansPlayer(Player):
    sequence = []

    def __init__(self, seed = None):
        self.random = Random(seed)

    def addMoveToSequence(self, leMove):
        self.sequence.append(leMove)
        return True

    def moveToTarget(self, board, i, j):
        self.sequence.clear()
        newBoard = board.clone()
        for x in range(i):
            if self.addMoveToSequence(Rotation.Clockwise) and newBoard.rotate(Rotation.Clockwise):
                return newBoard
        if newBoard.falling.left < j:
            while newBoard.falling.left != j:
                if self.addMoveToSequence(Direction.Right) and newBoard.move(Direction.Right):
                    self.sequence.append(Direction.Right)
                    return newBoard  
            newBoard.move(Direction.Drop)
            self.sequence.append(Direction.Drop)
            return newBoard

        elif newBoard.falling.left > j:
            while newBoard.falling.left != j:
                if self.addMoveToSequence(Direction.Left) and newBoard.move(Direction.Left):
                    self.sequence.append(Direction.Left)
                    return newBoard
        else:
            newBoard.move(Direction.Drop)
            self.sequence.append(Direction.Drop)
            return newBoard
        newBoard.move(Direction.Drop)
        return newBoard 

    def boardsHighest(self, board):
        try:
            return min(y for (x, y) in board.cells)  
        except:
            return 23
        
    def findHighestPoint(self, board, index):
        currentHighest = 24
        for (x, y) in board.cells:
            if x == index and y < currentHighest:
                currentHighest = y  
        return currentHighest
    
    def bumpiness(self, board):
        bumpiness = 0
        for i in range(0, 9, 1):
            firstMax = self.findHighestPoint(board, i)
            secondMax = self.findHighestPoint(board, i+1)
            bump = abs(firstMax - secondMax)
            bumpiness += bump
        return bumpiness
    
    def holes(self, board):
        numHoles = 0
        for (x, y) in board.cells:
            j = y+1
            while (x, j) not in board.cells and j < 24:
                numHoles += 1
                j += 1
        return numHoles
    
    def findHoles(self, board):
        holePos = []
        for(x, y) in board.cells:
            j = y+1
            while (x, j) not in board.cells and j < 24:
                holePos.append((x, j))
                j+=1
        return holePos
    
    def lowestHoles(self, board):
        holePos = self.findHoles(board)
        try:
            return min(y for (x, y) in holePos)
        except:
            return 19
        
    def score_board(self, board):
        cellSet = board.cells.copy()
        allY = 0
        blocks = 0
        for arr in cellSet:
            allY += arr[1]
            blocks += 1
        holesWeight = 40
        bumpinessWeight = 5
        return 1000 - holesWeight*self.holes(board) - bumpinessWeight*self.bumpiness(board)
        
    def findBestPos(self, board):
        bestI = 0
        bestJ = 0
        bestScore = 0
        highest = self.boardsHighest(board)
        prevHoles = self.holes(board)
        lowestHole = self.lowestHoles(board)
        if highest < lowestHole:
            minX = 0
        else:
            minX = 1
        for i in range(4):
            for j in range(minX, board.width, 1):
                newBoard = self.moveToTarget(board, i, j)
                highest = self.boardsHighest(newBoard)
                lowestHole = self.lowestHoles(newBoard)
                if highest < lowestHole:
                    minX = 0
                else:
                    minX = 1
                for k in range(4):
                    for l in range (minX, board.width, 1):
                        newerBoard = self.moveToTarget(newBoard, k, l)
                        score = self.score_board(newerBoard)
                        if score > bestScore:
                            bestI = i
                            bestJ = j
                            bestScore = score
        newBoard = self.moveToTarget(board, bestI, bestJ)
        currentHoles = self.holes(newBoard)
        if currentHoles - prevHoles > 0 and board.discards_remaining > 0:
            self.sequence.clear()
            self.sequence.append(Action.Discard)
    
    def choose_action(self, board):
        if len(self.sequence) == 0:
            self.findBestPos(board)
        return self.sequence.pop(0)
SelectedPlayer = RoshansPlayer