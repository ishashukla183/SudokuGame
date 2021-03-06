import pygame
import time
pygame.font.init()
from sudokuGenerator import createBoard
from sudokuSolver import find_empty, valid,solve
from crooksMain import solveByCrooks

board1 = []
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

class Grid:
    board = createBoard()
    
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
         # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 5
            else:
                thick = 2
            pygame.draw.line(self.win, (0,0,0), (20, i*gap+20), (self.width+20, i*gap+20), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap+20, 20), (i * gap+20, self.height+20), thick)
         
        

       
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)
    
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
    
    def reset(self):
        for i in range(0,9):
            for j in range(0,9):
               if self.cubes[i][j].value == 0:
                 self.cubes[i][j].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None
    
        

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False
        
    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(50)

        return False
    def solveByCrooks_(self):
        for i in range(9):
            for j in range(9):
                board1[i][j]=self.cubes[i][j].value
        board2=board1.copy()
        begin=time.time()
        solve(board2)
        end=time.time()
        
        
        brute_force=str(end-begin)
        print(brute_force)
        begin1=time.time()       
        solution=solveByCrooks(board1)
        end1=time.time()
        crooks=(str(end1-begin1))
        print(crooks)
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].value=solution[i][j]
        self.update_model()
                    
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 20)

        gap = self.width / 9
        x = self.col * gap +20
        y = self.row * gap+20

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+15, y+15))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            pygame.draw.rect(win,(230,100,255),(x,y,gap,gap))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 20)

        gap = self.width / 9
        x = self.col * gap+20
        y = self.row * gap+20

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 20)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 130, 530))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 530))
    # Draw grid and board
    board.draw()
    text = fnt.render("Give up", 1, (0, 0, 0))
    pygame.draw.rect(win,(0,255,0),(20,560,100,40))
    win.blit(text, (20 + (100/2 - text.get_width()/2), 560 + (40/2 - text.get_height()/2)))
    thick=3
    pygame.draw.line(win, (0,0,0), (20, 560), (20, 600), thick)
    pygame.draw.line(win, (0, 0, 0), (120, 560), (120, 600), thick)
    pygame.draw.line(win, (0,0,0), (20, 560), (120, 560), thick)
    pygame.draw.line(win, (0, 0, 0), (20, 600), (120, 600), thick)

def selectBtn(win,pos):
    if pos[0] < 120 and pos[1] < 600 and pos[0] > 20 and pos[1]>560:
           
            x = 20
            y = 560
            gap1=100
            gap2=40
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap1, gap2), 3)
            return True
    return False
    
def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


            
def menu(win):
   white = (255, 255, 255)
   green = (0, 255, 0)
   blue = (0, 0, 128)
   win.fill((0,0,0))
   fnt = pygame.font.SysFont("comicsans", 20)
   sudokuImg=pygame.image.load('sudoku-bg1.jpg')
   bg_rect=sudokuImg.get_rect()
   win.blit(sudokuImg, bg_rect)
   text = fnt.render('Instructions', 1, (0,0,0))
   win.blit(text, (150, 160))
   text = fnt.render('1. Press Enter to begin', 1,(0,0,0))
   win.blit(text, (150, 200))
   text = fnt.render('2. Press s to get the solution', 1,(0,0,0))
   win.blit(text, (150, 240))
   text = fnt.render('3. Press r to reset', 1, (0,0,0))
   win.blit(text, (150, 280))
   
      
   pygame.display.update()
def main():
    run=True
    win = pygame.display.set_mode((540,610))
    show_menu=True
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 500, 500, win)
    key = None
    start = time.time()
    strikes = 0
    while run:
        if(show_menu):
            menu(win)
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     run = False
                     show_menu=False
                 if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                          show_menu=False
            pygame.display.update()

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_r:
                    board.reset()
                if event.key == pygame.K_s:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                if selectBtn(win,pos):
                     board.solveByCrooks_()
                     print("Game over")

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()