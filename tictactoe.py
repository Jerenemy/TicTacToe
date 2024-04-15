#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Computer Networks
# Homework 1: Tic-tac-toe game
#
# Jeremy Zay

import random

import pygame as pg 
from sys import exit
pg.init()

#SIZE OF BOARD
SIZE = 800

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
PURPLE = ( 211, 3, 252)
YELLOW = (255, 241, 0)
ORANGE = (255, 140, 0)



class Window:
    def __init__(self, size, color):
        self.x = 0
        self.y = 0
        self.color = color
        self.paused = 0
        self.size = size
        self.screen = pg.display.set_mode((size, size))
        
    def display(self):
        # print("displaying\n\n\n")
        self.screen.fill(self.color)
        pg.display.set_caption("Tic Tac Toe")
        #pg.display.update()

    
        
class Square():
    """
    Square class that makes up Board
    """
    
    def __init__(self, x_coord, y_coord, square_size):
        self.square_str = "_"
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.square_size = square_size
        self.x_width = int(self.square_size * .12)
        self.o_width = int(self.square_size * .08)
        self.x_color = RED
        self.o_color = GREEN
        
    def __str__(self):
        return self.square_str
    
    def set_square(self, player):
        self.square_str = player.symbol
        
    def display(self, window):
        #window.screen.blit()
        if self.square_str == "x":
            self.draw_x(window)
        elif self.square_str == "o":
            self.draw_o(window)
        


    def draw_x(self, window):
        # Draw an "X" shape
        # Calculate center and offsets
        center_x, center_y = self.x_coord + self.square_size // 2, self.y_coord + self.square_size // 2
        offset = .7*self.square_size//2   # Half the size of the "X"
        
        # Top-left to bottom-right
        pg.draw.line(window.screen, self.x_color, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), self.x_width)
        # Top-right to bottom-left
        pg.draw.line(window.screen, self.x_color, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), self.x_width)

    def draw_o(self, window):
        
        center_x, center_y = self.x_coord + self.square_size // 2, self.y_coord + self.square_size // 2
        radius = .8*self.square_size//2 
        pg.draw.circle(window.screen, self.o_color, (center_x, center_y), radius, self.o_width)  # Draw white circle


