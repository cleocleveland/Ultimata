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
        self.monsters = []
        self.speed = 60
        self.action_taken = False
        self.fired = False
        self.arrows = []
        self.player = Player(self.screen, self.cell_size, self.gridX, self.gridY, levels[self.current_level][1])
        self.message_handler = MessageHandler(0, self.gridY * self.cell_size,
                                              (self.gridX + 5) * self.cell_size, (self.gridX + 5) * self.cell_size,
                                              self.screen)
        # messages can be added from anywhere in-app by self.message_handler.queue.append(("text", "system"))
        self.message_handler.queue.append(("Messages Handler initialized...", "system"))
        self.stats_handler = StatsHandler(self.cell_size * self.gridX, 0, 5 * self.cell_size,
                                          self.gridY * self.cell_size,
                                          self.screen)
        self.message_handler.queue.append(("Game State initialized...", "system"))
        self.create_monster((3, 3))
        self.create_monster((19, 11))
        self.create_monster((28, 3))
        self.clock = pg.time.Clock()

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
            self.clock.tick()

    def event_processor(self):
        self.action_taken = False
        self.fired = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.player.move("down", self.get_pos())
                    self.action_taken = True
                if event.key == pg.K_UP:
                    self.player.move("up", self.get_pos())
                    self.action_taken = True
                if event.key == pg.K_RIGHT:
                    self.player.move("right", self.get_pos())
                    self.action_taken = True
                if event.key == pg.K_LEFT:
                    self.player.move("left", self.get_pos())
                    self.action_taken = True
                if event.key == pg.K_w:
                    self.player.direction = "up"
                if event.key == pg.K_s:
                    self.player.direction = "down"
                if event.key == pg.K_a:
                    self.player.direction = "left"
                if event.key == pg.K_d:
                    self.player.direction = "right"
                if event.key == pg.K_f:
                    self.player_fires()
                    self.fired = True
                if event.key == pg.K_MINUS:
                    self.speed -= 3
                if event.key == pg.K_EQUALS:
                    self.speed += 3

        if self.action_taken:
            for monster in self.monsters:
                monster.go(self.get_pos())
        if self.action_taken or self.fired:
            self.monsters_fire()

    def player_fires(self):
        arrow = Fire(self.player.pixel_pos, self.player.direction, self.screen, self.speed, self.player)
        self.arrows.append(arrow)

    def update_arrows(self):
        dead = []
        for arrow in self.arrows:
            arrow.move(self.clock.get_fps())
            arrow.check(self.monsters, self.cell_size, self.player)
            if arrow.status == False:
                dead.append(arrow)
            arrow.draw()
        for arrow in dead:
            self.arrows.pop(self.arrows.index(arrow))

    def screen_updater(self):
        self.cell_updater()
        self.stats_updater()
        self.message_updater()
        self.player.draw()
        self.monster_updater()
        self.update_arrows()
        pg.display.flip()

    def stats_updater(self):
        self.stats_handler.hp = self.player.hp
        self.stats_handler.direction = self.player.direction
        self.stats_handler.monster_count = len(self.monsters)
        self.stats_handler.draw()

    def monster_updater(self):
        dead = []
        for monster in self.monsters:
            monster.draw()
            if monster.hp == 0:
                dead.append(monster)
        for monster in dead:
            self.monsters.pop(self.monsters.index(monster))

    def message_updater(self):
        for message in self.player.messages:
            self.message_handler.update_queue(message)
        self.player.messages = []
        self.message_handler.draw()

    def cell_updater(self):
        global cells
        for cell in cells.values():
            cell.draw()

    def create_monster(self, spawn):
        self.monsters.append(Monster(self.screen, self.cell_size, self.gridX, self.gridY, spawn))

    def get_pos(self):
        pos = [self.player.pos]
        for monster in self.monsters:
            pos.append(monster.pos)
        return(pos)

    def monsters_fire(self):
        for monster in self.monsters:
            if random.randint(1, 3) == 1:
                arrow = Fire(monster.pixel_pos, random.choice(["up", "down", "left", "right"]), self.screen,
                             self.speed, monster)
                self.arrows.append(arrow)


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
        self.pixel_pos = ()
        self.pos = start
        self.color = (0, 0, 200)
        self.direction = "right"
        self.surface = surface
        self.cell_size = cell_size
        self.offset = int(self.cell_size / 2)
        self.radius = int(self.cell_size * 0.3)
        self.gridX = gridX - 1
        self.gridY = gridY - 1
        self.messages = [("Initialising system...", "player")]
        self.hp = 5
        self.messages = [("Player initialized...", "system"), ("Ready to move...", "player")]

    def move(self, direction, lis):
        global cells
        if direction == "down":
            if self.pos[1] != self.gridY and cells[(self.pos[0], self.pos[1] + 1)].tile_type[1] == "pass" and (self.pos[0], self.pos[1] + 1) not in lis:
                self.pos = (self.pos[0], self.pos[1] + 1)
                self.messages.append(("Down", "player"))
        if direction == "up":
            if self.pos[1] != 0 and cells[(self.pos[0], self.pos[1] - 1)].tile_type[1] == "pass" and (self.pos[0], self.pos[1] - 1) not in lis:
                self.pos = (self.pos[0], self.pos[1] - 1)
                self.messages.append(("Up", "player"))
        if direction == "right":
            if self.pos[0] != self.gridX and cells[(self.pos[0] + 1, self.pos[1])].tile_type[1] == "pass" and (self.pos[0] + 1, self.pos[1]) not in lis:
                self.pos = (self.pos[0] + 1, self.pos[1])
                self.messages.append(("Right", "player"))
        if direction == "left":
            if self.pos[0] != 0 and cells[(self.pos[0] - 1, self.pos[1])].tile_type[1] == "pass" and (self.pos[0] - 1, self.pos[1]) not in lis:
                self.pos = (self.pos[0] - 1, self.pos[1])
                self.messages.append(("Left", "player"))

    def draw(self):
        self.pixel_pos = (self.pos[0] * self.cell_size + self.offset, self.pos[1] * self.cell_size + self.offset)
        pg.draw.circle(self.surface, self.color, self.pixel_pos, self.radius, 0)


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
        self.direction = "Test"
        self.monster_count = 0

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.stats_rect)
        self.screen.blit(self.title_img, (self.x + self.xPad, self.y + self.yPad))
        hp_img = self.stats_font.render("Hit Point: " + str(self.hp), True, self.stats_color)
        self.screen.blit(hp_img, (self.x + self.xPad, self.y + (3 * self.yPad)))
        direction_img = self.stats_font.render("Direction: " + self.direction, True, self.stats_color)
        self.screen.blit(direction_img, (self.x + self.xPad, self.y + (5 * self.yPad)))
        monster_img = self.stats_font.render("Monsters: " + str(self.monster_count), True, self.stats_color)
        self.screen.blit(monster_img, (self.x + self.xPad, self.y + (6.5 * self.yPad)))


