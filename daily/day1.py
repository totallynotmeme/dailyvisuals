import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Blob")
clock = pg.time.Clock()


class Layer:
    center = pg.Vector2(window_size) / 2
    def __init__(self, radius, points, hue):
        self.radius = radius
        self.points = [0] * points
        self.new_speeds()
        self.hue = hue % 360
        surf_size = (radius + 5) / 5 + radius
        self.surface = pg.Surface((surf_size*2, surf_size*2))
        self.local_center = pg.Vector2(surf_size, surf_size)
        self.rect = self.surface.get_rect(center=Layer.center)
    
    
    def draw(self, frame, canvas):
        angle_step = 360 / len(self.points)
        polygon = []
        hue = (self.hue + frame) % 360
        
        for ind, r in enumerate(self.points):
            r = sin(r) * (self.radius + 5) / 5 + self.radius
            direction = pg.Vector2(0, r).rotate(angle_step * ind)
            polygon.append(tuple(direction + self.local_center))
            self.points[ind] += self.speeds[ind]
        
        self.surface.fill((0, 0, 0))
        col = pg.Color(0)
        col.hsva = (hue, 100, 5)
        pg.draw.polygon(self.surface, col, polygon, 5) # replace 5 with 0 to fill
        canvas.blit(self.surface, self.rect, None, pg.BLEND_ADD)
    
    
    def new_speeds(self):
        self.speeds = [random.random() / 20 + 0.01 for i in range(len(self.points))]


layers = [
    Layer(i*18, i//2+10, i*45) for i in range(1, 21)
]
overlay = pg.Surface(window_size)
overlay.set_alpha(5)

run = True
frame = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    if frame % 300 == 0:
        for i in layers:
            i.new_speeds()
    
    #canvas.fill((250, 250, 250), special_flags=pg.BLEND_MULT)
    #canvas.fill((1, 1, 1), special_flags=pg.BLEND_SUB)
    canvas.blit(overlay, (0, 0))
    for i in layers:
        i.draw(frame, canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    frame += 1

pg.quit()
