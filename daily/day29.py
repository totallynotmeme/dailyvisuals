import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("188")
clock = pg.time.Clock()


window_size = pg.Vector2(window_size)
window_center = window_size / 2

overlay = pg.Surface((int(window_size.x), int(window_center.y) + 20))
overlay.fill((255, 255, 255))

for y in range(0, int(window_center.y)+20, 10):
    c = 1 - y / window_center.y
    c = c**2 * 255
    pg.draw.rect(overlay, (c, c, c), pg.Rect(0, y, window_size.x, 10))


corner_topleft = pg.Vector2(0, window_center.y)
corner_topmid = pg.Vector2(window_center.x / 1.2 - 5, 0)
corner_topright = pg.Vector2(window_size.x, window_center.y / 3)
vanish_point = pg.Vector2(window_center.x, window_size.y * 7)

color_wall_left = pg.Color(110, 110, 100)
color_wall_right = pg.Color(120, 120, 110)
color_window_unlit = pg.Color(10, 10, 15)
color_window_lit = pg.Color(200, 200, 150)
color_eyes = pg.Color(200, 0, 0)
edge_data = {
    # x offset: color
    0: pg.Color(200, 200, 180),   # border: top
    70: pg.Color(160, 160, 140),  # border: side
    140: pg.Color(180, 180, 170), # floor: shadow
    170: pg.Color(190, 190, 175), # floor: floor
}
windows_color_table = [color_window_unlit, color_window_lit]


direction_topleft_topmid = corner_topmid - corner_topleft
direction_topright_topmid = corner_topright - corner_topmid

def project_left(x, y):
    proj = corner_topleft + direction_topleft_topmid * (x / 20)
    proj += (vanish_point - proj) * (y / 150)
    return proj

def project_right(x, y):
    proj = corner_topmid + direction_topright_topmid * (x / 20)
    proj += (vanish_point - proj) * (y / 150)
    return proj


poly_edge = (
    (window_size.x, 0),
    (window_size.x / 1.1, 0),
    (window_size.x / 1.3, window_size.y),
    (window_size.x, window_size.y),
)
poly_left_wall = (
    (0, 0),
    corner_topmid,
    project_left(20, 22),
    (0, window_size.y),
)
# no need for right wall poly since we're just filling the screen to paint it


window_count = 63 # print(window_ind) after window drawing loops
windows_table = [random.random() > 0.5 for i in range(window_count)]


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_wall_right)
    pg.draw.polygon(canvas, color_wall_left, poly_left_wall)
    
    if random.random() < 0.01:
        ind = random.randint(0, window_count-1)
        windows_table[ind] = not windows_table[ind]
    windows_table[19] = False
    
    window_ind = 0
    
    # left wall
    for x in range(1, 19, 4):
        for y in range(-7, 20, 4):
            p1 = project_left(x, y)
            p2 = project_left(x, y+1.5)
            p3 = project_left(x+1.7, y+1.5)
            p4 = project_left(x+1.7, y)
            is_lit = windows_table[window_ind] and random.random() < 0.999
            color = windows_color_table[is_lit]
            pg.draw.polygon(canvas, color, (p1, p2, p3, p4))
            window_ind += 1
    
    # you would not believe your eyes. you would not believe your eyes.
    # you would not believe your e-e-e-eye-e-es
    p1 = project_left(9.5, 13.7)
    p2 = project_left(9.9, 13.78)
    if t % 248 < 240:
        pg.draw.circle(canvas, color_eyes, p1, 3)
        pg.draw.circle(canvas, color_eyes, p2, 3)
    
    # right wall
    for x in range(1, 16, 4):
        for y in range(-7, 20, 4):
            p1 = project_right(x, y)
            p2 = project_right(x, y+1.5)
            p3 = project_right(x+1.7, y+1.5)
            p4 = project_right(x+1.7, y)
            is_lit = windows_table[window_ind] and random.random() < 0.999
            color = windows_color_table[is_lit]
            pg.draw.polygon(canvas, color, (p1, p2, p3, p4))
            window_ind += 1
    
    overlay_pos = window_center.y + sin(t / 100)*20
    overlay_pos = int(overlay_pos / 5) * 5
    canvas.blit(overlay, (0, overlay_pos), None, pg.BLEND_MULT)
    
    for off_x, color in edge_data.items():
        points = [(x + off_x, y) for x, y in poly_edge]
        pg.draw.polygon(canvas, color, points)
    
    """ add # at the start of this line to draw perspective lines
    pg.draw.aaline(canvas, "red", corner_topleft, corner_topmid)
    pg.draw.aaline(canvas, "red", corner_topright, corner_topmid)
    pg.draw.aaline(canvas, "red", corner_topleft, vanish_point)
    pg.draw.aaline(canvas, "red", corner_topmid, vanish_point)
    pg.draw.aaline(canvas, "red", corner_topright, vanish_point)
    #"""
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
