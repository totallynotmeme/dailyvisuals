import pygame as pg


window_size = (1600, 900)
small_window_size = tuple(i-5 for i in window_size)

pg.init()
screen = pg.display.set_mode(window_size)
canvas = pg.Surface(window_size)
pg.display.set_caption("Grid")
clock = pg.time.Clock()


run = True
frame = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    
    for x in range(0, window_size[0], 50):
        x += frame / 2 % 50
        hue = min(int(255 * x / window_size[0]), 255)
        color = (0, 255, hue)
        pg.draw.aaline(canvas, color, (x, 0), (x, window_size[1]))
    
    for y in range(0, window_size[1], 50):
        y += frame / 2 % 50
        hue = min(int(255 * y / window_size[1]), 255)
        color = (255, hue, 0)
        pg.draw.aaline(canvas, color, (0, y), (window_size[0], y))
    
    
    canvas = pg.transform.smoothscale(canvas, small_window_size)
    canvas = pg.transform.smoothscale(canvas, window_size)
    screen.blit(canvas, (0, 0))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    frame += 1

pg.quit()
