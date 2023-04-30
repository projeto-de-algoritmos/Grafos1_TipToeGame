import pygame
import sys
from pygame.locals import *
import random
import time
import grafo as gf

# Configurações do tabuleiro
square_size = 50
square_margin = 3
board_width = 8 * square_size + 9 * square_margin
board_height = 8 * square_size + 9 * square_margin
rows = 15
columns = 15
size = width, height = ((square_size + square_margin)
                        * rows, (square_size + square_margin)*columns)
# grafo para apartir do tabuleiro
graph = gf.Graph(rows*columns)
end = [int(i) for i in range(15, 29)]

# cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
gray = (128, 128, 128)
yellow = (255, 255, 30)
blue = (0, 0, 255)
pink = (255, 20, 147)
orange = (223, 118, 2)
lightOrange = (255, 195, 128)
lightBlue = '#5dc9ee'
secondary_pink = '#ff799b'


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('TIP TOE') 
pygame.draw.rect(screen, green, (0, 0, width, height), 5)

# cria tabuleiro
def createBoard(row, column):

    board = []
    for i in range(row):
        board.append([])
        for j in range(column):
            board[i].append(0)
            if i < 2:  # duas primeiras linhas, que sao a linha de chegada
                board[i][j] = 5
                if i == 0 and j % 2 == 0:
                    board[i][j] = 3
                elif i == 1 and j % 2 != 0:
                    board[i][j] = 3
            elif i == (row-1):
                board[i][j] = 6

    # Geracao de buracos no tabuleiro
    for i in range(2, row-1):
        # numero 1 indica que existe um buraco
        board[i][random.randint(0, column-1)] = 1
        board[i][random.randint(0, column-1)] = 1


    return board

# Cria quadrado
def drawSquare(row, column, color):
    x = column * (square_size + square_margin) + square_margin
    y = row * (square_size + square_margin) + square_margin
    rect = pygame.Rect(x, y, square_size, square_size)
    pygame.draw.rect(screen, color, rect)


def centralizeImage():
    return (xPlayer * (square_size + square_margin) + square_margin + square_size/2, yPlayer * (square_size + square_margin) + square_margin + square_size/2)


def startPosition():
    return (random.randint(0,columns-1), rows-1)

# desenha tabuleiro
def drawBoard(board):

    for row in range(rows):
        for column in range(columns):
            # numero 1 indica que existe buraco
            if board[row][column] == 0 or board[row][column] == 1:
                drawSquare(row, column, orange)
            elif board[row][column] == 2:
                drawSquare(row, column, yellow)
                player_loc.center = centralizeImage()
            elif board[row][column] == 4:
                drawSquare(row, column, lightOrange)
            elif board[row][column] == 5:
                drawSquare(row, column, blue)
            elif board[row][column] == 6:
                drawSquare(row, column, pink)
            elif board[row][column] == 7:   # se for 7, indica que o buraco foi pisado
                drawSquare(row, column, red)

# define movimento do jogador
def movePlayer(direction, mode):
    global xPlayer, yPlayer, trail

    xPlayer += direction[0]
    yPlayer += direction[1]

    if recordMoviments() and mode == 'computer':
        return False
    else:
        return True
    
def recordMoviments():
    global xPlayer, yPlayer, trail

    if board[yPlayer][xPlayer] == 1 or board[yPlayer][xPlayer] == 7:  # caso ele passe em um buraco
        board[yPlayer][xPlayer] = 7
        index = graph.coordinatesToIndex([xPlayer, yPlayer], board)
        graph.removeBlock(index)
        xPlayer, yPlayer = startPosition()
        board[yPlayer][xPlayer] = 2
        cleanTrail()
        trail.append([xPlayer, yPlayer, 6])
        return False
    
    elif yPlayer == 1:  # caso ele chegue ao final
        time.sleep(2.6)
        xPlayer, yPlayer = startPosition()
        board[yPlayer][xPlayer] = 2
        cleanTrail()
        trail.append([xPlayer, yPlayer, 6])
        player_loc.center = centralizeImage()
        win()

    else:
        markTrail()
        if [xPlayer, yPlayer, 6] not in trail:
            trail.append([xPlayer, yPlayer, board[yPlayer][xPlayer]])
        board[yPlayer][xPlayer] = 2
        return True

def markTrail():
    global trail
    for i in trail:
        X, Y, cor = i
        board[Y][X] = 4

def cleanTrail():
    global trail
    for i in range(len(trail)):
        X, Y, cor = trail[i]
        board[Y][X] = cor
    trail = []

