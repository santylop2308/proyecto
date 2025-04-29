import pygame
import random

pygame.init()

# Configuración
width, height = 840, 900
cell_size = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
ROSADO = (255, 182, 193)
CIAN = (0, 255, 255)
NARANJA = (255, 165, 0)
AZUL_CLARO = (173, 216, 230)

# Cargar imágenes
afanadorabi = pygame.image.load("afanadorabierto.png")
afanadorcer = pygame.image.load("afanadorcerrado.png")
afanadorabitri = pygame.image.load("afanadorabiertotriste.png")
afanadorcertri = pygame.image.load("afanadorcerradotriste.png")

# Tablero (lista de listas)
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

font = pygame.font.Font(None, 36)

# Auxiliar
def hay_pared(x, y):
    return tablero[y % len(tablero)][x % len(tablero[0])] == "#"

def draw_board():
    for y, row in enumerate(tablero):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell == "#":
                pygame.draw.rect(screen, AZUL, rect)
            elif cell == ".":
                pygame.draw.circle(screen, BLANCO, rect.center, 3)
            elif cell == "o":
                pygame.draw.circle(screen, BLANCO, rect.center, 7)

def draw_lives(vidas):
    for i in range(vidas):
        pygame.draw.circle(screen, (255, 255, 0), (width - 30 * (i + 1), 50), 10)

