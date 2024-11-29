import pyxel
import random

TILE_SIZE = 8
# 1 - це стіни, 2 - це звичайні кульки, 3 - це покращені кульки. покращені дають додаткові очки і можливість стопнути привида
# мабуть є кращій спосіб малювати лабіринт, але так наглядно видно, що буде, як гра запуститься
INITIAL_MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
MAZE = [row[:] for row in INITIAL_MAZE]
# чим менше значення швидкості - тим швидший рух
SPEED = 5
# час на скільки стопаються привиди
GHOST_STOP_TIME = 100
SCREEN_WIDTH = len(MAZE[0]) * TILE_SIZE
SCREEN_HEIGHT = len(MAZE) * TILE_SIZE
# всі кольори є тут - https://github.com/kitao/pyxel/blob/main/docs/images/05_color_palette.png
COLORS = {
    "pacman": 10,
    "wall": 1,
    "pellet": 7,
    "ghost": 8,
    "empty": 0,
    "win": 9,
    "lose": 3,
}

class PacMan:
    def __init__(self, x, y):
        self.x = x + TILE_SIZE // 2
        self.y = y + TILE_SIZE // 2
        self.direction = "STOP"
        self.buffered_direction = None
        self.total_pellets = 0
        self.score = 0
        self.lives = 3
        self.powered_up = False
        self.power_timer = 0
        self.move_counter = 0

    def update(self, ghosts):
        self.move_counter += 1
        if self.move_counter < SPEED:
            return

        self.move_counter = 0

        grid_x = self.x // TILE_SIZE
        grid_y = self.y // TILE_SIZE

        for ghost in ghosts:
            ghost_x = ghost.x // TILE_SIZE
            ghost_y = ghost.y // TILE_SIZE

            if grid_x == ghost_x and grid_y == ghost_y:
                if self.powered_up:
                    self.score += 200
                    ghost.waiting = True
                else:
                    self.lives -= 1
                    self.x, self.y = TILE_SIZE + TILE_SIZE // 2, TILE_SIZE + TILE_SIZE // 2
                    self.direction = "STOP"
                    self.buffered_direction = None

        aligned_x = self.x % TILE_SIZE == TILE_SIZE // 2
        aligned_y = self.y % TILE_SIZE == TILE_SIZE // 2

        if aligned_x and aligned_y and self.buffered_direction:
            next_tile_x, next_tile_y = grid_x, grid_y
            if self.buffered_direction == "UP":
                next_tile_y -= 1
            elif self.buffered_direction == "DOWN":
                next_tile_y += 1
            elif self.buffered_direction == "LEFT":
                next_tile_x -= 1
            elif self.buffered_direction == "RIGHT":
                next_tile_x += 1

            if MAZE[next_tile_y][next_tile_x] != 1:
                self.direction = self.buffered_direction
            self.buffered_direction = None

        if self.direction == "UP" and aligned_x:
            if MAZE[grid_y - 1][grid_x] != 1:
                self.y -= TILE_SIZE
        elif self.direction == "DOWN" and aligned_x:
            if MAZE[grid_y + 1][grid_x] != 1:
                self.y += TILE_SIZE
        elif self.direction == "LEFT" and aligned_y:
            if MAZE[grid_y][grid_x - 1] != 1:
                self.x -= TILE_SIZE
        elif self.direction == "RIGHT" and aligned_y:
            if MAZE[grid_y][grid_x + 1] != 1:
                self.x += TILE_SIZE

        grid_x = self.x // TILE_SIZE
        grid_y = self.y // TILE_SIZE

        cell = MAZE[grid_y][grid_x]
        if cell == 2:
            self.score += 10
        elif cell == 3:
            self.score += 50
            self.powered_up = True
            self.power_timer = 20

        if cell == 2 or cell == 3:
            MAZE[grid_y][grid_x] = 0
            self.total_pellets -= 1

        if self.powered_up:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.powered_up = False

    def draw(self):
        pyxel.circ(self.x, self.y, TILE_SIZE // 2, COLORS["pacman"])

        # це типу емуляція рота пакмана
        if self.direction == "UP":
            pyxel.tri(
                self.x, self.y,
                self.x - TILE_SIZE // 4, self.y - TILE_SIZE // 2,
                self.x + TILE_SIZE // 4, self.y - TILE_SIZE // 2,
                COLORS["empty"]
            )
        elif self.direction == "DOWN":
            pyxel.tri(
                self.x, self.y,
                self.x - TILE_SIZE // 4, self.y + TILE_SIZE // 2,
                self.x + TILE_SIZE // 4, self.y + TILE_SIZE // 2,
                COLORS["empty"]
            )
        elif self.direction == "LEFT":
            pyxel.tri(
                self.x, self.y,
                self.x - TILE_SIZE // 2, self.y - TILE_SIZE // 4,
                self.x - TILE_SIZE // 2, self.y + TILE_SIZE // 4,
                COLORS["empty"]
            )
        elif self.direction == "RIGHT":
            pyxel.tri(
                self.x, self.y,
                self.x + TILE_SIZE // 2, self.y - TILE_SIZE // 4,
                self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 4,
                COLORS["empty"]
            )

class Ghost:
    def __init__(self, x, y):
        self.x = x + TILE_SIZE // 2
        self.y = y + TILE_SIZE // 2
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.move_counter = 0
        self.waiting = False
        self.waiting_counter = 0

    def update(self, pacman):
        if self.waiting:
            self.waiting_counter += 1

            if self.waiting_counter >= GHOST_STOP_TIME:
                self.waiting_counter = 0
                self.waiting = False
                self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            else:
                return

        self.move_counter += 1
        if self.move_counter < SPEED:
            return

        self.move_counter = 0

        new_x, new_y = self.x, self.y
        if self.direction == "UP":
            new_y -= TILE_SIZE
        elif self.direction == "DOWN":
            new_y += TILE_SIZE
        elif self.direction == "LEFT":
            new_x -= TILE_SIZE
        elif self.direction == "RIGHT":
            new_x += TILE_SIZE

        if MAZE[new_y // TILE_SIZE][new_x // TILE_SIZE] == 1:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        else:
            self.x, self.y = new_x, new_y

    def draw(self, pacman):
        # в залежності від того чи привид у звичайному стані, стоїть чи коли пакман підсилений - у привида різні кольори
        ghost_color = COLORS["ghost"]
        if self.waiting:
            ghost_color = 13
        elif pacman.powered_up:
            ghost_color = 6

        pyxel.circ(self.x, self.y, TILE_SIZE // 2, ghost_color)
        eye_offset = TILE_SIZE // 4

        pyxel.pset(self.x - eye_offset, self.y - eye_offset, COLORS["empty"])
        pyxel.pset(self.x + eye_offset, self.y - eye_offset, COLORS["empty"])

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.window_title = "Pac-Man"
        self.game_over = False
        self.win = False
        self.pacman = None
        self.ghosts = None
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def count_pellets(self):
        return sum(row.count(2) + row.count(3) for row in INITIAL_MAZE)

    def reset_game(self):
        global MAZE
        MAZE = [row[:] for row in INITIAL_MAZE]
        self.pacman = PacMan(TILE_SIZE, TILE_SIZE)
        self.ghosts = [
            Ghost(TILE_SIZE * 6, TILE_SIZE * 4),
            Ghost(TILE_SIZE * 12, TILE_SIZE * 14),
            Ghost(TILE_SIZE * 18, TILE_SIZE * 18)
        ]
        self.pacman.total_pellets = self.count_pellets()
        self.game_over = False
        self.win = False

    def update(self):
        if self.pacman.lives < 1:
            self.game_over = True

        if self.pacman.total_pellets < 1:
            self.win = True

        # при виграші чи програші настискання на пробіл перезапускає гру
        if self.game_over or self.win:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                return

        if pyxel.btn(pyxel.KEY_UP):
            self.pacman.buffered_direction = "UP"
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.pacman.buffered_direction = "DOWN"
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.pacman.buffered_direction = "LEFT"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.pacman.buffered_direction = "RIGHT"

        self.pacman.update(self.ghosts)
        for ghost in self.ghosts:
            ghost.update(self.pacman)

    def draw_maze(self):
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE
                if cell == 1:
                    pyxel.rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE, COLORS["wall"])
                elif cell == 2:
                    pyxel.pset(tile_x + TILE_SIZE // 2, tile_y + TILE_SIZE // 2, COLORS["pellet"])
                elif cell == 3:
                    pyxel.circ(tile_x + TILE_SIZE // 2, tile_y + TILE_SIZE // 2, 2, COLORS["pellet"])

    def draw(self):
        if self.game_over:
            pyxel.cls(COLORS["lose"])
            game_over_text = "GAME OVER"
            restart_text = "PRESS <<SPACE>> TO RESTART"
            pyxel.text((SCREEN_WIDTH - len(game_over_text) * 4) // 2, (SCREEN_HEIGHT - 6) // 2, game_over_text, 7)
            pyxel.text((SCREEN_WIDTH - len(restart_text) * 4) // 2, (SCREEN_HEIGHT + 12) // 2, restart_text, 7)
            return

        if self.win:
            pyxel.cls(COLORS["win"])
            game_over_text = "YOU WON"
            restart_text = "PRESS <<SPACE>> TO RESTART"
            pyxel.text((SCREEN_WIDTH - len(game_over_text) * 4) // 2, (SCREEN_HEIGHT - 6) // 2, game_over_text, 7)
            pyxel.text((SCREEN_WIDTH - len(restart_text) * 4) // 2, (SCREEN_HEIGHT + 12) // 2, restart_text, 7)
            return

        pyxel.cls(COLORS["empty"])

        self.draw_maze()
        self.pacman.draw()
        for ghost in self.ghosts:
            ghost.draw(self.pacman)

        pyxel.text(10, SCREEN_HEIGHT - 7, f"Score: {self.pacman.score}", 7)
        pyxel.text(60, SCREEN_HEIGHT - 7, f"Lives: {self.pacman.lives}", 7)

Game()
