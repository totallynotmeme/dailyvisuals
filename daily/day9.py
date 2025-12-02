import pygame as pg
import random


window_size = (1600, 900)
path = input("Path to image file: ").strip("'\" ")

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Squares")
clock = pg.time.Clock()

image = pg.image.load(path)
#factor = window_size[1] / image.get_size()[1]
#image = pg.transform.smoothscale_by(image, factor)
image = pg.transform.smoothscale(image, window_size)
colormap = pg.Surface(window_size)
colormap.blit(image, image.get_rect(center=(window_size[0]//2, window_size[1]//2)))


stack = []
step_x = window_size[0] // 16
step_y = window_size[1] // 9
for y in range(0, window_size[1], step_y):
    for x in range(0, window_size[0], step_x):
        stack.append((x, y, step_x, step_y))
#stack = stack[::-1]


run = True
rects = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    limit = 0
    while stack:
        limit += 1
        if limit > 200:# or rects > 3000:
            break
        
        rect = stack.pop(0)
        color = colormap.get_at(rect[:2])
        pg.draw.rect(canvas, color, rect, 1)
        x, y, sx, sy = rect
        if min(sx, sy) <= 8:
            continue
        
        newrects = [
            (x + 1, y + 1, sx // 2 - 2, sy // 2 - 2),
            (x + 1 + sx // 2, y + 1, sx // 2 - 2, sy // 2 - 2),
            (x + 1, y + sy // 2 + 1, sx // 2 - 2, sy // 2 - 2),
            (x + 1 + sx // 2, y + sy // 2 + 1, sx // 2 - 2, sy // 2 - 2),
        ]
        newrects.pop(random.randint(0, 3))
        stack.extend(newrects)
        rects += 1
    
    random.shuffle(stack)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
