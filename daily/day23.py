import pygame as pg


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Fractals")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
that's a lot of controls...
Hold 1/2/3 - select and drag monitor
Left/Right mouse button - draw white/black
Scroll wheel - change brush size
A/D - rotate
W/S - scale
Q - toggle smooth scale
P - print monitor positions
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


center_x, center_y = pg.Vector2(window_size) / 2

class Monitor:
    smooth = True
    funcmap = {
        True: pg.transform.smoothscale_by,
        False: pg.transform.scale_by,
    }
    
    def __init__(self):
        self.pos = (0, 0)
        self.scale = 0.2
        self.rot = 0
    
    def __repr__(self):
        return f"<Monitor @ {self.pos} {self.scale} {self.rot}>"
    
    def draw(self, target, surf, draw_rect):
        do_copy = True
        if self.scale != 1:
            do_copy = False
            surf = Monitor.funcmap[Monitor.smooth](surf, self.scale)
        if draw_rect:
            surf = surf.copy()
            rect = surf.get_rect()
            rect.x += 1
            rect.y += 1
            rect.w -= 2
            rect.h -= 2
            pg.draw.rect(surf, (255, 0, 0), rect, 1)
        if self.rot != 0:
            do_copy = False
            surf = pg.transform.rotate(surf, self.rot)
        target.blit(surf, surf.get_rect(center=self.pos), None, pg.BLEND_ADD)

monitors = []
monitor_map = {}
for i in range(1, 4):
    a = Monitor()
    a.pos = (window_size[0] * i / 4, window_size[1] / 2)
    monitors.append(a)
    monitor_map[pg.K_0 + i] = a

overlay = pg.Surface(window_size)
overlay.set_alpha(150)


last = 0
selected = None
rot_speed = 0.1
scale_speed = 0.001
reset_rot_speed = True
reset_scale_speed = True
brush = 21

run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.MOUSEWHEEL:
            brush += ev.y * 5
            brush = min(max(brush, 1), 500)
        if ev.type == pg.KEYDOWN:
            # check if we're trying to select a monitor
            for key, val in monitor_map.items():
                if ev.key == key:
                    if last == val:
                        selected = None
                    else:
                        selected = val
                    last = selected
            if ev.key == pg.K_q:
                Monitor.smooth = not Monitor.smooth
            if ev.key == pg.K_p:
                for ind, i in enumerate(monitors, start=1):
                    print(f"{ind} -> {i}")
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    mouse = pg.mouse.get_pressed()
    if mouse[0]: # left
        rect = pg.Rect(0, 0, brush, brush)
        rect.center = pg.mouse.get_pos()
        pg.draw.rect(overlay, (255, 255, 255), rect)
    if mouse[2]: # right
        rect = pg.Rect(0, 0, brush, brush)
        rect.center = pg.mouse.get_pos()
        pg.draw.rect(overlay, (0, 0, 0), rect)
    
    canvas.blit(overlay, (0, 0))
    
    keys = pg.key.get_pressed()
    reset_rot_speed = True
    reset_scale_speed = True
    
    if selected:
        selected.pos = pg.mouse.get_pos()
        if keys[pg.K_a]:
            selected.rot += rot_speed
            reset_rot_speed = False
        if keys[pg.K_d]:
            selected.rot -= rot_speed
            reset_rot_speed = False
        selected.rot %= 360
        if keys[pg.K_w]:
            selected.scale += scale_speed
            selected.scale = min(selected.scale, 2)
            reset_scale_speed = False
        if keys[pg.K_s]:
            selected.scale -= scale_speed
            selected.scale = max(selected.scale, 0.01)
            reset_scale_speed = False
    
    rot_speed = min(rot_speed + 0.05, 10)
    scale_speed = min(scale_speed + 0.001, 0.05)
    if reset_rot_speed:
        rot_speed = 0.1
    if reset_scale_speed:
        scale_speed = 0.001
    
    surf = canvas.copy()
    for i in monitors:
        i.draw(canvas, surf, i == selected)
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
