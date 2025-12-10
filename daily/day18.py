import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Night sky")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - regenerate sky
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


color_blue = pg.Color((150, 210, 255))
color_orang = pg.Color((255, 190, 130))


background = pg.Surface(window_size)
def gen_sky():
    global stars
    global background
    
    stars = []
    for _ in range(window_size[0] * window_size[1] // 5000):
        pos = (random.randint(0, window_size[0]), random.randint(0, window_size[1]))
        size = random.randint(1, 3)
        color = color_blue.lerp(color_orang, random.random())
        stars.append((color, pos, size))
    
    # drawing the nebula-ish thing?
    buffer_surf = pg.Surface(window_size)
    background.fill((0, 0, 0, 255))
    for _ in range(5):
        color_nebula_1 = pg.Color(0)
        color_nebula_2 = pg.Color(0)
        
        center = pg.Vector2(random.randint(0, window_size[0]),
                            random.randint(0, window_size[1]))
        size = (random.randint(window_size[0] // 10, window_size[0] // 3),
                random.randint(window_size[0] // 10, window_size[1] // 3))
        
        color_nebula_1.hsva = (random.randint(0, 360), 75, 3)
        color_nebula_2.hsva = (random.randint(0, 360), 75, 3)
        buffer_surf.fill((0, 0, 0))
        for i in range(150):
            pos = center + (random.randint(-size[0], size[0]),
                            random.randint(-size[1], size[1]))
            color = color_nebula_1.lerp(color_nebula_2, random.random())
            r = random.randint(min(size) // 2, max(size) // 2)
            pg.draw.circle(buffer_surf, color, pos, r)
            if i % 6 == 5:
                background.blit(buffer_surf, (0, 0), None, pg.BLEND_ADD)
                buffer_surf.fill((0, 0, 0))
    
gen_sky()
buffer_surf = pg.Surface(window_size)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                gen_sky()
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(background, (0, 0))
    buffer_surf.fill((0, 0, 0))
    
    ind = 0
    for color, pos, r in stars:
        factor = (ind / 7.1415 + t / (100 * r)) % 1
        factor = min(factor, 0.5) - max(factor, 0.5) + 0.5
        color = color.lerp("black", factor)
        pg.draw.circle(buffer_surf, color, pos, r)
        ind += 1
    
    canvas.blit(buffer_surf, (0, 0), None, pg.BLEND_MAX)
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
