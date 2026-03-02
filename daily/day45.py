import pygame as pg
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Caustics")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
SPACE - render caustics
S - step 5 frames (when rendering)
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


ray_height = window_size[1] - 100
def extend_ray(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    angle_coeff = (y2 - y1) / (x2 - x1)
    x3 = x1 - ray_height * angle_coeff
    y3 = y1 + ray_height
    return x3, y3


color_background = pg.Color(50, 150, 230)
color_water_top = pg.Color(30, 170, 200)
color_water_bottom = pg.Color(0, 50, 100)
color_sand = pg.Color(150, 150, 100)
color_ray_realtime = pg.Color(150, 200, 100)
color_ray_render = pg.Color(20, 20, 5)


rays = pg.Surface(window_size)
ray_buffer = pg.Surface(window_size)
water_gradient = pg.Surface(window_size)
for i in range(30):
    color = color_water_top.lerp(color_water_bottom, i / 29)
    step = window_size[1] / 30
    pg.draw.rect(water_gradient, color, pg.Rect(0, step * i, window_size[0], step+1))

sand_rect = pg.Rect(0, window_size[1] * 0.9, window_size[0], window_size[1])
pg.draw.rect(water_gradient, color_sand, sand_rect)


render = False
just_switched = True # to set things up at first
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                render = not render
                just_switched = True
            if ev.key == pg.K_s and render:
                just_switched = True
                t += 5
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(water_gradient, (0, 0))
    
    # some nonsense to set the variables
    if just_switched:
        if render:
            resolution = window_size[0]
            rendered_x = 0
            rays.fill((0, 0, 0))
        else:
            resolution = window_size[0] // 10
        step = window_size[0] / (resolution - 1)
        points = [0] * resolution
    
    # updating and drawing the waves
    for i in range(resolution):
        x = i * step
        y = sin(t / 300 + x / 500) * 30
        y += sin(t / 83 + x / 49) * 2
        y += sin(-t / 60 + x / 30) * 1
        y += sin(t / 47 - x / 17) * 1
        points[i] = (x, y + 50)
    # actually filling the sky because it's a solid color so it's easier to draw
    pg.draw.polygon(canvas, color_background, [(0, 0)] + points + [(window_size[0], 0)])
    
    # drawing the RAYS
    if render:
        # rendering
        iters = min(100 - rendered_x, 10)
        # doing this so we can pg.BLEND_ADD the lines together
        # and make them glowy... idk i just like doing this.
        # this can probably be done with an alpha channel but i'm too lazy
        for _ in range(iters):
            ray_buffer.fill((0, 0, 0))
            # drawing multiple lines per buffer to make it a bit faster
            # hoping the lines won't overlap much
            # (overlapping lines on the same buffer won't get pg.BLEND_ADD'ed)
            for x in range(rendered_x, window_size[0] - 1, 100):
                p1 = points[x]
                p2 = points[x+1]
                x3, y3 = extend_ray(p1, p2)
                # changing aaline to line gives a neat effect if you make the lines wide
                pg.draw.aaline(ray_buffer, color_ray_render, p1, (x3, y3))
            rays.blit(ray_buffer, (0, 0), None, pg.BLEND_ADD)
            rendered_x += 1
        
        canvas.blit(rays, (0, 0), None, pg.BLEND_ADD)
    else:
        # realtime
        for p1, p2 in zip(points, points[1:]):
            x3, y3 = extend_ray(p1, p2)
            pg.draw.aaline(canvas, color_ray_realtime, p1, (x3, y3))
    
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    
    # more nonsense just for fun
    if not render:
        t += 1
    just_switched = False

pg.quit()
