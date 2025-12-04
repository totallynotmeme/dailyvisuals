import pygame as pg
import random


window_size = (1600, 900)


class Point:
    count = 255
    def __init__(self, hue):
        self.pos = pg.Vector2(window_size) / 2
        self.vel = pg.Vector2()
        self.prevs = [tuple(self.pos)] * 30
        self.skip = [True] * 30
        self.color = pg.Color(0)
        self.color.hsva = (360 * hue / Point.count, 100, 100, 100)
    
    def draw_and_step(self, canvas):
        self.pos += self.vel
        skip = self.pos.x < 0 or self.pos.x >= window_size[0]
        skip |= self.pos.y < 0 or self.pos.y >= window_size[1]
        self.pos.x %= window_size[0]
        self.pos.y %= window_size[1]
        self.vel += (random.random()-0.5, random.random()-0.5)
        self.vel *= 0.99
        self.prevs.pop(0)
        self.prevs.append(tuple(self.pos))
        self.skip.pop(0)
        self.skip.append(skip)
        ind = 0
        for i, j, skip in zip(self.prevs, self.prevs[1:], self.skip[1:]):
            if not skip:
                pos = min(i, j)
                corner = max(i, j)
                size = (abs(corner[0] - pos[0]) + 1, abs(corner[1] - pos[1]) + 1)
                pg.draw.rect(canvas, self.color.lerp(0, 1-ind/30), pg.Rect(pos, size))
            ind += 1


pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Pixellines")
clock = pg.time.Clock()

points = [Point(i) for i in range(Point.count)]


run = True
while run:
    mouserel = pg.Vector2()
    for ev in pg.event.get():
        if ev.type == pg.MOUSEMOTION:
            mouserel += ev.rel
        if ev.type == pg.QUIT:
            run = False
            break

    canvas.fill((0, 0, 0))
    
    mousepos = pg.Vector2(pg.mouse.get_pos())
    for i in points:
        i.draw_and_step(canvas)
        if mouserel:
            i.vel += 3*mouserel / (mousepos.distance_to(i.pos) + 10)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
