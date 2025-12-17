import pygame as pg
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Water grid")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
A - toggle antialiased lines
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
color_water_high = pg.Color(0, 127, 255)
color_water_low = pg.Color(0, 63, 127)

# sin() / 4 -> range [-0.25; 0.25]
# *2 -> [-0.5; 0.5], +0.5 -> [0; 1]
get_color_factor = lambda h: h * 2 + 0.5


class Camera:
    rot = pg.Vector2()
    speed = 0
    proj_x = 0
    proj_y = 0
    factor = 100
    
    def step(pos, rel):
        Camera.speed /= 1.1
        Camera.speed -= rel.x / window_size[0] / 3
        Camera.rot.x += Camera.speed
        raw_pos = min(max(pos[1] / window_size[1], 0), 1)
        angle = 3 - raw_pos * 1.5
        Camera.rot.y = (Camera.rot.y * 4 + angle) / 5
        
        Camera.proj_x2x = math.cos(Camera.rot.x)
        Camera.proj_y2x = -math.sin(Camera.rot.x)
        Camera.proj_x2y = math.sin(Camera.rot.x) / Camera.rot.y
        Camera.proj_y2y = math.cos(Camera.rot.x) / Camera.rot.y
    
    def project(point):
        ox, oy, z = point
        x = ox * Camera.proj_x2x + oy * Camera.proj_y2x
        y = ox * Camera.proj_x2y + oy * Camera.proj_y2y
        x = x * Camera.factor + window_center.x
        y = y * Camera.factor + window_center.y + z * Camera.factor
        return (x, y)


Camera.factor = max(window_center) / 10

water_size_x = 13 # actual value: this * 2 + 1
water_size_y = 13 # same here

water_height = {}
for x in range(-water_size_x, water_size_x+1):
    for y in range(-water_size_x, water_size_x+1):
        water_height[(x, y)] = 0


def draw_water_point(canvas, x, y):
    z = water_height[(x, y)]
    color = color_water_high.lerp(color_water_low, get_color_factor(z))
    p_this = Camera.project((x, y, z))
    
    if x < water_size_x: # line going towards X neighbour
        z = water_height[(x+1, y)]
        p_nearx = Camera.project((x+1, y, z))
        draw_line(canvas, color, p_this, p_nearx)
    
    if y < water_size_y: # line going towards Y neighbour
        z = water_height[(x, y+1)]
        p_neary = Camera.project((x, y+1, z))
        draw_line(canvas, color, p_this, p_neary)


line_funcs = {
    True: pg.draw.aaline,
    False: pg.draw.line,
}
antialiasing = True
draw_line = line_funcs[antialiasing]

run = True
t = 0
while run:
    mouserel = pg.Vector2()
    holding = pg.mouse.get_pressed()[0]
    for ev in pg.event.get():
        if ev.type == pg.MOUSEMOTION and holding:
            mouserel += ev.rel
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_a:
                antialiasing = not antialiasing
                draw_line = line_funcs[antialiasing]
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    Camera.step(pg.mouse.get_pos(), mouserel)
    for pos in water_height.keys():
        x, y = pos
        water_height[pos] = math.sin(x * 0.17 + y * 0.59 + t/20) / 4
    
    canvas.fill((0, 0, 0))
    
    for x in range(-water_size_x, water_size_x+1):
        for y in range(-water_size_x, water_size_x+1):
            draw_water_point(canvas, x, y)
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
