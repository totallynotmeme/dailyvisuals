import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Leve l0")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
D - force lights off (2 seconds)
F - toggle zoom
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


scale_factor = min(window_size)
shift_factor = max(window_size)
window_size = pg.Vector2(window_size)
window_center = window_size / 2

color_ceil = pg.Color(120, 110, 40)
color_wall = pg.Color(110, 120, 20)
color_floor = pg.Color(120, 110, 30)
color_black = pg.Color(0, 0, 0)
color_eyes = pg.Color(30, 5, 5)

def project(point, shift):
    proj = pg.Vector2(point[0], -point[1]) + shift
    proj *= scale_factor / ((point[2] + 1) ** zoom_factor - 0.9) / 5
    proj += window_center
    return proj

polygons = []
eyes = [
    # top left
    ((-2.0, 1.7, 24), (-1.9, 1.5, 24)),
    ((-1.7, 1.9, 24), (-1.6, 1.7, 24)),
    # bot left
    ((-1.8, -0.3, 32), (-1.4, -0.1, 32)),
    ((-1.7, -0.7, 33), (-1.3, -0.5, 33)),
    # mid
    ((-0.2, 0.8, 15), (-0.15, 0.5, 15)),
    ((0.2, 0.9, 15), (0.25, 0.6, 15)),
    # top right
    ((2.0, 1.8, 20), (1.9, 1.6, 20)),
    ((1.6, 1.9, 20), (1.5, 1.7, 20)),
    # mid
    ((1.2, -0.2, 29), (1.1, -0.5, 29)),
    ((1.6, -0.3, 28), (1.5, -0.6, 28)),
]

# floor
for z in range(25):
    polygons.append((
        color_floor.lerp("black", z/25),
        (-5, -2, z),
        (-5, -2, z+1),
        (5, -2, z+1),
        (5, -2, z),
    ))

# ceil
for z in range(25):
    polygons.append((
        color_ceil.lerp("black", z/25),
        (-5, 3, z),
        (-5, 3, z+1),
        (5, 3, z+1),
        (5, 3, z),
    ))

# light above us
poly_lamp = [
    (255, 255, 200),
    (-1.5, 3, 1.1),
    (-1.5, 3, 1.9),
    (1.5, 3, 1.9),
    (1.5, 3, 1.1),
]
polygons.append(poly_lamp)

# patching up holes
# left far
polygons.append((
    color_wall.lerp("black", 16/25),
    (-3, 3, 17),
    (-5, 3, 17),
    (-5, -2, 17),
    (-3, -2, 17),
))
# left near
polygons.append((
    color_wall.lerp("black", 5/25),
    (-3, 3, 6),
    (-5, 3, 6),
    (-5, -2, 6),
    (-3, -2, 6),
))
# right
polygons.append((
    color_wall.lerp("black", 10/25),
    (3, 3, 11),
    (5, 3, 11),
    (5, -2, 11),
    (3, -2, 11),
))

# left wall
for z in range(25):
    # holes
    if z in range(4, 6) or z in range(13, 17):
        continue
    polygons.append((
        color_wall.lerp("black", z/25),
        (-3, 3, z),
        (-3, 3, z+1),
        (-3, -2, z+1),
        (-3, -2, z),
    ))

# right wall
for z in range(25):
    # more holes
    if z in range(7, 11):
        continue
    polygons.append((
        color_wall.lerp("black", z/25),
        (3, 3, z),
        (3, 3, z+1),
        (3, -2, z+1),
        (3, -2, z),
    ))


zoom_factor = 1.0
zoom_goal = 1
lamp_off_t = 0

mousepos = pg.Vector2()
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_d:
                lamp_off_t = 120
            if ev.key == pg.K_f:
                zoom_goal = 1 - zoom_goal
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    
    mousepos = mousepos.lerp(pg.mouse.get_pos(), 0.3)
    shift = (mousepos - window_center) / shift_factor
    if zoom_goal == 0:
        shift *= 3
    zoom_factor = (zoom_factor * 3 + zoom_goal / 2 + 0.5) / 4
    
    canvas.fill((0, 0, 0))
    
    lamp_bright = 1 - random.random() / 50
    
    if random.random() < 0.003:
        lamp_off_t = random.randint(30, 120)
    
    if lamp_off_t > 0:
        lamp_off_t -= 1
        lamp_bright = 0.2
    
    for color, *poly in polygons:
        points = [project(i, shift) for i in poly]
        pg.draw.polygon(canvas, color_black.lerp(color, lamp_bright), points)
    
    # them
    eye_width = 2 + (1-zoom_goal) * 5
    if lamp_off_t > 0:
        shake = pg.Vector2(random.random()-0.5, random.random()-0.5) * eye_width
        for left, right in eyes:
            point_from = shake + project(left, shift)
            point_to = shake + project(right, shift)
            pg.draw.line(canvas, color_eyes, point_from, point_to, eye_width)
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
