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
        self.player = Player(self.screen, self.cell_size, self.gridX, self.gridY)
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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.player.move("down")
                if event.key == pg.K_UP:
                    self.player.move("up")
                if event.key == pg.K_RIGHT:
                    self.player.move("right")
                if event.key == pg.K_LEFT:
                    self.player.move("left")

    def screen_updater(self):
        self.cell_updater()
        # self.draw_stats()
        # self.draw_messages()
        # self.draw_characters()
        self.player.draw()
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


class Player:
    def __init__(self, surface, cell_size, gridX, gridY):
        self.pos = (0, 0)
        self.color = (100, 0, 100)
        self.surface = surface
        self.cell_size = cell_size
        self.offset = int(self.cell_size / 2)
        self.radius = int(self.cell_size * 0.3)
        self.gridX = gridX - 1
        self.gridY = gridY - 1

    def move(self, direction):
        if direction == "down":
            if self.pos[1] != self.gridY:
                self.pos = (self.pos[0], self.pos[1] + 1)
        if direction == "up":
            if self.pos[1] != 0:
                self.pos = (self.pos[0], self.pos[1] - 1)
        if direction == "right":
            if self.pos[0] != self.gridX:
                self.pos = (self.pos[0] + 1, self.pos[1])
        if direction == "left":
            if self.pos[0] != 0:
                self.pos = (self.pos[0] - 1, self.pos[1])

class MessageHandler: # for displaying messages at bottom of screen
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
        pixel_pos = (self.pos[0] * self.cell_size + self.offset, self.pos[1] * self.cell_size + self.offset)
        pg.draw.circle(self.surface, self.color, pixel_pos, self.radius, 0)


a = Ultimata((1184, 672))
a.main_loop()
