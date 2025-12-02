import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Waves")
clock = pg.time.Clock()


class Wave:
    wave_count = 3
    def __init__(self, pos, color, points, amplitude):
        self.points = [0] * points
        self.waves = [random.random() * 2 for i in range(Wave.wave_count)]
        self.pos = pos
        self.color = pg.Color(0)
        self.color.hsva = (color, 100, 100)
        self.amplitude = amplitude
    
    def update_points(self, frame):
        self.points[1:] = self.points[0:-1]
        self.points[0] = sum(
            self.amplitude * sin(i * frame / 20)
            for ind, i in enumerate(self.waves, start=1)
        ) / Wave.wave_count
    
    def draw(self, canvas):
        polygon = [window_size, (0, window_size[1])]
        step = window_size[0] / (len(self.points) - 1)
        x = 0
        for i in self.points:
            point = (x, i + self.pos)
            polygon.append(point)
            x += step
        pg.draw.polygon(canvas, self.color, polygon)


waves = [
    Wave(
        pos = (i / 3) ** 3 * 20 + 250,
        color = i * 3 + 190,
        points = 250 - i * 20,
        amplitude = i * 10,
    )
    for i in range(-5, 10)
]

run = True
frame = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((127, 255, 255))
    for i in waves:
        i.draw(canvas)
        i.update_points(frame)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    frame += 1

pg.quit()
