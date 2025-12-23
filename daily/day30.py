import pygame as pg
import random
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Flow")
clock = pg.time.Clock()


window_center = pg.Vector2(window_size) / 2
scale = window_center.y / 36
canvas.set_alpha(200)
color = pg.Color(0)

run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(canvas, (-10, 0))
    pg.draw.rect(canvas, (0, 0, 0), pg.Rect(window_size[0]-10, 0, 10, window_size[1]))
    
    for i in range(36, 0, -1):
        color.hsva = (i*10, 100, 100, 100)
        sign = (i%2) * 2 - 1
        a = t / i**0.5 / 10
        x = window_size[0] - 10
        y = math.sin(a) * sign * scale * i
        y += window_center.y - 10
        pg.draw.rect(canvas, color, pg.Rect(x, y, 10, 20))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
