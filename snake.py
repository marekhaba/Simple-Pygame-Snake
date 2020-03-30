import pygame
from snake_base import SnakeHead, spawn_fruit
import pygamegui as pg

TILE_SIZE = 20
TILE_AMOUNT = 40
WINDOW_SIZE = (TILE_SIZE*TILE_AMOUNT, TILE_SIZE*TILE_AMOUNT)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.grid = [['0' for x in range(TILE_AMOUNT)] for y in range(TILE_AMOUNT)] 
        self.snake = SnakeHead(self.grid, 20, 20)
        self.clock = pygame.time.Clock()#Controls framerate

        self.COLORS = {
            "bg": (10, 10, 10),
            "f": (155, 0, 0)
        }

        spawn_fruit(self.grid)

    def draw(self):
        self.screen.fill(self.COLORS["bg"])
        for y in range(TILE_AMOUNT):
            for x in range(TILE_AMOUNT):
                tile = self.grid[x][y]
                if tile == self.snake.name:
                    pygame.draw.rect(self.screen, self.snake.color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if tile == "f":
                    pygame.draw.rect(self.screen, self.COLORS["f"], (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                


    def check_events(self):
        events = pygame.event.get()
        _return = "self"
        _moved = False
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and _moved is False:
                if event.key == pygame.K_w:
                    self.snake.change_dir("up")
                    _moved = True
                if event.key == pygame.K_s:
                    self.snake.change_dir("down")
                    _moved = True
                if event.key == pygame.K_d:
                    self.snake.change_dir("right")
                    _moved = True
                if event.key == pygame.K_a:
                    self.snake.change_dir("left")
                    _moved = True
        return _return

    def update(self):
        result = self.check_events()
        result_move = self.snake.move()
        #print(self.snake.x, self.snake.y)
        self.draw()
        pygame.display.update()
        self.clock.tick(10)
        if result_move != "self":
            return result_move
        return result

def start():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Snake')

    snake_theme = pg.Theme(text_color=(0, 155, 0))
    start_menu = pg.Menu(screen, snake_theme, (10, 10, 10))
    pg.Label(start_menu, 400, 150, "Snake", text_size=75)
    pg.Button(start_menu, 300, 500, 200, 100, "start", text="Start")

    end_menu = pg.Menu(screen, snake_theme, (10, 10, 10))
    pg.Label(end_menu, 400, 300, "Game Over", text_size=75)
    pg.Button(end_menu, 300, 600, 200, 100, "start", text="Restart")
    end_score = pg.Label(end_menu, 400, 450, "Score: ")

    active_screen = start_menu
    done = False
    while not done:
        result = active_screen.update()
        if result == "start":
            active_screen = Game(screen)
        elif result == 'quit':
            done = True
        elif result.isnumeric():
            end_score.change_text(f"Score: {result}", True)
            active_screen = end_menu
    pygame.quit()

if __name__ == "__main__":
    start()