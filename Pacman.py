import turtle
import sys, pygame

pygame.init()
size = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PacMan")
width, height = 800, 600
speed = [1, 1]
pacman = pygame.image.load("pacman.png")
ballrect = pacman.get_rect()
run = True

while run:
    pygame.time.delay(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ballrect=ballrect.move(0,-1)
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[1] = -speed[1]

    screen.fill("black")
    screen.blit(pacman, ballrect)
    pygame.display.flip()

pygame.quit()
