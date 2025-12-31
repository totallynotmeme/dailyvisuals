import pygame as pg
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Beach")
clock = pg.time.Clock()

def sign(x):
    if x < 0:
        return -1
    return 1

color_sky = pg.Color(150, 210, 255)
color_sun = pg.Color(255, 255, 230)
color_bird = pg.Color(0, 0, 0)
color_sand = pg.Color(255, 230, 200)
color_water = pg.Color(60, 80, 230)
color_foam = pg.Color(120, 160, 255)
color_ship = pg.Color(180, 170, 170)
color_cloud = pg.Color(255, 255, 255)

color_sun_glow = color_sun.lerp(color_sky, 0.5)


birds_pos = (window_size[0] - 250, 180)
sun_pos = (window_size[0] - 150, 70)

horizon_y = int(window_size[1] / 2.3)
beach_edge_x = 150


cloud_points = [
    (80, 60),
    (window_size[0] // 6, 120),
    (window_size[0] // 3, 80),
    (window_size[0] // 2, 150),
]

edge_points = []
y = -1 / 1.1
ind = 0
while y + horizon_y < window_size[1]:
    y = y * 1.1 + 1
    ind += 1
    point = (beach_edge_x + math.sin(ind / 1.5) * y / 10, y + horizon_y)
    edge_points.append(point)

beach_points = edge_points.copy()
beach_points.insert(0, (0, horizon_y))
beach_points.append((0, window_size[1]))

ship_pos = (window_size[0] // 1.2, horizon_y + 5)
ship_points = [(ship_pos[0] + i[0], ship_pos[1] + i[1]) for i in (
    (-15, 0),
    (-20, -15),
    (-8, -15),
    (-8, -25),
    (-3, -25),
    (-3, -15),
    (20, -15),
    (15, 0),
)]


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_sky)
    pg.draw.rect(canvas, color_water, pg.Rect((0, horizon_y), window_size))
    pg.draw.polygon(canvas, color_sand, beach_points)
    
    # white wave-like stuff, foam i guess??
    wave_size = int(math.sin(t / 70) * 3 + 4)
    for x in range(wave_size):
        points = [(i[0] + x, i[1]) for i in edge_points]
        pg.draw.lines(canvas, color_foam, False, points, 5)
    
    # more foam
    range_y = (window_size[1] - horizon_y) / 2 - 50
    for x in range(beach_edge_x + 100, window_size[0], 30):
        origin_y = horizon_y + range_y/2 + 155
        origin_y += math.sin(x / 1.01) * range_y
        phase_1 = math.sin(x / 3 + t / 50) * 10 + 15
        phase_2 = math.sin(x / 3 + t / 50 + 0.5) * 10 + 15
        p_from = (x, origin_y - phase_1)
        p_to = (x, origin_y + phase_2)
        pg.draw.line(canvas, color_foam, p_from, p_to, 3)
    
    # ship in the bg
    points = [(i[0], i[1] + math.sin(t / 150) * 2) for i in ship_points]
    pg.draw.polygon(canvas, color_ship, points)
    
    # sun
    r = math.sin(t / 100) * 3 + 55
    pg.draw.circle(canvas, color_sun_glow, sun_pos, r)
    pg.draw.circle(canvas, color_sun, sun_pos, 50)
    
    # clouds
    for x, y in cloud_points:
        for ind in range(12):
            ind = ind / 4 + 0.1
            r = math.sin(ind) ** 2 * 20
            pg.draw.circle(canvas, color_cloud, (x, y), r)
            x += r
            y += math.sin(x/2 + t/50)
    
    # "and i-i don't know, simulate some.. birds... and add them!!!1"
    for shift_x in range(0, 150, 25):
        shift_y = shift_x // 3
        x = birds_pos[0] - shift_x
        y = birds_pos[1] + math.sin(t / 40 + x / 3) * 3
        wing_pos = 2 * sign(math.sin(t / 25 - shift_x / 50))
        
        this_y = y - shift_y
        pg.draw.line(canvas, color_bird, (x, this_y), (x-8, this_y + wing_pos), 3)
        pg.draw.line(canvas, color_bird, (x, this_y), (x+8, this_y + wing_pos), 3)
        if shift_x == 0:
            continue
        this_y = y + shift_y
        pg.draw.line(canvas, color_bird, (x, this_y), (x-8, this_y + wing_pos), 3)
        pg.draw.line(canvas, color_bird, (x, this_y), (x+8, this_y + wing_pos), 3)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
