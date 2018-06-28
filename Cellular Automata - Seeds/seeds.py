import pyglet
from random import random

WIDTH = 600
HEIGHT = 600

class Seeds:
    def __init__(self, size, alive):
        self.rows = WIDTH // size
        self.cols = HEIGHT // size
        self.alive = alive
        self.size = size
        self.cells = []

        self.generate()

    def generate(self):
        for row in range(0, self.rows):
            self.cells.append([])
            for col in range(0, self.cols):
                if random() < self.alive:
                    self.cells[row].append(1)
                else:
                    self.cells[row].append(0)

    def run_rules(self):
        temp_grid = [[0 for i in range(0, self.rows)] for j in range(0, self.cols)]
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                if self.cells[row][col] == 0 and self.get_neighbors(row, col) == 2:
                    temp_grid[row][col] = 1
                else:
                    temp_grid[row][col] = 0
        self.cells = temp_grid

    def get_neighbors(self, r, c):
        neighbors = 0
        row_config = (-1, 0, 1, -1, 1, -1, 0, 1)
        col_config = (-1, -1, -1, 0, 0, 1, 1, 1)
        for i in range(0, 8):
            if r + row_config[i] < 0 or r + row_config[i] > self.rows - 1 or c + col_config[i] < 0 or c + col_config[i] > self.cols - 1:
                pass
            elif self.cells[r + row_config[i]][c + col_config[i]] == 1:
                neighbors += 1
        return neighbors

    def show(self):
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                color = (0, 0, 0, 255)
                if self.cells[row][col] == 1:
                    color = (255, 255, 255, 255)
                self.rect((row * self.size, col * self.size), self.size, self.size, color)

    def rect(self, pos, width, height, color):
        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, 
            ("v2f", (pos[0], pos[1], pos[0], pos[1] + height, pos[0] + width, pos[1], pos[0] + width, pos[1] + height)),
            ("c4B", tuple(color[i] for i in range(0, 4)) * 4))

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Cellular Automata - Seeds")

        pyglet.clock.schedule_interval(self.update, 1 / 10)

        self.seeds = Seeds(12, 0.2)

    def on_draw(self):
        self.clear()

        pyglet.gl.glClearColor(1, 1, 1, 1)

        self.seeds.show()
        self.seeds.run_rules()
        # print(self.seeds.get_neighbors(0, 0))

    def update(self, dt):
        pass

window = MainWindow()
pyglet.app.run()