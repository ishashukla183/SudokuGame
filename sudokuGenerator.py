import turtle
from random import randint,shuffle
from sudokuSolver import valid, find_empty


numberList=[1,2,3,4,5,6,7,8,9]
def solve(board): #recursive method
    find=find_empty(board)
    if not find: #base case, puzzle solved
        return True
    else:
        row, col=find
        
    for i in numberList: #try all values from 1-9 and check if it is valid
        shuffle(numberList)
        if valid(board, i, (row, col)):
            board[row][col]= i
             
            if solve(board):
                return True
            
            board[row][col]=0 #if not valid reset value (back tracking)
            
    return False


def createBoard():
    board = []
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    solve(board)
    originalBoard=[]
    originalBoard=board.copy()


#Start Removing Numbers one by one
   
#A higher number of attempts will end up removing more numbers from the grid
#Potentially resulting in more difficiult grids to solve!
    attempts = 60


    while attempts>0:
        #Select a random cell that is not already empty
        row = randint(0,8)
        col = randint(0,8)
        while board[row][col]==0:
            row = randint(0,8)
            col = randint(0,8)
        #Remember its cell value in case we need to put it back  
        backup = board[row][col]
        board[row][col]=0
  
        #Take a full copy of the grid
        copyBoard = []
        for r in range(0,9):
            copyBoard.append([])
            for c in range(0,9):
                copyBoard[r].append(board[r][c])
  
       #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)  
        solve(copyBoard) 
        attempts-=1
       #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
        for i in range(9):
            for j in range(9):
                if copyBoard[i][j]!=originalBoard[i][j]:
                    board[row][col]=backup
                    
        
    return board
