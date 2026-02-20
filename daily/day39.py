import pygame as pg
from random import random
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Flow")
clock = pg.time.Clock()


particles = []
for _ in range(100):
    x = random() * window_size[0]
    y = random() * window_size[1]
    particles.append([x, y])


color_water = pg.Color(0, 20, 50)
color_water_dark = pg.Color(10, 0, 30)
color_sunray = pg.Color(31, 50, 64)
color_particle = pg.Color(255, 255, 255)

bg_size_y = window_size[1] + 100
background = pg.Surface((window_size[0], bg_size_y))
overlay = pg.Surface(window_size)

for i in range(11):
    color = color_water.lerp(color_water_dark, i / 10)
    y_high = i * bg_size_y / 10
    y_low = (i+1) * bg_size_y / 10
    points = (
        (0, y_high - 100), (window_size[0], y_high),
        (window_size[0], y_low), (0, y_low - 100)
    )
    pg.draw.polygon(background, color, points)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(background, (0, sin(t / 100) * 50 - 50))
    
    overlay.fill((0, 0, 0))
    for x in range(0, 6):
        ray_from = (window_size[0] / 1.5 + x*75 + sin(t/100 - x/3) * 25, 0)
        ray_to = (window_size[0] / 2 + x*150 + sin(t/100 - x/3 - 1) * 75, window_size[1])
        pg.draw.line(overlay, color_sunray, ray_from, ray_to, 50)
    
    canvas.blit(overlay, (0, 0), None, pg.BLEND_ADD)
    
    for i in particles:
        pg.draw.circle(canvas, color_particle, i, 3, 1)
        i[0] -= 3
        i[1] += sin(i[0] / 100 + 0.5 - t / 300)
    
    if t % 5 == 0:
        particles = [i for i in particles if i[0] >= -5]
        particles.append([window_size[0], random() * window_size[1]])
    
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
