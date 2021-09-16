# Connect Four V1 By Nolan Lowhorn 8-23-21
# Credit to freeCodeCamp.org

# Imports
import pygame
import numpy as np
import math

# Key coordinates
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Classes

# Triangle
class Triangle:
    def __init__(self, size, blink, timer, placement):
        self.size = size
        self.blink = blink
        self.timer = timer
        self.placement = placement

    # Shows triangle
    def show(self):
        if turn == 0:
            pygame.draw.polygon(screen, RED, [(self.size * self.placement - self.size + 6, 20), (self.size * self.placement + 5, 60), (self.size * self.placement + self.size + 6, 20)])
        else:
            pygame.draw.polygon(screen, YELLOW, [(self.size * self.placement - self.size + 6, 20), (self.size * self.placement + 5, 60), (self.size * self.placement + self.size + 6, 20)])

    # Updates state
    def update(self, pressed_keys):

        # Movement
        if pressed_keys[K_LEFT]:
            self.placement -= 2.5
            self.show()
        elif pressed_keys[K_RIGHT]:
            self.placement += 2.5
            self.show()

        # Checks for out of bounds
        if self.placement > 16:
            self.placement = 16
        elif self.placement < 1:
            self.placement = 1

        # Timer for blinking
        self.timer += 1
        if self.timer > 20:
            self.blink = not self.blink
            self.timer = 0

        # Displays triangle
        if self.blink is True and game_over is False:
            self.show()
            if self.timer == 1:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("blip.wav"))

# Functions

# Creates board in console
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Places piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Checks for valid location for placing piece
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Gets the next row for placing
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Prints board
def print_board(board):
    print(np.flip(board, 0))

# Checks for win
def winning_move(board, piece):

    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
       for r in range(ROW_COUNT):
           if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
               return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Blue board
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Black circles
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

# Variables

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Player turn
turn = 0

# Screen size
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Square size
SQUARESIZE = 100

# Columns and Rows
COLUMN_COUNT = 7
ROW_COUNT = 6

# Radius
RADIUS = int(SQUARESIZE/2 - 2)

# Triangle
triangle = Triangle(40, True, 0, 1)

# Initialize pygame
pygame.init()

# Initializes sound
pygame.mixer.init()

# Setup frame rate
clock = pygame.time.Clock()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Prints board
board = create_board()
print_board(board)

# Font
myfont = pygame.font.SysFont("monospace", 75)

# Main Loop
game_over = False
while not game_over:

    # Black screen
    screen.fill(BLACK)

    # Key presses
    pressed_keys = pygame.key.get_pressed()

    # Looks at every event in the game
    for event in pygame.event.get():
        # If users hits a key
        if event.type == KEYDOWN:
            # If it was the ESCAPE key
            if event.key == K_ESCAPE:
                # Stops loop
                game_over = True

        # If closes the window
        elif event.type == QUIT:
            game_over = True

        # If presses down
        elif pressed_keys[K_DOWN]:
            # Player 1 Input
            if turn == 0:
                col = int(math.floor((triangle.placement*triangle.size) / SQUARESIZE))

                # Places piece if location is valid
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("drop.wav"))
                    turn += 1

                    # If wins
                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # Player 2 Input
            else:
                col = int(math.floor((triangle.placement*triangle.size) / SQUARESIZE))

                # Places piece if location is valid
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("drop.wav"))
                    turn -= 1

                    # If wins
                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

    # Board
    draw_board(board)

    # Triangle
    triangle.update(pressed_keys)

    # Updates screen
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

    # Stops if over
    if game_over:
        pygame.time.wait(3000)