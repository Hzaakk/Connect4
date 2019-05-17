#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''
Controls:
    A = left
    D = right
    S = drop piece
    Q = close game
'''
import numpy as np
import cv2
import pygame
import time
import sys

pygame.init()

# board dimensions
WIDTH = 7
HEIGHT = 6

# how many to connect to win
NUM2WIN = 4

# screen size in pixels = board dimensions * WINSIZE
WINSIZE = 100


# In[4]:


class Board():
    def __init__(self):
        self.height = HEIGHT
        self.width = WIDTH
        self.size = (self.height,self.width) # board dimensions
        self.image = np.zeros((*self.size, 3)) # image w/out piece at top
        self.new_image = self.image.copy()     # image to display moving piece at top
        self.piece = Piece('Red', (255, 0, 0)) # This piece starts first
        self.game_over = False
        self.win_color = None
        
    def update(self):
        # superimposing unplaced top piece onto top of board
        self.new_image = self.image.copy()
        self.new_image[self.piece.y, self.piece.x] = self.piece.value
        
    def fall(self):
        self.piece.fallen = True
        try:
            while not any(self.image[self.piece.y+1, self.piece.x]):
                self.piece.y += 1
        except IndexError: # stop when reached end
            pass
        
        self.update()
        self.image = self.new_image.copy()
    
    def check_connection(self, x_range: int, y_range: (int, list, tuple), dir_y: int, dir_x: int):
            board = self.new_image
            color = self.piece.color
            value = self.piece.value
            
            if not isinstance(y_range, (list, tuple)): # make y_range in list format so it can be unpacked
                y_range = [y_range]
            
            for x in range(x_range):
                for y in range(*y_range):
                    if all([all(board[y + i * dir_y, x + i * dir_x] == value) for i in range(NUM2WIN)]): # checks everywhere on the board for a win
                        self.game_over = True
                        self.win_color = color
    
    def check_win(self):
        # horizontal
        self.check_connection(WIDTH-NUM2WIN+1, HEIGHT, 0, 1)
        # vertical
        self.check_connection(WIDTH, HEIGHT-NUM2WIN+1, 1, 0)
        # neg diagonals
        self.check_connection(WIDTH-NUM2WIN+1, HEIGHT-NUM2WIN+1, 1, 1)
        # pos diagonals
        self.check_connection(WIDTH-NUM2WIN+1, [NUM2WIN-1, HEIGHT], -1, 1)

class Piece():
    def __init__(self, color: str, value: (tuple, list)):
        self.fallen = False
        self.x = WIDTH // 2
        self.y = 0
        self.color = color # e.g 'Red'
        self.value = value # color in (R, G, B) format
        
    def move_right(self):
        if self.x < WIDTH - 1:
            self.x += 1
    
    def move_left(self):
        if self.x > 0:
            self.x -= 1


# In[5]:


count = 0
board = Board()

clock = pygame.time.Clock()
display = pygame.display.set_mode((board.width*WINSIZE, board.height*WINSIZE))
pygame.display.set_caption('Connect4')

while not board.game_over:
    if board.piece.fallen: # adds a new piece once one has fallen
        board.piece = Piece(*(('Red', (255,0,0)) if count % 2 else ('Blue', (0,0,255))))
        count += 1

    movement = [0, 0] # truthy index 0 means move left. truthy index 1 means move right
    fall = False # whether to drop piece

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movement[0] = 1
            if event.key == pygame.K_d:
                movement[1] = 1
            if event.key == pygame.K_s:
                fall = True
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
    
    if movement[0]:
        board.piece.move_left()
    if movement[1]:
        board.piece.move_right()
    if fall:
        board.fall()
    
    board.check_win()
    if board.game_over:
        print(board.win_color, 'has won!')
        
        
    surf = pygame.surfarray.make_surface(cv2.resize(board.new_image.transpose(1,0,2), (board.height*WINSIZE, board.width*WINSIZE), interpolation = 0)) # turns the numpy array of the board to a pygame surface
    
    # grid
    grid_color = (15,15,15)
    for i in np.linspace(WINSIZE, board.width*WINSIZE, board.width):
        pygame.draw.line(surf, grid_color, (i,0), (i,board.height*WINSIZE), 1)
    for i in np.linspace(WINSIZE, board.height*WINSIZE, board.height):
        pygame.draw.line(surf, grid_color, (0,i), ((board.height+1)*WINSIZE, i), 1)
    
    display.blit(surf, (0,0))

    pygame.display.update()
    board.update()
    clock.tick(60)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()


# In[ ]:


quit()


# In[ ]:




