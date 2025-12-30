import pygame as pg
import random
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Night road")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - re-generate terrain
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


window_center = pg.Vector2(window_size) / 2
scale_factor = min(window_size) / 4
mouse_pos = pg.Vector2(0, 0)

color_sky = pg.Color(0, 5, 20)
color_ground = pg.Color(20, 15, 10)
color_star1 = pg.Color(255, 240, 220)
color_star2 = pg.Color(220, 240, 255) # also moon color

color_tree = pg.Color(0, 0, 0)
color_road_black = pg.Color(0, 2, 5)
color_road_yellow = pg.Color(60, 50, 10)
color_road_white = pg.Color(50, 50, 55)


class Camera:
    rot_x = 0
    rot_y = 0
    pos = pg.Vector3(0, 5, -20)


def project(point):
    point = -Camera.pos + point
    point.rotate_y_ip(Camera.rot_x)
    point.rotate_x_ip(Camera.rot_y)
    
    if point.z < 0.01:
        return (-1, -1)
    x = (point.x * 5) / (point.z + 5)
    y = (-point.y * 5) / (point.z + 5)
    x *= scale_factor
    x += window_center.x
    y *= scale_factor
    y += window_center.y
    return (x, y)


data_road = [
    # (width, color),
    (0.2, color_road_black),
    (0.3, color_road_yellow),
    (5, color_road_black),
    (0.5, color_road_white),
]


def gen_terrain():
    global data_stars
    global data_trees
    
    data_stars = [] # (pos, color),
    for i in range(500):
        point = pg.Vector3(0, 0, 5000)
        point.rotate_y_ip(random.uniform(-55, 55))
        point.rotate_x_ip(random.uniform(-0.1, -40))
        color = color_star1.lerp(color_star2, random.random())
        data_stars.append((point, color))

    data_trees = [] # pos,
    for i in range(100):
        x = random.uniform(8, 50) * random.choice([-1, 1])
        y = 0
        z = random.uniform(0, 200)
        data_trees.append(pg.Vector3(x, y, z))

gen_terrain()


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                gen_terrain()
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    mouse_pos = mouse_pos.lerp(window_center - pg.mouse.get_pos(), 0.2)
    
    Camera.rot_x = mouse_pos.x * 40 / window_size[0]
    Camera.rot_y = mouse_pos.y * 20 / window_size[1]
    Camera.pos.x = mouse_pos.x * 5 / window_size[0]
    Camera.pos.y = 5 - mouse_pos.y * 2 / window_size[0]
    
    canvas.fill(color_sky)
    
    # stars
    ind = 0 # too lazy to enumerate()
    for pos, color in data_stars:
        p = project(pos)
        phase = abs(math.sin(ind + t / 60)) / 2
        pg.draw.circle(canvas, color.lerp(color_sky, phase), p, 2)
        ind += 1
    
    # moon, drawing it after stars so they dont peek from the... C <-- this part
    moon_pos = project((500, 500, 1500))
    pg.draw.circle(canvas, color_star2, moon_pos, 20)
    pg.draw.circle(canvas, color_sky, moon_pos + pg.Vector2(-7, -2), 20)
    
    # ground
    ground_pos = project((0, 0, 8000))
    rect = pg.Rect(
        0, ground_pos[1],
        window_size[0], window_size[1],
    )
    pg.draw.rect(canvas, color_ground, rect)
    
    # road
    x = 0
    for width, color in data_road:
        # right side
        pg.draw.polygon(canvas, color, (
            project((x, 0.1, -17.2)),
            project((x+width, 0.1, -17.2)),
            project((x+width, 0.1, 8000)),
            project((x, 0.1, 8000)),
        ))
        # left side
        pg.draw.polygon(canvas, color, (
            project((-x, 0.1, -17.2)),
            project((-x-width, 0.1, -17.2)),
            project((-x-width, 0.1, 8000)),
            project((-x, 0.1, 8000)),
        ))
        x += width
    
    # trees
    for pos in data_trees:
        # just a flat 2d poly because i don't want to spend too much time on this
        pg.draw.polygon(canvas, color_tree, (
            project(pos + (-1, 0, 0)),
            project(pos + (-0.9, 7, 0)),
            project(pos + (-3, 7, 0)),
            project(pos + (-1.1, 10, 0)),
            project(pos + (-2.5, 10, 0)),
            project(pos + (0, 13, 0)),
            project(pos + (2.5, 10, 0)),
            project(pos + (1.1, 10, 0)),
            project(pos + (3, 7, 0)),
            project(pos + (0.9, 7, 0)),
            project(pos + (1, 0, 0)),
        ))
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
