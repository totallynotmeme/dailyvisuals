import pygame as pg
import random


window_size = (1600, 900)
path = input("Path to image file: ").strip("'\" ")

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Circles")
clock = pg.time.Clock()

image = pg.image.load(path)
#factor = window_size[1] / image.get_size()[1]
#image = pg.transform.smoothscale_by(image, factor)
image = pg.transform.smoothscale(image, window_size)
colormap = pg.Surface(window_size)
colormap.blit(image, image.get_rect(center=(window_size[0]//2, window_size[1]//2)))


run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    for i in range(100):
        pos = (
            random.randint(0, window_size[0]-1),
            random.randint(0, window_size[1]-1),
        )
        color = colormap.get_at(pos)
        radius = random.randint(5, 25)
        pg.draw.circle(canvas, color, pos, radius)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
