import turtle
import sys, pygame
import random

pygame.init()
width = 1200
height = 800
cell_size=40
fps=10
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("PacMan")

speed = [0, 0]
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0,0,255)
pacman = pygame.image.load("pacmanright.png")
ghosts_imgs=[
    
]
ballrect = pacman.get_rect()
tamaño_celda = 40
tablero = [ 
    "##########################" , 
    "#............##............#" , 
    "#.####.#####.#####.#####.#" , 
    "#o###.#####.##.#####.####o#" , 
    "#.####.#####.#####.####.####.#" , 
    "#..........................#" , 
    "#.####.########.#####.####.#" , 
    "#.####.########.#####.####.#" ,
    "#......##....##.##......#" , 
    "######.##### ## #####.######" , 
    "######.##### ## #####.######" , 
    "######.## ##.######" , 
    "######.## ###--### ##.######" , 
    "######.## # # ##.######" , 
    " ## # # ##" , 
    "######.## # # ##.######" , 
    "######.## ######## ##.######" , 
    "######.## ##.######" , 
    "######.## ######## ##.######" , 
    "######.## ######## ##.######" , 
    "#............##............#" , 
    "#.####.#####.##.#####.####.#" , 
    "#.####.#####.##.#####.####.#" , 
    "#o..##................##..o#" , 
    "###.##.##.########.##.##.###" , 
    "###.##.##.########.##.##.###" , 
    "#......##....##....##......#" , 
    "#.##########.##.##########.#" , 
    "#.##########.##.#########.#" , 
    "#............................#" , 
    "############################"
 ]

def draw_board (): 
    for y, row in enumerate (tablero):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, AZUL, (x*cell_size, y * cell_size, cell_size, cell_size))
            elif cell== ".":
                pygame.draw.circle (screen, BLANCO, (x*cell_size + cell_size//2, y*cell_size+ cell_size//2),3)
            elif cell=="o":
                pygame.draw.circle(screen, BLANCO,(x+cell_size+cell_size//2,y*cell_size+cell_size//2),7)
run = True  

while run:
    pygame.time.delay(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    draw_board()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ballrect=ballrect.move(0,-1)
        pacman=pygame.image.load("pacmanup.png")
    if keys[pygame.K_DOWN]:
        ballrect=ballrect.move(0,1)
        pacman=pygame.image.load("pacmandown.png")
    if keys[pygame.K_RIGHT]:
        ballrect=ballrect.move(1,0)
        pacman=pygame.image.load("pacmanright.png")
    if keys[pygame.K_LEFT]:
        ballrect=ballrect.move(-1,0)
        pacman=pygame.image.load("pacmanleft.png")
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[1] = -speed[1]

    screen.fill("black")
    screen.blit(pacman, ballrect)
    pygame.display.flip()

pygame.quit()
