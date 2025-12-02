import pygame as pg
from math import sin, cos
import random


window_size = (1600, 900)

water_color = (0, 127, 255)
light_color = (100, 80, 60)


def generate():
    global light_shines
    global bubbles
    light_shines = []
    center = window_size[0] / 2
    for _ in range(10):
        p1 = (random.randint(200, window_size[0] - 200), 0)
        p2 = (p1[0] + random.randint(-200, 200), 0)
        low_p1 = ((p1[0] - center) * 1.5 + center, window_size[1])
        low_p2 = ((p2[0] - center) * 1.5 + center, window_size[1])
        light_shines.append((p1, p2, low_p2, low_p1))

    bubbles = []
    for _ in range(20):
        pos = pg.Vector2(
            random.randint(20, window_size[0] - 20),
            random.randint(20, window_size[1] - 100),
        )
        radius = random.randint(5, 15)
        bubbles.append((pos, radius))
        
        for i in range(5):
            if radius < i*2:
                break
            offset = (random.random() - 0.5) * i*50
            bubbles.append((pos + pg.Vector2(offset, i*radius*2), radius - i*2))

generate()


pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Water")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - randomize scene
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


dark_overlay = pg.Surface(window_size)
for y in range(-25, window_size[1], 10):
    color = (int((y+25) / window_size[1] * 100),) * 3
    points = [(x, sin(x / 89) * 10 + y) for x in range(0, window_size[0]+30, 30)]
    points.insert(0, (0, window_size[1]))
    points.append(window_size)
    pg.draw.polygon(dark_overlay, color, points)
light_overlay = pg.Surface(window_size)

run = True
frame = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                generate()
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(water_color)
    for pos, rad in bubbles:
        offset = (sin(frame / 20 + pos.x) * 5, cos(frame / 25 + pos.y) * 3)
        pg.draw.circle(canvas, (255, 255, 255), pos+offset, rad, 2)
    
    for shine in light_shines:
        light_overlay.fill((0, 0, 0))
        p = [(x + sin(frame / 20 + x) * 5, y) for x, y in shine]
        pg.draw.polygon(light_overlay, light_color, p)
        canvas.blit(light_overlay, (0, 0), None, pg.BLEND_ADD)
    
    canvas.blit(dark_overlay, (0, 0), None, pg.BLEND_SUB)
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    frame += 1

pg.quit()
