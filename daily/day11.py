import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Addition")
clock = pg.time.Clock()


cell_size = 16
per_step = 20 # frames per step (at 60fps)
modulo = 6 # how many colors
grid_size = (window_size[0]//cell_size, window_size[1]//cell_size)
grid = {(x, y): 0 for x in range(grid_size[0]) for y in range(grid_size[1])}
grid_old = {}

colors = [pg.Color(0, 0, 0)]
c = pg.Color(0)
for i in range(modulo-1):
    c.hsva = (360*i/modulo, 100, 80, 100)
    colors.append(pg.Color(c))

grid[(grid_size[0]//2, grid_size[1]//2)] = 1


def get_nearby(x, y):
    near = [(x, y)]
    if x > 0:
        near.append((x - 1, y))
    if x < grid_size[0]-1:
        near.append((x + 1, y))
    if y > 0:
        near.append((x, y - 1))
    if y < grid_size[1]-1:
        near.append((x, y + 1))
    return near


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    if t % per_step == 0:
        grid_old = grid.copy()
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                grid[(x, y)] = sum(grid_old[i] for i in get_nearby(x, y)) % modulo
    for pos, val in grid.items():
        pix_pos = (pos[0] * cell_size, pos[1] * cell_size)
        col_1 = colors[val]
        col_2 = colors[grid_old[pos]]
        this_col = col_2.lerp(col_1, t/per_step % 1)
        pg.draw.rect(canvas, this_col, pg.Rect(*pix_pos, cell_size, cell_size))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
