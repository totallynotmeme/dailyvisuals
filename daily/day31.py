import pygame as pg
import random
from math import sin, pi


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("JOLLY tree")
clock = pg.time.Clock()


center_x = window_size[0]//2
moon_pos = (window_size[0] - 150, 70)
moon_shadow_pos = (window_size[0] - 170, 65)

color_sky = pg.Color(5, 10, 40)
color_snow = pg.Color(220, 220, 255) # also color for the moon
color_tree_light = pg.Color(20, 150, 20)
color_tree_mid = pg.Color(15, 100, 15)
color_tree_dark = pg.Color(10, 50, 10)


snow_front = []
snow_back = [] # draw some snowflakes behind the tree for better 3d-ish effect??

run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_sky)
    
    pg.draw.circle(canvas, color_snow, moon_pos, 60)
    pg.draw.circle(canvas, color_sky, moon_shadow_pos, 60)
    
    if t % 30 == 0:
        x = random.randint(0, window_size[0])
        snow_front.append(pg.Vector3(x, 0, 0))
    if t % 30 == 15:
        x = random.randint(0, window_size[0])
        snow_back.append(pg.Vector3(x, 0, 0))
    
    for vec in snow_back.copy():
        # (x, y, speed_x)
        vec[2] /= 1.05
        vec[2] += random.random() - 0.5
        vec[0] += vec[2] / 1.1
        vec[1] += 3
        if vec[1] > window_size[1] + 5:
            snow_back.remove(vec)
        else:
            pg.draw.circle(canvas, color_snow, (vec[0], vec[1]), 5)
    
    offset = t % 150
    iterator = range(window_size[1] + offset, window_size[1]//3 + offset, -150)
    for ind, y in enumerate(iterator):
        if ind == len(iterator)-1:
            size = (t % 150) / 150
            size = size ** 0.5 * 200
        else:
            size = 200
        angle = (y + t) / 370 % 1
        sin_angle = sin(angle * pi)
        sin_factor = size / 4
        
        color_right = color_tree_light.lerp(color_tree_mid, angle)
        color_left = color_tree_mid.lerp(color_tree_dark, angle)
        
        point_left = (center_x - sin_angle * sin_factor - size, y)
        point_mid = (center_x + size - sin(angle * pi/2) ** 2 * size*2, y)
        point_right = (center_x + sin_angle * sin_factor + size, y)
        point_up = (center_x, y - size * 1.2)
        
        pg.draw.polygon(canvas, color_left, (point_up, point_mid, point_left))
        pg.draw.polygon(canvas, color_right, (point_up, point_mid, point_right))
    
    for vec in snow_front.copy():
        # (x, y, speed_x)
        vec[2] /= 1.1
        vec[2] += random.random() - 0.5
        vec[0] += vec[2]
        vec[1] += 3
        if vec[1] > window_size[1] + 5:
            snow_front.remove(vec)
        else:
            pg.draw.circle(canvas, color_snow, (vec[0], vec[1]), 5)
    
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
