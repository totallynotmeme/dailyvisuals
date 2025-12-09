import pygame as pg
from math import sin, pi
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Sunset")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - randomize clouds
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


window_size = pg.Vector2(window_size)
window_center = window_size / 2

sun_pos = pg.Vector2(window_center.x, window_center.y + 150)
water_line = sun_pos.y + 20
color_sun = pg.Color(255, 255, 200)
color_sky_far = pg.Color(220, 90, 100)
color_sky_near = pg.Color(100, 70, 130)
color_water = pg.Color(40, 70, 150)

color_ref_sun = color_sun.lerp(color_water, 0.5)
color_ref_cloudf = color_sky_near.lerp(color_water, 0.5)
color_ref_cloudb = color_sky_far.lerp(color_water, 0.5)


def draw_cloud_front(canvas, pos, size, t):
    shift = sin(t / 160 + pos[1]) * 4
    water_shift = sin(pos[1] / 10 - t / 70) * 10
    # real
    rect_front = pg.Rect((0, 0), size)
    rect_front.center = (pos[0] + shift, pos[1])
    pg.draw.rect(canvas, color_sky_near, rect_front)
    
    # reflection
    rect_front = pg.Rect((0, 0), (size[0], size[1] / 1.5))
    rect_front.center = (pos[0] + shift + water_shift, 1.5*water_line - pos[1]/2)
    pg.draw.rect(canvas, color_ref_cloudf, rect_front)

def draw_cloud_back(canvas, pos, size, t):
    shift = sin(t / 160 + pos[1]) * 4
    water_shift = sin(pos[1] / 10 - t / 70) * 10
    # real
    pos_back = (pg.Vector2(pos) + (shift, 0)).lerp(window_center, 0.03)
    size_back = pg.Vector2(size).lerp((0, 0), 0.03)
    
    rect_back = pg.Rect((0, 0), size_back)
    rect_back.center = pos_back
    pg.draw.rect(canvas, color_sky_far, rect_back)
    
    # reflection
    rect_back = pg.Rect((0, 0), (size_back[0], size_back[1] / 1.5))
    rect_back.center = (pos_back[0] + water_shift, 1.5*water_line - pos_back[1]/2)
    pg.draw.rect(canvas, color_ref_cloudb, rect_back)


def gen_clouds():
    global clouds
    
    clouds = []
    for _ in range(15):
        x = random.randint(150, window_size.x - 150)
        y = random.randint(50, water_line - 50)
        w = random.randint(75, 150)
        for i in range(w // 30):
            clouds.append(((x, y - i*15), (w - i*30, 20)))
gen_clouds()


sky = pg.Surface(window_size)
lines = int(sun_pos.y) + 20
for y in range(lines):
    l = window_center.x * (lines-y) / lines
    color = color_sky_near.lerp(color_sky_far,  y / lines)
    pg.draw.line(sky, color, (0, y), (window_size.x, y))

mask = pg.Surface(window_size)
mask.fill((155, 155, 155))
for r in range(100, 0, -1):
    c = 255 - r
    pg.draw.circle(mask, (c, c, c), sun_pos, r*5)
sky.blit(mask, (0, 0), None, pg.BLEND_MULT)
del mask

pg.draw.circle(sky, color_sun, sun_pos, 50)
pg.draw.rect(sky, color_water, pg.Rect(0, water_line, window_size.x, window_center.y - 170))


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                gen_clouds()
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(sky, (0, 0))
    points = []
    for i in range(10):
        y = i * 5 + water_line
        line_pos = sin(y / 10 - t / 70) * i * 3 + window_center.x
        line_width = sin(i * pi/20 + pi/2) * 46
        points.append((line_pos-line_width, y))
        points.insert(0, (line_pos+line_width, y))
    pg.draw.polygon(canvas, color_ref_sun, points)
    
    [draw_cloud_back(canvas, pos, size, t) for pos, size in clouds]
    [draw_cloud_front(canvas, pos, size, t) for pos, size in clouds]
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
