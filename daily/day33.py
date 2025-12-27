import pygame as pg
import random
from math import ceil


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Tunnel")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - randomize tunnel right now
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
up = pg.Vector2(0, -1)
scale = window_center.length() * 1.4

speed = 0
speed_wiggle = 0
sides = 4
zoom_factor = 1

speed_goal = 0.4
speed_wiggle_goal = -0.3
sides_goal = 10
zoom_factor_goal = 3

angle_shift = 0
far_shift = 0

resolution = 25
resolution_p1 = resolution + 1

poly_color1 = pg.Color(0, 127, 255)
hue1 = 90
hue1_goal = poly_color1.hsva[0]
poly_color2 = pg.Color(63, 0, 255)
hue2 = 180
hue2_goal = poly_color2.hsva[0]


run = True
t = 350
since_last_jump = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                t = 0
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    # smooth transition stuff
    speed = (speed * 9 + speed_goal) / 10
    speed_wiggle = (speed_wiggle * 9 + speed_wiggle_goal) / 10
    sides = (sides * 9 + sides_goal) / 10
    zoom_factor = (zoom_factor * 9 + zoom_factor_goal) / 10
    hue1 = (hue1 * 9 + hue1_goal) / 10
    hue2 = (hue2 * 9 + hue2_goal) / 10
    
    angle_shift += speed
    far_shift += speed_wiggle
    
    far_point = window_center + up.rotate(far_shift) * scale / 1.5
    
    for depth in range(resolution-1, 0, -1):
        colors = (
            poly_color1.lerp("black", depth / resolution),
            poly_color2.lerp("black", depth / resolution),
        )
        zoom_1 = (depth / resolution_p1) ** zoom_factor
        zoom_2 = ((depth+1) / resolution_p1) ** zoom_factor
        
        for angle in range(ceil(sides)):
            rot = angle_shift + 360 * angle / sides
            # surely there's a better way to do this... but im lazy
            pos1 = window_center + up.rotate(rot) * scale
            pos2 = window_center + up.rotate(rot + 360 / sides) * scale
            
            color = colors[angle % 2]
            
            this_point_1 = window_center.lerp(far_point, zoom_1)
            this_point_2 = window_center.lerp(far_point, zoom_2)
            
            points = [
                pos1.lerp(this_point_1, (depth) / resolution_p1),
                pos1.lerp(this_point_2, (depth+1) / resolution_p1),
                pos2.lerp(this_point_2, (depth+1) / resolution_p1),
                pos2.lerp(this_point_1, (depth) / resolution_p1),
            ]
            pg.draw.polygon(canvas, color, points)
    
    if since_last_jump < 60:
        poly_color1.hsva = (hue1, 100, 100, 100)
        poly_color2.hsva = (hue2, 100, 100, 100)
    
    if t < 0:
        sign = random.choice((1, -1))
        speed_goal = (random.random() / 2 + 0.2) * sign
        speed_wiggle_goal = (random.random() / 2 + 0.2) * -sign
        sides_goal = random.randint(3, 6) * 2
        zoom_factor_goal = random.random() * 5 + 2
        hue1_goal = random.randint(0, 360)
        hue2_goal = random.randint(0, 360)
        
        t = random.randint(300, 500)
        since_last_jump = 0
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t -= 1
    since_last_jump += 1

pg.quit()
