import sys, random
import pygame as pg


class Ultimata:
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

        # message handling variables next
        self.font = pg.font.SysFont(None, 8, False, False)
        self.message_handler = MessageHandler(0, self.gridY * self.cell_size,
                                              (self.gridX + 5) * self.cell_size, (self.gridX + 5) * self.cell_size,
                                              self.screen, self.font)

    def create_cells(self):
        for x in range(self.gridX):
            for y in range(self.gridY):
                self.cells[(x, y)] = Cell(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size,
                                          self.screen)

    def main_loop(self):
        while True:
            self.event_processor()
            # self.process_cells()
            # self.process_stats()
            # self.process_messages()
            # self.process_characters()
            # self.process_player()
            self.screen_updater()

    def event_processor(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def screen_updater(self):
        self.cell_updater()
        # self.draw_stats()
        self.message_handler.draw()
        # self.draw_characters()
        # self.draw_player()
        pg.display.flip()

    def cell_updater(self):
        for cell in self.cells.values():
            cell.draw()


class Cell:
    def __init__(self, x, y, w, h, screen):
        self.screen = screen
        self.rect = pg.Rect(x, y, w, h)
        self.color = random.choice([(0, 0, 200), (0, 200, 0), (200, 0, 0)])

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

class MessageHandler:
    def __init__(self, x, y, w, h, screen, font):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.screen = screen
        self.message_rect = pg.Rect(x, y, w, h)
        self.color = (20, 80, 80)
        self.title = "Message Box"
        self.title_img = img = font.render('Message Box', True, (250, 205, 200))

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.message_rect)

a = Ultimata((1184, 672))
a.main_loop()
