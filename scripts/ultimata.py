import sys
import random
import os
import pygame as pg

cells = {}
tileset = {}
tileinfo = {0: ("wall", "no pass"), 1: ("wall", "no pass"), 2: ("wall", "no pass"), 3: ("wall", "no pass"),
            4: ("floor", "pass"), 5: ("floor", "pass"), 6: ("water", "no pass"), 7: ("floor", "pass"),
            8: ("floor", "pass"), 9: ("floor", "pass"), 10: ("wall", "no pass"), 11: ("floor", "pass")}
levels = {0: ([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
               0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0,
               0, 4, 4, 4, 4, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0,
               0, 4, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0,
               0, 4, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0,
               0, 0, 0, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 4, 0, 0, 4, 0, 0, 0,
               4, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 0, 4, 4, 4, 4, 0, 4, 0, 4, 4,
               4, 4, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0, 4, 4, 0, 0, 0, 4, 0, 0, 0,
               4, 4, 0, 4, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0, 4, 4, 4, 0, 4, 4, 0, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0,
               4, 4, 0, 4, 0, 4, 4, 4, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0,
               4, 0, 0, 4, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0,
               4, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0,
               4, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0,
               4, 0, 4, 4, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0,
               4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4], (1, 2))}


class Tile:

    def __init__(self, image):
        self.image = image


class Ultimata:
    def __init__(self, screen_size=(1184, 672)):  # screen_size is tuple (dimensions for main game screen)
        global levels
        pg.init()
        self.screen_size = screen_size
        self.screen = pg.display.set_mode(self.screen_size)
        self.title = "Ultimata"
        pg.display.set_caption(self.title)
        self.load_tiles()
        self.current_level = 0
        self.gridX = 32
        self.gridY = 16
        self.cell_size = 32
        self.cell_count = self.gridX * self.gridY
        self.create_cells()
        self.player = Player(self.screen, self.cell_size, self.gridX, self.gridY, levels[self.current_level][1])
        self.message_handler = MessageHandler(0, self.gridY * self.cell_size,
                                              (self.gridX + 5) * self.cell_size, (self.gridX + 5) * self.cell_size,
                                              self.screen)
        # messages can be added from anywhere in app by self.message_handler.queue.append(("text", "system"))
        self.message_handler.queue.append(("Messages Handler initialized...", "system"))
        self.stats_handler = StatsHandler(self.cell_size * self.gridX, 0, 5 * self.cell_size,
                                          self.gridY * self.cell_size,
                                          self.screen)

    def load_tiles(self):
        global tileset
        counter = 0
        for filename in os.listdir('tiles'):
            img = pg.image.load(os.path.join("tiles", filename)).convert()
            tileset[counter] = Tile(img)
            counter += 1

    def create_cells(self):
        global levels, cells
        counter = 0
        limit = len(levels[self.current_level][0])
        for y in range(self.gridY):
            for x in range(self.gridX):
                if counter >= limit:
                    counter = 0
                tile = levels[self.current_level][0][counter]
                cells[(x, y)] = Cell(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size,
                                     self.screen, tile)
                counter += 1

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
                if event.key == pg.K_w:
                    self.player.direction = "up"
                if event.key == pg.K_s:
                    self.player.direction = "down"
                if event.key == pg.K_a:
                    self.player.direction = "right"
                if event.key == pg.K_d:
                    self.player.direction = "left"

    def screen_updater(self):
        self.cell_updater()
        self.stats_updater()
        self.message_updater()
        self.player.draw()
        pg.display.flip()

    def stats_updater(self):
        self.stats_handler.hp = self.player.hp
        self.stats_handler.draw()

    def message_updater(self):
        for message in self.player.messages:
            self.message_handler.update_queue(message)
        self.player.messages = []
        self.message_handler.draw()

    def cell_updater(self):
        global cells
        for cell in cells.values():
            cell.draw()


class Cell:
    def __init__(self, x, y, w, h, screen, tile):
        global tileset, tileinfo
        self.screen = screen
        self.rect = pg.Rect(x, y, w, h)
        self.tile = tileset[tile]
        self.tile_type = tileinfo[tile]

    def draw(self):
        self.screen.blit(self.tile.image, self.rect)


