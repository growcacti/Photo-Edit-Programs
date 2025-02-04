import pygame as pg
import os
import random
from constants import Constants
from player import Player

con = Constants
screen = con.screen
W = con.W
H = con.H
W2 = con.W2
H2 = con.H2
QW = W / 4
HW = W / 2
HH = H / 2
QH = H / 4


class Expanding_Galaxy:
    def __init__(self, player):
        self.player = player
        self.cam = self.player.camera
        self.camx, self.camy = self.cam
        self.bgdata = []
        self.player = player
        self.x = 1000
        self.y = 1000
        self.w = W
        self.H = H
        self.stars = 200000

        # Defining colorlist here
        self.colorlist = [
            pg.Color("white"),
            pg.Color("gray59"),
            pg.Color("gray80"),
            pg.Color("gray93"),
            pg.Color("snow"),
            pg.Color("ivory"),
            pg.Color("turquoise1"),
            pg.Color("cyan"),
            pg.Color("cyan1"),
            pg.Color("aliceblue"),
            pg.Color("antiquewhite1"),
            pg.Color("ivory2"),
            pg.Color("aquamarine2"),
            pg.Color("aquamarine1"),
            pg.Color("aquamarine3"),
            pg.Color("azure"),
            pg.Color("skyblue"),
        ]

    def coordinates(self, camx, camy, radius):
        self.camxx = 2 * self.camx
        self.camyy = 2 * self.camy
        self.camrect = pg.Rect(self.camx, self.camy, W, H)
        while True:
            self.startx = int(self.camx) - W // 1
            self.stopx = int(self.camx) + W2 // 1
            self.starty = int(self.camy) - H // 1
            self.stopy = int(self.camy) + H2 // 1
            self.rx = random.randint(self.startx, self.stopx)
            self.ry = random.randint(self.starty, self.stopy)
            self.objrect = pg.Rect(self.rx, self.ry, radius * 2, radius * 2)
            if not self.objrect.colliderect(self.camrect):
                return self.rx, self.ry

    def add_bg(self, camx, camy):
        circle = {}
        circle["color"] = random.choice(self.colorlist)
        circle["radius"] = random.randint(
            1, 3
        )  # Adjust the radius range as per your requirement
        circle["x"], circle["y"] = self.coordinates(camx, camy, circle["radius"])
        return circle

    def boundaries(self, camx, camy, circle):
        self.bounds_left = self.camx - W
        self.bounds_top = self.camy - H
        self.boundsrect = pg.Rect(self.bounds_left, self.bounds_top, W2 * 2, H2 * 2)
        circle_rect = pg.Rect(
            circle["x"] - circle["radius"],
            circle["y"] - circle["radius"],
            circle["radius"] * 2,
            circle["radius"] * 2,
        )
        return not self.boundsrect.colliderect(circle_rect)

    def bgupdate(self, camx, camy):
        self.camx = camx
        self.camy = camy
        if len(self.bgdata) < self.stars:
            self.bgdata.append(self.add_bg(self.camx, self.camy))
        for circle in self.bgdata:
            pg.draw.circle(
                screen,
                circle["color"],
                (circle["x"] - camx, circle["y"] - camy),
                circle["radius"],
            )

        for i in range(len(self.bgdata) - 1, -1, -1):
            if self.boundaries(self.camx, self.camy, self.bgdata[i]):
                del self.bgdata[i]


class Galaxy:
    img = pg.image.load("gx/backgrounds/level4.png").convert_alpha()
    rect = img.get_rect()

    def __init__(self, player, dt):
        self.player = player
        self.screen = screen.copy()
        self.dt = dt

        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.sr = screen.get_rect()

        self.playrect = player.rect
        self.cam = self.player.camera
        self.invcam = self.player.invcam
        self.subcam = self.player.subcam
        self.revcam = self.player.revcam
        self.extcam = self.player.extcam
        self.camx, self.camy = self.cam
        self.playerpos = pg.math.Vector2(player.position)
        self.start = pg.Vector2(1000, 1000)

        self.img2 = self.img.subsurface(self.rect)

        self.img4 = self.img.subsurface(self.rect)
        self.img5 = self.img.subsurface(self.rect)

        self.dist = []
        self.dist1 = [i for i in range(1000, 100000) if i % 60000 == 0]
        self.dist2 = [j for j in range(100000, 1000000) if j % 200000 == 0]
        self.dist3 = [k for k in range(1000000, 100000000) if k % 300000 == 0]
        self.distance, self.projected, self.projected2 = player.update(dt)
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x, self.y = self.playerpos

    def draw(self, surface, dt):
        self.dt = dt

        self.distance, self.projected, self.projected2 = self.player.update(dt)

        surface.blit(self.img, -self.cam)

    def update(self, dt):
        self.distance, self.projected, self.projected2 = self.player.update(dt)

        self.blitdistance = self.distance * 2
        for distance in self.dist1:
            if self.blitdistance > distance:
                screen.blit(self.img, self.extcam, self.rect2)
                screen.blit(self.img4, self.revcam, self.rect)
                screen.blit(self.img5, self.revcam, self.rect)

                for blitdistance in self.dist2:
                    if self.blitdistance > distance:
                        screen.blit(self.img2, self.extcam, self.rect4)
                        screen.blit(self.img5, self.extcam, self.rect5)
                        screen.blit(self.img4, self.extcam, self.rect)
                for distance in self.dist3:
                    if self.blitdistance > distance:
                        screen.blit(self.img11, self.extcam, self.rect11)


con = Constants()


class Stars:
    def __init__(self, player):
        self.player = player
        self.cam = self.player.camera
        self.sizex = int(1300)
        self.sizey = int(800)
        self.size = (1300, 800)
        self.invcam = self.player.invcam
        self.subcam = self.player.subcam
        self.revcam = self.player.revcam
        self.extcam = self.player.extcam
        self.camx, self.camy = self.cam
        self.center_pos = (650, 400)
        self.bg = pg.Surface((self.size))
        self.rect = self.bg.get_rect()
        self.bg.set_colorkey((0, 0, 0))
        self.color = [0, 0, 0, 0]

    def starmap(self):
        wht = pg.Color("white")
        gry = pg.Color("gray59")
        gry2 = pg.Color("gray80")
        gry3 = pg.Color("gray93")
        snow = pg.Color("snow")
        ivory = pg.Color("ivory")
        cyan = pg.Color("turquoise1")
        colorlist = [wht, gry, gry2, gry3, snow, ivory, cyan]

        for self.color in colorlist:
            for self.stars in range(10):
                self.color = random.choice(colorlist)
                self.starx = random.randint(10, self.sizex)
                self.stary = random.randint(10, self.sizey)
                self.star = self.starx, self.stary
                self.radius = 1
                for self.stars in range(5):
                    self.color = random.choice(colorlist)
                    self.starx = random.randint(10, self.sizex)
                    self.stary = random.randint(10, self.sizey)
                    self.star = self.starx, self.stary
                    self.radius = 1
                    pg.draw.circle(self.bg, self.color, self.star, self.radius)