def game_over(score):
    screen.fill(NEGRO)
    txt1 = font.render("GAME OVER", True, ROJO)
    txt2 = font.render(f"Score: {score}", True, BLANCO)
    screen.blit(txt1, (width // 2 - txt1.get_width() // 2, height // 2 - 40))
    screen.blit(txt2, (width // 2 - txt2.get_width() // 2, height // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(3000)

def game_win(score):
    screen.fill(NEGRO)
    txt1 = font.render("YOU WIN", True, ROJO)
    txt2 = font.render(f"Score: {score}", True, BLANCO)
    screen.blit(txt1, (width // 2 - txt1.get_width() // 2, height // 2 - 40))
    screen.blit(txt2, (width // 2 - txt2.get_width() // 2, height // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(3000)

# Pacman
class Pacman:
    def __init__(self):
        self.x, self.y = 1, 1
        self.score = 0
        self.sprite_abierto = afanadorabi
        self.sprite_cerrado = afanadorcer
        self.sprite_triste_abierto = afanadorabitri
        self.sprite_triste_cerrado = afanadorcertri
        self.img = self.sprite_abierto
        self.direccion = (0, 0)
        self.direccion_siguiente = (0, 0)
        self.last_move_time = 0
        self.move_delay = 100  # milisegundos entre movimientos (ajusta según qué tan lento quieres)


    def mover(self, keys):
        ahora = pygame.time.get_ticks()
        if ahora - self.last_move_time < self.move_delay:
            return
        self.last_move_time = ahora

        if keys[pygame.K_UP]: self.direccion_siguiente = (0, -1)
        elif keys[pygame.K_DOWN]: self.direccion_siguiente = (0, 1)
        elif keys[pygame.K_LEFT]: self.direccion_siguiente = (-1, 0)
        elif keys[pygame.K_RIGHT]: self.direccion_siguiente = (1, 0)

        nx, ny = self.x + self.direccion_siguiente[0], self.y + self.direccion_siguiente[1]
        if not hay_pared(nx, ny):
            self.direccion = self.direccion_siguiente

        nx, ny = self.x + self.direccion[0], self.y + self.direccion[1]
        if not hay_pared(nx, ny):
            self.x, self.y = nx % len(tablero[0]), ny % len(tablero)


    def comer(self):
        global fantasmas_vulnerables, vulnerable_start_time
        celda = tablero[self.y][self.x]
        if celda == ".":
            self.score += 1
            tablero[self.y][self.x] = " "
        elif celda == "o":
            self.score += 10
            tablero[self.y][self.x] = " "
            fantasmas_vulnerables = True
            vulnerable_start_time = pygame.time.get_ticks()

    def actualizar_sprite(self, tiempo):
        triste = tiempo > 20000
        if (tiempo // 500) % 2 == 0:
            self.img = self.sprite_triste_abierto if triste else self.sprite_abierto
        else:
            self.img = self.sprite_triste_cerrado if triste else self.sprite_cerrado

    def dibujar(self):
        screen.blit(self.img, (self.x * cell_size, self.y * cell_size))

    def reiniciar_posicion(self):
        self.x, self.y = 1, 1
        self.direccion = (0, 0)

# Fantasma
class Fantasma:
    def __init__(self, x, y, color, tipo):
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.color = color
        self.tipo = tipo
        self.direccion_actual = (0, 0)
        self.vulnerable = False
        self.img = pygame.Surface((cell_size, cell_size))
        self.img.fill(self.color)
        self.last_move_time = 0

    def mover(self, pacman):
        ahora = pygame.time.get_ticks()
        if ahora - self.last_move_time < 150:
            return
        self.last_move_time = ahora

        opciones = self.opciones_movimiento()

        if self.vulnerable:
            opciones.sort(key=lambda d: self.distancia(pacman, d[0], d[1]), reverse=True)
        elif self.tipo == "Blinky":
            opciones.sort(key=lambda d: self.distancia(pacman, d[0], d[1]))
        else:
            random.shuffle(opciones)

        if opciones:
            nuevo_x, nuevo_y = opciones[0]
            self.direccion_actual = (nuevo_x - self.x, nuevo_y - self.y)
            self.x, self.y = nuevo_x % len(tablero[0]), nuevo_y % len(tablero)

    def opciones_movimiento(self):
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        posibles = []
        for dx, dy in direcciones:
            nx, ny = self.x + dx, self.y + dy
            if not hay_pared(nx, ny) and (dx, dy) != (-self.direccion_actual[0], -self.direccion_actual[1]):
                posibles.append((nx, ny))
        return posibles

    def distancia(self, pacman, x, y):
        return abs(pacman.x - x) + abs(pacman.y - y)

    def dibujar(self):
        self.img.fill(AZUL_CLARO if self.vulnerable else self.color)
        screen.blit(self.img, (self.x * cell_size, self.y * cell_size))

    def reiniciar_posicion(self):
        self.x, self.y = self.spawn_x, self.spawn_y
        self.direccion_actual = (0, 0)

# Main loop
def main():
    global fantasmas_vulnerables, vulnerable_start_time

    pacman = Pacman()
    fantasmas = [
        Fantasma(13, 11, ROJO, "Blinky"),
        Fantasma(15, 5, ROSADO, "Pinky"),
        Fantasma(7, 7, CIAN, "Inky"),
        Fantasma(5, 13, NARANJA, "Clyde")
    ]

    vidas = 3
    start_time = pygame.time.get_ticks()
    fantasmas_vulnerables = False
    vulnerable_start_time = 0
    puntaje_maximo = sum(row.count(".") for row in tablero) + sum(row.count("o") * 10 for row in tablero)

    run = True
    while run:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        tiempo = pygame.time.get_ticks() - start_time

        pacman.mover(keys)
        pacman.comer()
        pacman.actualizar_sprite(tiempo)

        if fantasmas_vulnerables and pygame.time.get_ticks() - vulnerable_start_time > 5000:
            fantasmas_vulnerables = False

        for f in fantasmas:
            f.vulnerable = fantasmas_vulnerables
            f.mover(pacman)

        for f in fantasmas:
            if pacman.x == f.x and pacman.y == f.y:
                if f.vulnerable:
                    f.reiniciar_posicion()
                    pacman.score += 50
                else:
                    vidas -= 1
                    if vidas <= 0:
                        game_over(pacman.score)
                        return
                    pacman.reiniciar_posicion()
                    for g in fantasmas:
                        g.reiniciar_posicion()
                    break

        screen.fill(NEGRO)
        draw_board()
        pacman.dibujar()
        for f in fantasmas:
            f.dibujar()

        screen.blit(font.render(f'Score: {pacman.score}', True, BLANCO), (10, 10))
        draw_lives(vidas)

        if all(cell not in (".", "o") for row in tablero for cell in row):
            game_win(pacman.score)
            return

        pygame.display.flip()

    pygame.quit()

main()
