import pygame as pg
import random
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Thalassophobia")
clock = pg.time.Clock()


window_size = pg.Vector2(window_size)
window_center = window_size / 2

wave_points = 100
wave_layers = 30
wave_step_x = window_size.x / wave_points
color_sky = pg.Color(10, 30, 50)
color_water_near = pg.Color(0, 200, 255)
color_water_far = pg.Color(0, 50, 100)

background = pg.Surface(window_size)
background.fill(color_sky)
y_base = window_center.y
for y in range(int(window_size.y - y_base)):
    factor = (y / (window_size.y - y_base)) ** 1.2
    c = color_water_near.lerp(color_water_far, factor)
    y += y_base
    pg.draw.line(background, c, (0, y), (window_size.x, y))


height_pos = 0
shift_pos = 0
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    mouse_pos = pg.mouse.get_pos()
    height_pos = (height_pos * 3 + mouse_pos[1]) / 4
    height_factor = 120 - 100 * height_pos / window_size.y
    shift_pos = (shift_pos * 3 + mouse_pos[0]) / 4
    shift_factor = 100 * shift_pos / window_size.x
    
    canvas.blit(background, (0, 0))
    
    wave_top = window_center.y - (wave_layers ** 0.3) * height_factor - 15
    for i in range(wave_layers, -1, -1):
        wave_cutoff = window_center.y - (i ** 0.3) * height_factor
        c = color_water_near.lerp(color_water_far, i / wave_layers)
        
        points = []
        distance = 5 + i
        offset = i ** 2 * 4 - shift_factor / (i + 10)
        for j in range(wave_points+1):
            off_j = j / wave_points
            wave_offset = sin(offset + off_j * distance * 5 + t / distance / 3) * 5
            wave_offset += sin(offset + off_j * distance * 2 + t / distance / 6) * 10
            points.append((j * wave_step_x, wave_top + wave_offset))
        points.append((window_size.x, wave_cutoff))
        points.append((0, wave_cutoff))
        pg.draw.polygon(canvas, c, points)
        
        wave_top = wave_cutoff - 15
    
    # ..wh- what is that??
    color_factor = (1 - height_pos / window_size.y) / 8
    color_base = color_water_far.lerp(color_water_near, color_factor)
    color_eyes = color_base.lerp("white", 0.2)
    color_body = color_base.lerp("black", 0.2)
    
    pos_x = shift_factor / 2 + window_center.x
    pos_y = height_pos / 10 + window_size.y * 0.8
    # body
    points = [
        (pos_x - 120, pos_y + 20 + sin(t/50 - 0.7) * 2),
        (pos_x - 110, pos_y - 30 + sin(t/50 - 0.6) * 2),
        (pos_x + 10, pos_y - 50 + sin(t/50 + 0.4) * 2),
        (pos_x + 100, pos_y - 24 + sin(t/50 + 2.4) * 2),
        (pos_x + 120, pos_y + 20 + sin(t/50 + 2.6) * 2),
        (pos_x + 80, pos_y + 80 + sin(t/50 + 2.1) * 2),
        (pos_x - 50, pos_y + 70 + sin(t/50 + 0.2) * 2),
    ]
    pg.draw.polygon(canvas, color_body, points)
    # the
    for raw_x in (-80, -40, -15, 10, 35, 70, 105):
        x = raw_x + pos_x
        for ind, y in enumerate(range(0, 210, 15)):
            y += pos_y + 30
            pos_from = (x + sin(ind - t/60 + raw_x/6) * ind, y)
            pos_to = (x + sin(ind+1 - t/60 + raw_x/6) * ind, y + 15)
            pg.draw.line(canvas, color_body, pos_from, pos_to, 5)
    # eyes
    if t % 500 < 480:
        pg.draw.circle(canvas, color_eyes, (pos_x - 30, pos_y + sin(t/50) * 2), 5)
    else:
        eye_y = pos_y + sin(t/50) * 2
        pg.draw.line(canvas, color_eyes, (pos_x-34, pos_y), (pos_x-26, pos_y), 3)
    if (t+5) % 500 < 480:
        pg.draw.circle(canvas, color_eyes, (pos_x + 30, pos_y + 2 + sin(t/50 + 2) * 2), 5)
    else:
        eye_y = pos_y + 2 + sin(t/50 + 2) * 2
        pg.draw.line(canvas, color_eyes, (pos_x+26, pos_y), (pos_x+34, pos_y), 3)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
