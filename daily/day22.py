import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Title") # Title
clock = pg.time.Clock()

font = pg.font.SysFont("consolas", 35)

texts = [
    "ran out of ideas",
    "don't know what to do",
    "what if i just...",
    "write down some random text",
    # and
    "use that as today visuals?",
    "yeah sounds like a great idea",
    "surely nothing can go wrong"
]

overlay = pg.Surface(window_size)
overlay.fill((250, 250, 250))

original = pg.Surface(window_size)
original.set_alpha(5)


color = pg.Color(0)
run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(original, (0, 0))
    canvas.blit(canvas, (0, 1), None, pg.BLEND_MAX)
    canvas.blit(overlay, (0, 0), None, pg.BLEND_MULT)
    
    for i in range(2):
        color.hsva = (random.randint(0, 360), 50, 100, 100)
        pos = (random.randint(0, window_size[0]), random.randint(0, window_size[1]))
        txt = font.render(random.choice(texts), True, color)
        
        rect = txt.get_rect(center=pos)
        canvas.blit(txt, rect)
        pg.draw.rect(original, (0, 0, 0), rect)
        original.blit(txt, rect)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
