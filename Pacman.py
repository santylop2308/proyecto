import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width = 840
height = 900
cell_size = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
ROSADO = (255, 182, 193)
CIAN = (0, 255, 255)
NARANJA = (255, 165, 0)

# Cargar imágenes de Pac-Man
try:
    pacman_up = pygame.image.load("pacmanup.png")
    pacman_down = pygame.image.load("pacmandown.png")
    pacman_left = pygame.image.load("pacmanleft.png")
    pacman_right = pygame.image.load("pacmanright.png")
except pygame.error:
    print("Error: No se pudieron cargar las imágenes de Pac-Man.")
    pygame.quit()
    exit()

pacman = pacman_right  # Imagen inicial

# Tablero (convertido en lista de listas para modificarlo)
tablero = [
    list("############################"),
    list("#............##............#"),
    list("#.####.#####.##.#####.####.#"),
    list("#o####.#####.##.#####.####o#"),
    list("#.####.#####.##.#####.####.#"),
    list("#..........................#"),
    list("#.####.##.########.##.####.#"),
    list("#.####.##.########.##.####.#"),
    list("#......##....##....##......#"),
    list("######.##### ## #####.######"),
    list("######.##### ## #####.######"),
    list("######.##          ##.######"),
    list("######.## ###--### ##.######"),
    list("######.## #      # ##.######"),
    list("       ## #      # ##       "),
    list("######.## #      # ##.######"),
    list("######.## ######## ##.######"),
    list("######.##          ##.######"),
    list("######.## ######## ##.######"),
    list("######.## ######## ##.######"),
    list("#............##............#"),
    list("#.####.#####.##.#####.####.#"),
    list("#.####.#####.##.#####.####.#"),
    list("#o..##................##..o#"),
    list("###.##.##.########.##.##.###"),
    list("###.##.##.########.##.##.###"),
    list("#......##....##....##......#"),
    list("#.##########.##.##########.#"),
    list("#..........................#"),
    list("############################")
]

# Posición inicial de Pac-Man
pacman_x, pacman_y = 1, 1
pacman_speed = 1
vidas = 3
score = 0
font = pygame.font.Font(None, 36)

# Imágenes del fantasma
fantasma_img = pygame.Surface((cell_size, cell_size))
fantasma_img.fill(ROJO)

# Función para comprobar si hay una pared en una dirección
def hay_pared(x, y):
    if 0 <= y < len(tablero) and 0 <= x < len(tablero[0]):
        return tablero[y][x] == "#"
    return False

# Clase Fantasma
class Fantasma:
    def __init__(self, x, y, color, tipo):
        self.x = x
        self.y = y
        self.color = color
        self.tipo = tipo  # Tipo de fantasma: 'Blinky', 'Pinky', 'Inky', 'Clyde'
        self.direccion = random.choice(['up', 'down', 'left', 'right'])
        self.img = pygame.Surface((cell_size, cell_size))
        self.img.fill(self.color)
        self.velocidad = 0.5  # Velocidad reducida para los fantasmas

    def mover(self, pacman_x, pacman_y):
        posibles_direcciones = ['up', 'down', 'left', 'right']
        random.shuffle(posibles_direcciones)  # Aleatoriza el movimiento de los fantasmas

        for direccion in posibles_direcciones:
            new_x, new_y = self.x, self.y
            if direccion == 'up':
                new_y -= 1
            elif direccion == 'down':
                new_y += 1
            elif direccion == 'left':
                new_x -= 1
            elif direccion == 'right':
                new_x += 1

            # Verificar si el nuevo movimiento es válido
            if 0 <= new_y < len(tablero) and 0 <= new_x < len(tablero[0]) and tablero[new_y][new_x] != "#":
                # Verificar si no colisiona con otro fantasma
                if not any(fantasma.x == new_x and fantasma.y == new_y for fantasma in fantasmas):
                    self.x, self.y = new_x, new_y
                    break

    def dibujar(self):
        screen.blit(self.img, (self.x * cell_size, self.y * cell_size))

# Crear instancias de los 4 fantasmas
fantasmas = [
    Fantasma(13, 11, ROJO, "Blinky"),
    Fantasma(15, 5, ROSADO, "Pinky"),
    Fantasma(7, 7, CIAN, "Inky"),
    Fantasma(5, 13, NARANJA, "Clyde")
]

# Función para dibujar el tablero
def draw_board():
    for y, row in enumerate(tablero):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, AZUL, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == ".":
                pygame.draw.circle(screen, BLANCO, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 3)
            elif cell == "o":
                pygame.draw.circle(screen, BLANCO, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 7)

# Función para dibujar a Pac-Man
def draw_pacman():
    screen.blit(pacman, (pacman_x * cell_size, pacman_y * cell_size))

# Pantalla de fin de juego
def game_over():
    screen.fill(NEGRO)
    game_over_text = font.render("GAME OVER", True, ROJO)
    score_text = font.render(f"Score: {score}", True, BLANCO)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 40))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(2000)

# Bucle principal del juego
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Intento de movimiento de Pac-Man
    new_x, new_y = pacman_x, pacman_y

    if keys[pygame.K_UP]:
        new_y -= pacman_speed
        pacman = pacman_up
    elif keys[pygame.K_DOWN]:
        new_y += pacman_speed
        pacman = pacman_down
    elif keys[pygame.K_RIGHT]:
        new_x += pacman_speed
        pacman = pacman_right
    elif keys[pygame.K_LEFT]:
        new_x -= pacman_speed
        pacman = pacman_left

    # Verificar colisión antes de mover a Pac-Man
    if 0 <= new_y < len(tablero) and 0 <= new_x < len(tablero[0]):
        if tablero[new_y][new_x] != "#":
            pacman_x, pacman_y = new_x, new_y

    # Comer puntos
    if tablero[pacman_y][pacman_x] == ".":
        score += 1
        tablero[pacman_y][pacman_x] = " "
    elif tablero[pacman_y][pacman_x] == "o":
        score += 10
        tablero[pacman_y][pacman_x] = " "

    # Mover los fantasmas
    for fantasma in fantasmas:
        fantasma.mover(pacman_x, pacman_y)

    # Revisar colisión con Pac-Man
    for fantasma in fantasmas:
        if pacman_x == fantasma.x and pacman_y == fantasma.y:
            vidas -= 1
            if vidas <= 0:
                game_over()
                run = False
            else:
                pacman_x, pacman_y = 1, 1  # Respawn de Pac-Man
                break

    # Dibujar todo
    screen.fill(NEGRO)
    draw_board()
    draw_pacman()

    for fantasma in fantasmas:
        fantasma.dibujar()

    # Mostrar el puntaje y vidas restantes
    score_text = font.render(f'Score: {score}', True, BLANCO)
    screen.blit(score_text, (10, 10))

    vidas_text = font.render(f'Vidas: {vidas}', True, BLANCO)
    screen.blit(vidas_text, (width - 150, 10))

    pygame.display.flip()

pygame.quit()
