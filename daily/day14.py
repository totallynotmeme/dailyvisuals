import pygame as pg
import random
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Weird")
clock = pg.time.Clock()
font = pg.font.SysFont("consolas", 25)


def surf_to_rgb(surf):
    size = surf.get_size()
    red = pg.Surface(size)
    red.fill((255, 0, 0))
    red.blit(surf, (0, 0), None, pg.BLEND_MULT)
    green = pg.Surface(size)
    green.fill((0, 255, 0))
    green.blit(surf, (0, 0), None, pg.BLEND_MULT)
    blue = pg.Surface(size)
    blue.fill((0, 0, 255))
    blue.blit(surf, (0, 0), None, pg.BLEND_MULT)
    return red, green, blue


texts = [
    "do you want to see me",
    "come closer trust me",
    "dont forget to smile",
    "i am your new friend",
    "this is a safe place",
    "please stay with us",
    "be part of our family",
    "why are you afraid",
]

base = pg.Surface(window_size)
# sky
base.fill((70, 150, 200))
# sun
pg.draw.circle(base, (255, 255, 200), (0, 0), 200)
# background
for i in range(4, -1, -1):
    y_base = window_size[1] - 50 - i*10
    for x in range(0, window_size[0]+1, 50 + i*25):
        y = y_base + random.randint(-10, 10)
        r = random.randint(200 + i*50, 250 + i*50)
        pg.draw.circle(base, (50 - i*10, 150 - i*20, 50 - i*10), (x, y), r)
# setting up y_base
y_base = window_size[1] - 50
# house stuff:
# base
pg.draw.polygon(base, (230, 230, 180), (
    (140, y_base - 400),
    (220, y_base - 450),
    (300, y_base - 400),
    (300, y_base - 150),
    (140, y_base - 150),
))
# door
pg.draw.rect(base, (120, 40, 40), pg.Rect(205, y_base - 215, 30, 60))
# windows
for x in (160, 205, 250):
    for y in (370, 290):
        pg.draw.rect(base, (60, 60, 40), pg.Rect(x, y_base - y, 30, 45))
        pg.draw.rect(base, (255, 255, 200), pg.Rect(x, y_base - y, 30, 45), 3)
# 3d-ish side
pg.draw.polygon(base, (200, 200, 150), (
    (100, y_base - 405),
    (140, y_base - 405),
    (140, y_base - 150),
    (100, y_base - 170),
))
# roof
pg.draw.polygon(base, (120, 80, 80), (
    (225, y_base - 450),
    (305, y_base - 400),
    (300, y_base - 400),
    (220, y_base - 450),
))
pg.draw.polygon(base, (150, 100, 100), (
    (90, y_base - 405),
    (170, y_base - 450),
    (225, y_base - 450),
    (145, y_base - 400),
))
# shadow
pg.draw.polygon(base, (40, 130, 40), (
    (140, y_base - 150),
    (300, y_base - 150),
    (400, y_base - 100),
    (340, y_base - 80),
    (240, y_base - 100),
))


buffer_surf = pg.Surface(window_size)
rgb_shift_t = 0


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    # nothing behind here.
    if t % 20 == 0:
        behind = []
        y = y_base - 600 + random.randint(-10, 10)
        x_base = window_size[0] - 400
        while y < y_base - 300:
            x = x_base + random.randint(-10, 10)
            y_size = random.randint(10, 50)
            behind.append(pg.Rect(x, y, 200, y_size))
            y += y_size
    
    # rgb shift timer
    if t % 100 == 0:
        if random.random() < 0.6:
            rgb_shift_t = random.random() * 120
    
    # changing text every once in a while
    if t % 310 == 0:
        active_text = font.render(random.choice(texts), True, (70, 0, 0))
    
    # refreshing screen and drawing stuff
    canvas.blit(base, (0, 0))
    
    # clouds
    for orig_x, orig_y in (
            (window_size[0] // 4, 120),
            (window_size[0] // 2, 170),
            (window_size[0] // 4 * 3, 60),
        ):
        if random.random() < 0.01:
            continue
        for i in range(10):
            x = orig_x + i*20 - 100
            y = orig_y + math.sin(t/20 + x/10) * 3
            r = math.sin(i / 3) * 20 + 15
            pg.draw.circle(canvas, (255, 255, 255), (x, y), r)
    
    # texts
    for i in range(5):
        x = window_size[0] - 700 + i * 10
        y = math.sin(t / 60 - i / 3)**2 * 80 + y_base - 450 - i * 10
        canvas.blit(active_text, (x, y))
    
    # brightness stripes
    if t % 10 == 0:
        for x in range(0, window_size[0], 5):
            c = random.randint(250, 255)
            pg.draw.rect(buffer_surf, (c, c, c), pg.Rect(x, 0, 5, window_size[1]))
    canvas.blit(buffer_surf, (0, 0), None, pg.BLEND_MULT)
    
    # actually doing rgb shift
    if rgb_shift_t > 0:
        rgb_shift_t -= 1
        rgb_shift = random.random() / 2 + 1
        r, g, b = surf_to_rgb(canvas)
        canvas.fill((0, 0, 0))
        canvas.blit(r, (rgb_shift*-5, rgb_shift*2), None, pg.BLEND_ADD)
        canvas.blit(g, (0, 0), None, pg.BLEND_ADD)
        canvas.blit(b, (rgb_shift*5, rgb_shift*-2), None, pg.BLEND_ADD)
    
    # [redacted]
    for i in behind:
        pg.draw.rect(canvas, (0, 0, 0), i)
    
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
