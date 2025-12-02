import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Grow")
clock = pg.time.Clock()


offsets = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
)
agents = [(800, 450)]
canvas.set_at(agents[0], (0, 127, 255))


run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    limit = -1
    while agents:
        limit += 1
        if limit > len(agents) // 5:
            break
        pos = agents.pop(0)
        color = canvas.get_at(pos)
        x, y = pos
        
        for off_x, off_y in offsets:
            new_pos = (x + off_x, y + off_y)
            if min(new_pos) < 0:
                continue
            if new_pos[0] >= window_size[0] or new_pos[1] >= window_size[1]:
                continue
            color_at = canvas.get_at(new_pos)
            if color_at != (0, 0, 0, 255):
                continue
            
            new_col = tuple(min(max(i + random.randint(-5, 5), 0), 255) for i in color)
            canvas.set_at(new_pos, new_col)
            agents.append(new_pos)
    if len(agents) < 10000:
        random.shuffle(agents)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
