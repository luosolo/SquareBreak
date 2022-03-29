import pyxel
import constants
from random import *


class Drawable:
    def __init__(self, x, y, u, v, w, h, name=None):
        self.name = name
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.width = w
        self.height = h

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.width, self.height)


class Movable(Drawable):
    def __init__(self, x, y, u, v, w, h, direction, name):
        super().__init__(x, y, u, v, w, h, name)

        self.direction = direction
        self.speed = 4

    def update_position(self):
        if self.direction == constants.UP:
            self.y -= self.speed
        elif self.direction == constants.DOWN:
            self.y += self.speed
        elif self.direction == constants.LEFT:
            self.x -= self.speed
        elif self.direction == constants.RIGHT:
            self.x += self.speed

    def is_outside(self):
        return self.x < 4 or self.x > 156 or self.y < 4 or self.y > 156

    def collide_with(self, item: Drawable):
        return abs(self.x - item.x) < self.width and abs(self.y - item.y) < self.height


class Enemy(Movable):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 0, 8, 6, 6, direction, "Enemy")
        self.speed = 3


class Bullet(Movable):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 8, 0, 4, 4, direction, "Bullet")


class Player(Drawable):

    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 8, 8, "Player")
        self.direction = constants.UP

    def draw(self):
        super(Player, self).draw()

        if self.direction == constants.UP:
            pyxel.rect(self.x, self.y - 4, 8, 4, 3)
        elif self.direction == constants.DOWN:
            pyxel.rect(self.x, self.y + self.height, 8, 4, 3)
        elif self.direction == constants.LEFT:
            pyxel.rect(self.x - 4, self.y, 4, 8, 3)
        elif self.direction == constants.RIGHT:
            pyxel.rect(self.x + self.width, self.y, 4, 8, 3)


class MainGame:

    def __init__(self, width=160, height=160):
        pyxel.init(width, height, title="Battle Square")
        pyxel.load("assets/sqb.pyxres")
        self.player = Player((160 - 8) / 2, (160 - 8) / 2)
        self.bullets: list[Bullet] = [None, None, None, None]
        self.enemies: list[Enemy] = [None, None, None, None]
        pyxel.run(self.update, self.draw)

    def add_enemy(self):
        el = [cnt for cnt in range(4) if self.enemies[cnt] is None]
        idx = choice(el)
        if idx == constants.UP:
            self.enemies[idx] = Enemy((160 - 6) / 2,  self.player.height, constants.DOWN)
        elif idx == constants.DOWN:
            self.enemies[idx] = Enemy((160 - 6) / 2, 160 - self.player.height, constants.UP)

        elif idx == constants.LEFT:
            self.enemies[idx] = Enemy(4, (160 - 6) / 2, constants.RIGHT)

        elif idx == constants.RIGHT:
            self.enemies[idx] = Enemy(160 - 6, (160 - 6) / 2, constants.LEFT)

    def check_collision(self):
        for cnt in range(len(self.bullets)):
            item = self.bullets[cnt]
            if item:
                item.update_position()
                if item.is_outside():
                    self.bullets[cnt] = None

        for cnt in range(len(self.enemies)):
            item = self.enemies[cnt]
            if item:
                item.update_position()
                if item.is_outside():
                    print(f"{item.name} {cnt} OUTSIDE and DELETED")
                    self.enemies[cnt] = None
                collide = False
                for bc in range(len(self.bullets)):
                    b = self.bullets[bc]
                    if b and item.collide_with(b):
                        collide = True
                        self.enemies[cnt] = None
                        self.bullets[bc] = None
                if not collide:
                    if item.collide_with(self.player):
                        self.enemies[cnt] = None
                        print("GAME OVER")

    def update(self):

        if pyxel.btnp(pyxel.KEY_E):
            self.add_enemy()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.player.direction = constants.DOWN
            if self.bullets[constants.DOWN] is None:
                self.bullets[constants.DOWN] = Bullet(self.player.x + 2,
                                                      self.player.y + self.player.height, constants.DOWN)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.player.direction = constants.UP
            if self.bullets[constants.UP] is None:
                self.bullets[constants.UP] = Bullet(self.player.x + 2,
                                                    self.player.y - 4, constants.UP)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.player.direction = constants.LEFT
            if self.bullets[constants.LEFT] is None:
                self.bullets[constants.LEFT] = Bullet(self.player.x - 4,
                                                      self.player.y + 2, constants.LEFT)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.player.direction = constants.RIGHT
            if self.bullets[constants.RIGHT] is None:
                self.bullets[constants.RIGHT] = Bullet(self.player.x + self.player.width,
                                                       self.player.y + 2, constants.RIGHT)



    def draw(self):
        pyxel.cls(0)

        pyxel.rect((160 - 8) / 2, 0, 8, 160, 7)

        pyxel.rect(0, (160 - 8) / 2, 160, 8, 7)

        self.check_collision()
        self.player.draw()
        for item in self.bullets:
            if item is not None:
                item.draw()

        for item in self.enemies:
            if item is not None:
                item.draw()
        pyxel.rect(0, 0, 160, 4, 1)
        pyxel.rect(0, 160 - 4, 160, 4, 1)

        pyxel.rect(0, 0, 4, 160, 1)
        pyxel.rect(160 - 4, 0, 4, 160, 1)
        if pyxel.frame_count % 16 == 0:
            self.add_enemy()


MainGame()
