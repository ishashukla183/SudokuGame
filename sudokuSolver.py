#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Sudoku Solver
#Algorithm: Bruteforce method using recursive backtracking
#Rules: Digit cannot be repeated in a column, row or the corresponding 3x3 square
from random import randint,shuffle
def print_puzzle(board):
    for i in range(len(board)):
        if i%3==0 and i!=0:
            print("----------------------------")
        for j in range(len(board[0])):
            if j%3==0:
                print(" | ", end="")
            if j==8:
                print(str(board[i][j]) +" | ")
            else:
                print(str(board[i][j]) + " ",end="")


# In[2]:

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


# In[3]:


#find blank values in the puzzle that need to be filled in
def find_empty(board) :
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                return (i,j) #return(row, column)
    return None


# In[4]:


#check if position for a given number is valid
def valid(board, num, position): #position=(row, column)
    #check row for repeating number
    for i in range(len(board[0])):
        if board[position[0]][i] == num and position[1] != i :
             return False
           
   
  #check column for repeating number
    for i in range(len(board)) :
        if board[i][position[1]] == num and position[0] != i :
            return False
        
   #check corresponding 3x3 square
    box_x=position[1] // 3
    box_y=position[0] // 3

    for i in range(box_y * 3, (box_y * 3 + 3)):
        for j in range(box_x * 3, (box_x * 3 + 3)):
            if board[i][j]==num and (i,j)!=position:
                return False
    return True


# In[ ]:





# In[5]:




# In[ ]:




