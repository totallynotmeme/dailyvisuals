import pygame as pg
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Sky")
clock = pg.time.Clock()


window_center = pg.Vector2(window_size) / 2

color_sky_top = pg.Color(50, 75, 150)
color_sky_bot = pg.Color(100, 150, 255)
color_sun = pg.Color(255, 255, 200)
color_cloud_near = pg.Color(255, 255, 255)
color_cloud_far = pg.Color(250, 230, 200)

color_sky_average = color_sky_bot.lerp(color_sky_top, 0.5)
color_sun_glow1 = color_sky_average.lerp(color_sun, 0.2)
color_sun_glow2 = color_sky_average.lerp(color_sun, 0.4)

sky = pg.Surface(window_size)
limit = window_size[1] + 50
for y in range(0, limit+1, 50):
    color = color_sky_top.lerp(color_sky_bot, y/limit)
    points = [
        (0, y-100),
        (0, y),
        (window_size[0], y+100),
        (window_size[0], y),
    ]
    pg.draw.polygon(sky, color, points)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(sky, (0, 0))
    
    # sun
    pg.draw.circle(canvas, color_sun_glow1, window_center, 172 + sin(t/50-0.5) * 7)
    pg.draw.circle(canvas, color_sun_glow2, window_center, 162 + sin(t/50) * 5)
    pg.draw.circle(canvas, color_sun, window_center, 150)
    
    # clouds
    for i in range(5, -1, -1):
        color = color_cloud_near.lerp(color_cloud_far, i/5)
        y = window_center.y * 15 / (7 + i)
        y_delta = window_center.y * 15 / (6 + i) - y
        for x in range(0, window_size[0] + 70, int(y_delta)):
            factor = i ** 2 * 5 + 20
            wavy = sin(x / 20 - t / factor) * 5
            wavy += sin(x / 50 + t / factor / 2) * 3
            pg.draw.circle(canvas, color, (x, y), wavy + y_delta)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
