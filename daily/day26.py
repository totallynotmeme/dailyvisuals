import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Tiling")
clock = pg.time.Clock()


color_from = pg.Color(0)
color_to = pg.Color(0)

grid_offset_x = -50
grid_offset_y = -50
grid_step_x = 100
grid_step_y = 100
rounding = 0
line_a = 0
line_b = 0

up = pg.Vector2(0, -1)
up_angle = 0


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    factor = min(max(t - 20, 0), 50) / 50
    bg_color = color_to.lerp(color_from, factor)
    canvas.fill(bg_color)
    
    for x in range(grid_offset_x, window_size[0] + grid_step_x, grid_step_x):
        for y in range(grid_offset_y, window_size[1] + grid_step_y, grid_step_y):
            factor = line_a*x + line_b*y + (t - 150) * 15
            if factor > 200:
                continue
            factor = min(max(1 - factor / 200, 0), 0.95) ** 0.3
            size = pg.Vector2(grid_step_x, grid_step_y) * factor
            rect = pg.Rect((0, 0), size)
            rect.center = (x, y)
            pg.draw.rect(canvas, color_to, rect, 0, rounding)
    
    if t <= 0:
        t = 300
        color_from.hsva = color_to.hsva
        up_angle += random.random() * 80 + 30
        new_hue = color_from.hsva[0] + random.randint(90, 180)
        color_to.hsva = (new_hue % 360, 70, 70, 100)
        
        grid_step_x = random.randint(30, 100)
        grid_step_y = random.randint(30, 100)
        grid_offset_x = -random.randint(0, grid_step_x)
        grid_offset_y = -random.randint(0, grid_step_y)
        rounding = random.randint(0, 20)
        line_dir = up.rotate(up_angle)
        line_a = line_dir.x
        line_b = line_dir.y
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t -= 1

pg.quit()