def win():
    screen.fill(lightBlue)
    global board
    board = createBoard(rows, columns)
    graph.matrixToGraph(board)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto do titulo

        WIN_TEXT = font.render("PARABÉNS ! VOCÊ VENCEU", True, white)
        WIN_RECT = WIN_TEXT.get_rect(center=(width/2, height * 0.15))

        
        # Definir os botões

        MENU_BUTTON = pygame.Rect((width/3), (height/3), 300, 50)
        MENU_TEXT = font.render("Voltar ao menu", True, white)
        MENU_TEXT_RECT = MENU_TEXT.get_rect(center=MENU_BUTTON.center)

        
        QUIT_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.10), 300, 50)
        QUIT_TEXT = font.render("Sair", True, white)
        QUIT_TEXT_RECT = QUIT_TEXT.get_rect(center=QUIT_BUTTON.center)

        pygame.draw.rect(screen, secondary_pink, MENU_BUTTON)
        pygame.draw.rect(screen, secondary_pink, QUIT_BUTTON)

        screen.blit(WIN_TEXT, WIN_RECT)
        screen.blit(MENU_TEXT, MENU_TEXT_RECT)
        screen.blit(QUIT_TEXT, QUIT_TEXT_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.collidepoint(MENU_MOUSE_POS):
                    main_menu()

                if QUIT_BUTTON.collidepoint(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# define movimento do computador
def playComputer():
    global xPlayer, yPlayer, board
    start = graph.coordinatesToIndex([xPlayer,yPlayer],board)
    path = graph.dfs(start, end)
    graph.clearVisited()
    path = graph.pathToMoves(path, board)

    return path

    
board = createBoard(rows, columns)
graph.matrixToGraph(board)
player = xPlayer, yPlayer = startPosition()
trail = []
trail.append([xPlayer, yPlayer, board[yPlayer][xPlayer]])
board[yPlayer][xPlayer] = 2

# carrega imagem do jogador
playerIcon = pygame.image.load('jujuba.png')
playerIcon = pygame.transform.scale(playerIcon, (square_size, square_size))
player_loc = playerIcon.get_rect()
player_loc.center = centralizeImage()

# Definir as fontes
font = pygame.font.Font(None, 36)
fontFooter = pygame.font.SysFont('verdana', 20, italic=pygame.font.Font.italic)

def computer_play():
    path = playComputer()
    while True:
        
        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if path != None and len(path) > 0:
            x, y = path.pop(0)
            if movePlayer([x, y], 'computer'):
                path = playComputer()
        
        time.sleep(0.5)

        pygame.display.update()


def play():
    while True:

        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_LEFT, K_a]:
                    if xPlayer > 0:
                        movePlayer([-1, 0], 'player')
                if event.key in [K_RIGHT, K_d]:
                    if xPlayer < rows-1:
                        movePlayer([1, 0], 'player')
                if event.key in [K_UP, K_w]:
                    if yPlayer > 0:
                        movePlayer([0, -1], 'player')
                if event.key in [K_DOWN, K_s]:
                    if yPlayer < rows-1:
                        movePlayer([0, 1], 'player')

        pygame.display.update()

def main_menu():
    while True:
        screen.fill(lightBlue)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto do titulo

        MENU_TEXT = font.render("TIP TOE - FALL GUYS", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height * 0.2))

        # Texto do rodape

        FOOTER_TEXT = font.render(
            "Trabalho de Grafos 1 - @AntonioRangelC e @kessJhones", True, white)
        FOOTER_RECT = FOOTER_TEXT.get_rect(center=(width/2, height*0.9))

        # Definir os botões

        PLAY_BUTTON = pygame.Rect((width/3), (height/3), 300, 50)
        PLAY_TEXT = font.render("Jogador vs Máquina", True, white)
        PLAY_TEXT_RECT = PLAY_TEXT.get_rect(center=PLAY_BUTTON.center)

        COMPUTER_PLAY_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.15), 300, 50)
        COMPUTER_PLAY_TEXT = font.render("Máquina vs Máquina", True, white)
        COMPUTER_PLAY_TEXT_RECT = COMPUTER_PLAY_TEXT.get_rect(
            center=COMPUTER_PLAY_BUTTON.center)

        QUIT_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.30), 300, 50)
        QUIT_TEXT = font.render("Sair", True, white)
        QUIT_TEXT_RECT = QUIT_TEXT.get_rect(center=QUIT_BUTTON.center)

        pygame.draw.rect(screen, secondary_pink, PLAY_BUTTON)
        pygame.draw.rect(screen, secondary_pink, COMPUTER_PLAY_BUTTON)
        pygame.draw.rect(screen, secondary_pink, QUIT_BUTTON)

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(PLAY_TEXT, PLAY_TEXT_RECT)
        screen.blit(COMPUTER_PLAY_TEXT, COMPUTER_PLAY_TEXT_RECT)
        screen.blit(QUIT_TEXT, QUIT_TEXT_RECT)
        screen.blit(FOOTER_TEXT, FOOTER_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.collidepoint(MENU_MOUSE_POS):
                    play()
                if COMPUTER_PLAY_BUTTON.collidepoint(MENU_MOUSE_POS):
                    computer_play()
                if QUIT_BUTTON.collidepoint(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
pygame.quit()