class Board():
    """
    TicTacToe game board
    """

    def __init__(self, n, window):
        self.n = n
        self.board_list = []
        self.window = window
        self.init_board_list()
        self.grid_color = WHITE


    def __str__(self):
        board_str = ""
        
        for i in range(self.n):
            for j in range(self.n):
                board_str += str(self.get_square(i, j)) + " "
            board_str += "\n"

        return board_str
        
    def get_square(self, row, col):
        return self.board_list[row][col]    
    
    def init_board_list(self):
        
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row += [Square((j*(self.window.size//self.n)), (i*(self.window.size//self.n)), self.window.size//self.n)]
            self.board_list += [row]
        

    def display(self):
        '''
        prints itself (board) using __str__
        and displays itself in window using pygame
        '''
        print(self)
        self.display_grid()
        self.display_moves()
        #print("displayed!!!!!")
        pg.display.update()
    
    
    
    def display_grid(self):

        grid_width = self.window.size // (20*self.n)
        # Create a surface for the rectangle (size 100x50)
        rect_surface = pg.Surface((grid_width, self.window.size))

        # Fill the rectangle surface with a color (optional, for transparency)
        rect_surface.fill((0, 0, 0))
        rect_surface.set_colorkey((0, 0, 0))  # Making black transparent


        # Rotate the surface to get a diagonal rectangle
        angle = 45  # Rotate by 45 degrees
        rotated_rect_surface = pg.transform.rotate(rect_surface, angle)
        # Blit the rotated rectangle onto the screen
        self.window.screen.blit(rotated_rect_surface, (100, 100))  # Adjust position as needed

        for i in range(self.n-1):

            pg.draw.rect(rect_surface, self.grid_color, rect_surface.get_rect())
            self.window.screen.blit(rect_surface, ((i+1)*(self.window.size // (self.n)), 0))

        for i in range(self.n-1):
            pg.draw.rect(rect_surface, self.grid_color, rect_surface.get_rect())
            self.window.screen.blit(pg.transform.rotate(rect_surface, 90), (0, (i+1)*(self.window.size // (self.n))))


    
    def display_moves(self):
        for row in self.board_list:
            for square in row:
                square.display(self.window)
        
    
    def update_board(self, move, player):
        row, col = move
        self.board_list[row][col].set_square(player)
        
    def check_compl_horiz_row(self, player):
        for row in self.board_list:
            if all(str(square) == player.symbol for square in row):
                return True
        return False
    
    def check_compl_vert_row(self, player):
        for i in range(self.n):
            if all(str(row[i]) == player.symbol for row in self.board_list):
                return True
        return False            
    
    def check_compl_diag_ul_lr(self, player):
        for i in range(self.n):
            if str(self.get_square(i, i)) != player.symbol:
                return False
        return True
    
    def check_compl_diag_ur_ll(self, player):
        for i in range(self.n):
            if str(self.get_square(i, self.n - i - 1)) != player.symbol:
                return False
        return True  
    
    
    
class TicTacToe():
    """
    TicTacToe game
    """

    def __init__(self, n, window):
        
        self.n = n #dimensions
        self.window = window
        self.board = Board(n, self.window)



    def display(self):
        '''
        prints the board using its __str__ method
        and displays the board using pygame
        '''
        #print(self.board)
        self.window.display()
        self.board.display()
        
    def display_print(self):
        '''
        ONLY prints board to terminal, does not display with pygame
        '''
        print()
        print(self.board)
        
        
    def check_winner(self, player):
        '''
        Player -> bool
        returns whether or not the game is over
        '''
        return (self.board.check_compl_horiz_row(player) or self.board.check_compl_vert_row(player)
                or self.board.check_compl_diag_ul_lr(player) or self.board.check_compl_diag_ur_ll(player))
            
    
    def update_board(self, move, player):
        player.print_player_move() #print who just moved
        self.board.update_board(move, player)
    
    def is_valid_move(self, move):
        '''
        int, int -> bool
        returns whether or not (row, col) is a valid move
        '''
        #check types
        row, col = move
        if not (type(row) == type(col) == int):
            return False
        #check within range
        if row >= self.n or col >= self.n or row < 0 or col < 0:
            return False
        #check not already moved there
        if str(self.board.get_square(row, col)) != "_":
            return False
        #if satisfies everything, return true
        return True
    
    def check_draw(self, player):
        '''
        returns true if draw (player has no valid moves), false otherwise
        '''
        return player.get_valid_moves(self) == []
            
    def check_done(self, player):
        '''
        return true if game over, print message, false otherwise
        '''
        if self.check_winner(player):
            print(f"Winner: {player.symbol} !")
            return True
        elif self.check_draw(player):
            print(f"Draw :|")
            return True
        return False
        
   

class Player():
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def print_player_move(self):
        '''
        prints which player's turn it is
        '''
        print(f"{self.name} move:")
        
    def get_valid_moves(self, ttt):
        '''
        TicTacToe -> list[(int,int)]
        returns list of all valid moves that can be made in ttt
        '''
        n = ttt.n
        valid_moves = []
        for i in range(n):
            for j in range(n):
                if ttt.is_valid_move((i, j)):
                    valid_moves += [(i, j)]
        return valid_moves
    

class User(Player):
    
    def get_move(self, ttt):

        while True:
            # print("starting while true in get_move")
            for event in pg.event.get():
                # print("starting for event in in get_move")

                #quit upon exit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    #print(mouse_pos)
                    move = self.translate_mouse_pos_to_move(mouse_pos, ttt.n, ttt.window.size)
                    if ttt.is_valid_move(move):
                        #print("valid move")
                        return move
                    
                    print("NOT valid move")
        
            
    def translate_mouse_pos_to_move(self, mouse_pos, n, size):
        y_pos, x_pos = mouse_pos
        row, col = (-1, -1)
        for i in range(n):
            if x_pos <= (size // n) * (1+i):
                row = i
                break
        for i in range(n):
            if y_pos <= (size // n) * (1+i):
                col = i
                break
        return (row, col)
            
            

class AI(Player):
    
    
    def get_move(self, ttt):
        '''
        TicTacToe -> (int, int)
        returns random valid move for ai to make
        '''
        valid_moves = self.get_valid_moves(ttt)
        random_move_index = random.randint(0, len(valid_moves)-1)

        return valid_moves[random_move_index]
        
        
class User2(Player):
    
    def get_move_on_board(self, ttt):
        n = ttt.n
        string = "Choose row [0-" + str(n-1) + "]: "
        row = input(string)
        while not row.isnumeric() or int(row) < 0 or int(row) >= n:
            print("Invalid move!")
            row = input("Enter row: ")

        string = "Choose col [0-" + str(n-1) + "]: "
        col = input(string)
        while not row.isnumeric() or int(col) < 0 or int(col) >= n:
            print("Invalid move!")
            col = input("Enter col: ")
        
        return (int(row), int(col))

        
    def get_move(self, ttt):

        move = self.get_move_on_board(ttt)
        while not ttt.is_valid_move(move):
            print("Invalid move!")
            move = move = self.get_move_on_board(ttt)
        
        return move
    
class Server():
    """
    Server for TicTacToe game
    """
    
    def get_input(self):
        
        n = input("Enter number of rows in TicTacToe board: ")
        while not n.isdigit() or int(n) == 0:
            n = input("Invalid number of rows.\nEnter number of rows in TicTacToe board: ")
        return int(n)
 
    
    def play(self):
        '''
        plays TicTacToe game
        NOT CALLED WHEN PLAYED THROUGH SERVER AND CLIENT
        '''
        print("==================")
        print("| TicTacToe Game |")
        print("==================\n")
        
        n = self.get_input()
        window = Window(SIZE, BLACK)
        ttt = TicTacToe(n, window)
        user = User("User", "o")
        ai = AI("Server", "x")

        
        
        current_player = user
        #window.display()
        ttt.display() #display blank board
        #window.display()
        
        run = True
        while run:
            
            #quit upon exit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            #current_player.print_player_move() #print who just moved
            ttt.update_board(current_player.get_move(ttt), current_player) #update board, pass move and current player
            
            ttt.display() #display updated board
            
            if ttt.check_winner(current_player):
                print(f"Winner: {current_player.symbol} !") #print winner
                
                run = False #check for winner
            elif ttt.check_draw(current_player):
                print(f"Draw :|") 
                run = False

            current_player = ai if current_player == user else user #alternate player
            
            pg.display.update()
                
                   

def main():
    s = Server()
    s.play()
       


if __name__ == '__main__':
    main()