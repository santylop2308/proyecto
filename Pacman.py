import pygame

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
score = 0
font = pygame.font.Font(None, 36)

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

# Bucle principal del juego
run = True
while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    # Intento de movimiento
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

    # **Verificar colisión antes de mover**
    if 0 <= new_y < len(tablero) and 0 <= new_x < len(tablero[0]):  # Asegurar que la nueva posición está dentro del tablero
        if tablero[new_y][new_x] != "#":  # Solo se mueve si no es pared
            pacman_x, pacman_y = new_x, new_y

    # **Comer puntos**
    if tablero[pacman_y][pacman_x] == ".":  # Si hay un punto en la posición actual
        score += 1  # Sumar puntos
        tablero[pacman_y][pacman_x] = " "  # Eliminar el punto del tablero

    if tablero[pacman_y][pacman_x] == "o":  # Si hay un punto en la posición actual
        score += 10  # Sumar puntos
        tablero[pacman_y][pacman_x] = " "  # Eliminar el punto del tablero

    # Limpiar pantalla
    screen.fill(NEGRO)
    draw_board()
    draw_pacman()

    # Mostrar el puntaje
    score_text = font.render(f'Score: {score}', True, BLANCO)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
