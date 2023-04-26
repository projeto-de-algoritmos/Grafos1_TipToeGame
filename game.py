import pygame, sys
from pygame.locals import *
import random


# Configurações do tabuleiro
square_size = 50
square_margin = 3
board_width = 8 * square_size + 9 * square_margin
board_height = 8 * square_size + 9 * square_margin
#define tamanho tabuleiro
rows = 15
columns = 15
size = width, height = ((square_size + square_margin)*rows, (square_size + square_margin)*columns)

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
running = True
# Define o tamanho da tela
screen = pygame.display.set_mode(size)
# Define o título da janela
pygame.display.set_caption("Encontre o caminho!")
# delimita o tabuleiro
pygame.draw.rect(screen, green, (0,0, width, height), 5)

# cria tabuleiro
def createBoard(row, column):
   
    board = []
    for i in range(row):
        board.append([])
        for j in range(column):
            board[i].append(0)
            if i< 2: # duas primeiras linhas, que sao a linha de chegada
                board[i][j] = 5
                if i==0 and j%2==0:
                    board[i][j] = 3
                elif i==1 and j%2!=0:
                    board[i][j] = 3 
            elif i==(row-1):
                board[i][j] = 6

    # Geracao de buracos no tabuleiro
    for i in range(row):
        board[i][random.randint(0,column-1)] = 1   # numero 1 indica que existe um buraco

    return board
    
# Cria quadrado
def drawSquare(row, column, color):
    x = column * (square_size + square_margin) + square_margin
    y = row * (square_size + square_margin) + square_margin
    rect = pygame.Rect(x, y, square_size, square_size)
    pygame.draw.rect(screen, color, rect)

def centralizeImage():
    return (xPlayer * (square_size + square_margin) + square_margin + square_size/2, yPlayer * (square_size + square_margin) + square_margin + square_size/2)

# desenha tabuleiro
def drawBoard(board):
    for row in range(rows):
        for column in range(columns):
            # desenha quadrado preto
            if board[row][column] == 0 or board[row][column] == 1:  # numero 1 indica que existe buraco
                drawSquare(row, column, orange)
            # desenha quadrado vermelho
            # desenha quadrado amarelo
            elif board[row][column] == 2:
                drawSquare(row, column, yellow)
                player_loc.center = centralizeImage()
            # desenha quadrado azul/linha de chegada
            elif board[row][column] == 5:
                drawSquare(row, column, blue)
            # desenha quadrado rosa/linha de ponto de partida
            elif board[row][column] == 6:
                drawSquare(row, column, pink)
            elif board[row][column] == 3:
                drawSquare(row, column, white)
            elif board[row][column] == 4:
                drawSquare(row, column, lightOrange)
            elif board[row][column] == 7:   # se for 7, indica que o buraco foi pisado
                drawSquare(row, column, red)  

# define movimento do jogador
def movePlayer(direction):
    global xPlayer, yPlayer, corLast, xTrail, yTrail
    board[yPlayer][xPlayer] = 4 #rastro
    board[yTrail][xTrail] = corLast
    yTrail, xTrail = (yPlayer,xPlayer)
    xPlayer += direction[0]
    yPlayer += direction[1]

    if board[yPlayer][xPlayer] == 1 or board[yPlayer][xPlayer] == 7: # caso ele passe em um buraco
        board[yPlayer][xPlayer] = 7
        xPlayer, yPlayer = (random.randint(0,columns-1),rows-1)
    
       

    corLast = board[yPlayer][xPlayer]
    board[yPlayer][xPlayer] = 2


board = createBoard(rows, columns)
# posicao inicial do jogador
player = xPlayer, yPlayer = (random.randint(0,columns-1),rows-1)
# guarda a cor do ultimo quadrado que o jogador pisou
corLast = board[yPlayer][xPlayer]
board[yPlayer][xPlayer] = 2
yTrail, xTrail = (yPlayer,xPlayer)

playerIcon = pygame.image.load('jujuba.png')
playerIcon = pygame.transform.scale(playerIcon, (square_size, square_size))
player_loc = playerIcon.get_rect()
player_loc.center = centralizeImage()


# Definir as fontes
font = pygame.font.Font(None, 36)

fontFooter = pygame.font.SysFont('verdana', 20, italic = pygame.font.Font.italic)

def computer_play():
    while True:

        screen.fill("white")
        

        pygame.display.update()


def play():

    while True:
    
        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)
        
        for event in pygame.event.get():
                
            if event.type == KEYDOWN:
                if event.key in [K_LEFT, K_a]:
                    if xPlayer > 0:
                        movePlayer([-1,0])
                if event.key in [K_RIGHT, K_d]:
                    if xPlayer < rows-1:
                        movePlayer([1,0])
                if event.key in [K_UP, K_w]:
                    if yPlayer > 0:
                        movePlayer([0,-1])
                if event.key in [K_DOWN, K_s]:
                    if yPlayer < rows-1:
                        movePlayer([0,1])

        pygame.display.update()
        

def main_menu():
    while True:
        screen.fill(lightBlue)
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto do titulo

        MENU_TEXT = font.render("TIP TOE - FALL GUYS", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height * 0.2))


        # Texto do rodape

        FOOTER_TEXT = font.render("Trabalho de Grafos 1 - @AntonioRangelC e @kessJhones", True, white)
        FOOTER_RECT = FOOTER_TEXT.get_rect(center=(width/2, height*0.9))


        # Definir os botões

        PLAY_BUTTON = pygame.Rect((width/3), (height/3), 300, 50)
        PLAY_TEXT = font.render("Jogar Solo", True, white)
        PLAY_TEXT_RECT = PLAY_TEXT.get_rect(center=PLAY_BUTTON.center)
        
        COMPUTER_PLAY_BUTTON = pygame.Rect((width/3), (height/3) + (height * 0.15), 300, 50)
        COMPUTER_PLAY_TEXT = font.render("Jogar com amigos", True, white)
        COMPUTER_PLAY_TEXT_RECT =  COMPUTER_PLAY_TEXT.get_rect(center=COMPUTER_PLAY_BUTTON.center)

        QUIT_BUTTON = pygame.Rect((width/3), (height/3) + (height * 0.30), 300, 50)
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