class Player:
    def __init__(self, surface, cell_size, gridX, gridY, start):
        self.pos = start
        self.color = (100, 0, 100)
        self.direction = ""
        self.surface = surface
        self.cell_size = cell_size
        self.offset = int(self.cell_size / 2)
        self.radius = int(self.cell_size * 0.3)
        self.gridX = gridX - 1
        self.gridY = gridY - 1
        # player can post message anytime by appending tuple to self.messages list ("text", "player")
        self.messages = [("Player initialized...", "system")]
        self.hp = 100

    def move(self, direction):
        global cells, messages
        if direction == "down":
            if self.pos[1] != self.gridY and cells[(self.pos[0], self.pos[1] + 1)].tile_type[1] == "pass":
                self.pos = (self.pos[0], self.pos[1] + 1)
                self.messages.append(("Down", "player"))
        if direction == "up":
            if self.pos[1] != 0 and cells[(self.pos[0], self.pos[1] - 1)].tile_type[1] == "pass":
                self.pos = (self.pos[0], self.pos[1] - 1)
                self.messages.append(("Up", "player"))
        if direction == "right":
            if self.pos[0] != self.gridX and cells[(self.pos[0] + 1, self.pos[1])].tile_type[1] == "pass":
                self.pos = (self.pos[0] + 1, self.pos[1])
                self.messages.append(("Right", "player"))
        if direction == "left":
            if self.pos[0] != 0 and cells[(self.pos[0] - 1, self.pos[1])].tile_type[1] == "pass":
                self.pos = (self.pos[0] - 1, self.pos[1])
                self.messages.append(("Left", "player"))

    def draw(self):
        pixel_pos = (self.pos[0] * self.cell_size + self.offset, self.pos[1] * self.cell_size + self.offset)
        pg.draw.circle(self.surface, self.color, pixel_pos, self.radius, 0)


class MessageHandler:  # for displaying messages at bottom of screen
    def __init__(self, x, y, w, h, screen):
        # establish the subscreen message box on which we'll write messages
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.screen = screen
        self.message_rect = pg.Rect(x, y, w, h)
        self.color = (20, 20, 80)
        self.queue = []
        # establish fonts for different kinds of messages
        self.xPad = 32
        self.yPad = 16
        self.system_font = pg.font.SysFont('arial', 16)
        self.player_message = pg.font.SysFont('verdana', 14)
        self.p_color = (255, 255, 255)
        self.s_color = (255, 50, 50)
        self.system_message = pg.font.SysFont('verdana', 14, italic=True)
        self.title = "MESSAGE HISTORY"
        self.title_img = self.system_font.render(self.title, True, (255, 255, 255))

    def update_queue(self, message):
        message_text, message_type = message
        if len(self.queue) > 5:
            self.queue.pop(0)
        self.queue.append((message_text, message_type))

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.message_rect)
        # blit the message title
        self.screen.blit(self.title_img, (self.x + self.xPad, self.y + self.yPad))
        # now loop through and blit everything in message q
        counter = 1
        for message in self.queue:
            message_text, message_type = message
            if message_type == "player":
                m = self.player_message.render(message_text, True, self.p_color)
            elif message_type == "system":
                m = self.system_message.render(message_text, True, self.s_color)
            else:
                m = self.system_font.render("MESSAGE TYPE NOT FOUND", True, self.s_color)
            self.screen.blit(m, (self.x + self.xPad, (self.y + 22) + (counter * self.yPad)))
            counter += 1


class StatsHandler:  # for displaying messages at right of screen
    def __init__(self, x, y, w, h, screen):
        # establish the subscreen message box on which we'll write messages
        self.x = x
        self.y = y
        self.xPad = 8
        self.yPad = 16
        self.width = w
        self.height = h
        self.screen = screen
        self.stats_rect = pg.Rect(x, y, w, h)
        self.color = (200, 255, 255)
        self.stats_title = pg.font.SysFont('arial', 16)
        self.stats_font = pg.font.SysFont('verdana', 14)
        self.title_color = (0, 0, 25)
        self.stats_color = (0, 0, 0)
        self.title = "GAME STATE:"
        self.title_img = self.stats_title.render(self.title, True, self.title_color)
        # include various stats for updating below
        self.hp = 0

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.stats_rect)
        self.screen.blit(self.title_img, (self.x + self.xPad, self.y + self.yPad))
        hp_img = self.stats_font.render("Hit Point: " + str(self.hp), True, self.stats_color)
        self.screen.blit(hp_img, (self.x + self.xPad, self.y + (3 * self.yPad)))


a = Ultimata((1184, 672))
a.main_loop()
