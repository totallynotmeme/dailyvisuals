import pygame as pg
import random
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Lightning")
clock = pg.time.Clock()


def pseudoperlin(x, y):
    res = 0
    for i in range(1, 6):
        res += math.sin(x*i * 29 - y + i*i) / i
    return res


strike_y = window_size[1] - 105
lightning_shift = window_size[0] // 10

color_sky_light = pg.Color(0, 20, 40)
color_sky_dark = pg.Color(10, 0, 30)
color_ground_light = pg.Color(0, 40, 20)
color_ground_dark = pg.Color(10, 30, 0)
color_cloud = pg.Color(5, 10, 20)
color_lightning = pg.Color(200, 255, 255)

color_ground_lit = color_ground_light.lerp("white", 0.05)
color_lightning_glow = color_lightning.lerp(color_sky_light, 0.7)


lightning_end_origin = [pg.Vector2(x * window_size[0] / 4, strike_y) for x in (1, 2, 3)]
lightning_end = lightning_end_origin.copy()

lightning_start_origin = [pg.Vector2(x * window_size[0] / 4, 50) for x in (1, 2, 3)]
lightning_start = lightning_start_origin.copy()


background = pg.Surface(window_size)
# gradient
for y in range(0, window_size[1] + 500, 100):
    color = color_sky_light.lerp(color_sky_dark, y / (window_size[1] + 500))
    pg.draw.line(background, color, (0, y), (window_size[0], y-500), 101)

# ground
for y in range(0, 150, 25):
    color = color_ground_light.lerp(color_ground_dark, y/125)
    y += window_size[1]-150
    pg.draw.rect(background, color, pg.Rect(0, y, window_size[0], 25))

run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(background, (0, 0))
    
    # make lightnings shift every few seconds
    for i in range(3):
        if random.random() < 0.01:
            offset = random.randint(-lightning_shift, lightning_shift)
            lightning_start[i] = lightning_start_origin[i] + (offset, 0)
        if random.random() < 0.01:
            offset = random.randint(-lightning_shift, lightning_shift)
            lightning_end[i] = lightning_end_origin[i] + (offset, 0)
    
    # clouds
    for i in range(4):
        if i == 2:
            # lightnings in between clouds
            for start, end in zip(lightning_start, lightning_end):
                pg.draw.circle(canvas, color_ground_lit, end, 15)
                points = []
                points_l = []
                points_r = []
                for j in range(20+1):
                    j /= 20
                    factor = math.sin(j * math.pi) * 25
                    offset = pg.Vector2(pseudoperlin(j + start.x/19, t/5 + end.x/23), 0) * factor
                    p = start.lerp(end, j) + offset
                    points.append(p)
                    points_l.append(p + (-5, 0))
                    points_r.append(p + (5, 0))
                pg.draw.lines(canvas, color_lightning_glow, False, points_l, 5)
                pg.draw.lines(canvas, color_lightning_glow, False, points_r, 5)
                pg.draw.lines(canvas, color_lightning, False, points, 5)
        # clouds fr
        color = color_cloud.lerp("black", i/3)
        div_x = 7 + i*3
        div_t = 200 + i*10
        f_mult = 50 + i*5
        f_add = 100 + i*20
        y_pos = 200 - i*100
        for x in range(0, window_size[0], 75 + i*12):
            r = abs(math.sin(x / div_x + t / div_t) ** 2) * f_mult + f_add
            pg.draw.circle(canvas, color, (x, y_pos), r)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
