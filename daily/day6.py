import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Ants")
clock = pg.time.Clock()

overlay = pg.Surface(window_size)
overlay.set_alpha(5)


class Ant:
    up = pg.Vector2(0, -5)
    
    def __init__(self):
        self.pos = pg.Vector2(window_size) / 2
        self.rot = random.random() * 360
        self.prev_pos = self.pos
    
    def step(self, canvas):
        self.prev_pos = self.pos.copy()
        self.pos += Ant.up.rotate(self.rot)
        
        for deg in range(-20, 21, 10):
            pixel = self.pos + Ant.up.rotate(deg + self.rot) * 5
            try:
                weight = canvas.get_at(tuple(map(int, pixel)))
                weight = sum(weight[:3]) / 765 / 10
            except IndexError:
                continue
            self.rot = (self.rot * 9 + deg * weight) / (9 + weight)
        
        self.rot += random.random() * 5
        self.rot %= 360
        
        limit_x = window_size[0] - 1
        limit_y = window_size[1] - 1
        
        if self.pos.x < 0:
            self.pos.x = limit_x
            self.prev_pos.x = limit_x
        if self.pos.x > limit_x:
            self.pos.x = 0
            self.prev_pos.x = 0
        if self.pos.y < 0:
            self.pos.y = limit_y
            self.prev_pos.y = limit_y
        if self.pos.y > limit_y:
            self.pos.y = 0
            self.prev_pos.y = 0
    
    def draw(self, canvas):
        pg.draw.line(canvas, (255, 255, 255), self.pos, self.prev_pos, 5)


ants = [Ant() for i in range(1000)]

run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    for i in ants:
        i.step(canvas)
        i.draw(canvas)
    
    canvas.blit(overlay, (0, 0))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
