import sys, random
import pygame as pg


class ultimata:
    def __init__(self, screen_size=(1184, 672)):  # screen_size is tuple (dimensions for main game screen)
        pg.init()
        self.screen_size = screen_size
        self.screen = pg.display.set_mode(self.screen_size)
        print(self.screen.get_size())
        self.title = "Ultimata"
        pg.display.set_caption(self.title)
        self.gridX = 32
        self.gridY = 16
        self.cell_size = 32
        self.cell_count = self.gridX * self.gridY
        self.cells = {}
        self.create_cells()

    def create_cells(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                self.cells[(x, y)] = cell(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size,
                                          self.screen)

    def main_loop(self):
        while True:
            self.event_processor()
            self.screen_updater()

    def event_processor(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def screen_updater(self):
        self.cell_updater()
        pg.display.flip()

    def cell_updater(self):
        for cell in self.cells.values():
            cell.draw()


class cell:
    def __init__(self, x, y, w, h, screen):
        self.screen = screen
        self.rect = pg.Rect(x, y, w, h)
        self.color = random.choice([(0, 0, 200), (0, 200, 0), (200, 0, 0)])

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


a = ultimata((1184, 672)) # added this comment
a.main_loop()
print("hi")