class Monster:
    def __init__(self, surface, cell_size, gridX, gridY, start):
        self.pos = start
        self.pixel_pos = ()
        self.color = (0, 200, 200)
        self.direction = ""
        self.surface = surface
        self.cell_size = cell_size
        self.offset = int(self.cell_size / 2)
        self.radius = int(self.cell_size * 0.3)
        self.gridX = gridX - 1
        self.gridY = gridY - 1
        # player can post message anytime by appending tuple to self.messages list ("text", "player")
        self.messages = [("Player initialized...", "system")]
        self.hp = 3

    def go(self, lis):
        answer = self.move(random.choice(["up", "down", "left", "right"]), lis)
        while answer == "nope":
            answer = self.move(random.choice(["up", "down", "left", "right"]), lis)

    def move(self, direction, lis):
        global cells
        if direction == "down":
            if self.pos[1] != self.gridY and cells[(self.pos[0], self.pos[1] + 1)].tile_type[1] == "pass" and (self.pos[0], self.pos[1] + 1) not in lis:
                self.pos = (self.pos[0], self.pos[1] + 1)
            else:
                return("nope")
        if direction == "up":
            if self.pos[1] != 0 and cells[(self.pos[0], self.pos[1] - 1)].tile_type[1] == "pass" and (self.pos[0], self.pos[1] - 1) not in lis:
                self.pos = (self.pos[0], self.pos[1] - 1)
            else:
                return("nope")
        if direction == "right":
            if self.pos[0] != self.gridX and cells[(self.pos[0] + 1, self.pos[1])].tile_type[1] == "pass" and (self.pos[0] + 1, self.pos[1]) not in lis:
                self.pos = (self.pos[0] + 1, self.pos[1])
            else:
                return("nope")
        if direction == "left":
            if self.pos[0] != 0 and cells[(self.pos[0] - 1, self.pos[1])].tile_type[1] == "pass" and (self.pos[0] - 1, self.pos[1]) not in lis:
                self.pos = (self.pos[0] - 1, self.pos[1])
            else:
                return("nope")

    def draw(self):
        self.pixel_pos = (self.pos[0] * self.cell_size + self.offset, self.pos[1] * self.cell_size + self.offset)
        pg.draw.circle(self.surface, self.color, self.pixel_pos, self.radius, 0)

class Fire:
    def __init__(self, start, direction, surface, speed, shooter):
        self.pos = start
        self.status = True
        self.dir = direction
        self.counter = 0
        self.speed = speed
        self.surface = surface
        self.color = (0, 0, 0)
        self.shooter = shooter

    def draw(self):
        pg.draw.circle(self.surface, self.color, (int(self.pos[0]), int(self.pos[1])), 5, 0)

    def move(self, rate=60):
        distance = self.speed/rate
        if self.dir == "down":
            self.pos = (self.pos[0], self.pos[1] + distance)
        if self.dir == "up":
            self.pos = (self.pos[0], self.pos[1] - distance)
        if self.dir == "right":
            self.pos = (self.pos[0] + distance, self.pos[1])
        if self.dir == "left":
            self.pos = (self.pos[0] - distance, self.pos[1])

    def check(self, monsters, cell_size, player):
        global cells
        cell_pos = (int(self.pos[0]/cell_size), int(self.pos[1]/cell_size))
        if cells[cell_pos].tile_type[1] == "no pass":
            self.status = False
        enemies = monsters.copy()
        enemies.append(player)
        for enemy in enemies:
            if enemy.pos == cell_pos and enemy != self.shooter:
                enemy.hp -= 1
                print(enemy.hp)
                self.status = False



a = Ultimata((1184, 672))
a.main_loop()
