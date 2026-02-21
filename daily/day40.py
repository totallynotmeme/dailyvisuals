import pygame as pg
from math import sin
import random
from time import perf_counter as time


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("ZEROscapes")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
R - regenerate spikes
E - reset beat counter
Z - hide this text

CBF Detected, loser!
Click Between Frames is illegitimate and will not be allowed for use in Nullscapes.
Please disable the mod in order to continue playing.
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


def generate_spikes():
    global spike_data
    global floating_stuff
    
    spike_data = []
    for x in range(-100, window_size[0], 50):
        height = random.uniform(window_size[1] / 3, window_size[1] / 1.5)
        skew = height / 3 + random.random() * 50
        width = random.uniform(40, 70)
        
        spike_data.append((
            (x, window_size[1]), # botleft point
            (x + skew, window_size[1] - height), # top point
            (x + width, window_size[1]), # botright point
            (x + width/3, window_size[1]), # botmid point
        ))
    
    floating_stuff = []
    for i in range(20):
        origin = pg.Vector2(
            random.randint(0, window_size[0]),
            random.randint(0, window_size[1] / 2 + 100),
        )
        
        off1 = (random.uniform(-20, 0), random.uniform(0, 20))
        off2 = (random.uniform(5, 20), random.uniform(-20, -5))
        off3 = (random.uniform(0, 15), random.uniform(0, 20))
        
        floating_stuff.append((
            origin + off1,
            origin + off2,
            origin + off3,
        ))

generate_spikes()


# actually seconds per beat but who cares
bpm = 128 / 60
last_beat = 0
beat_fade = 0
beat_type = True

color_bg = pg.Color((20, 30, 40))
color_spikes = pg.Color((30, 50, 70))
color_ground = pg.Color((40, 60, 80))
color_sun = pg.Color((255, 255, 230))
color_black = pg.Color((0, 0, 0))

color_spikes_dark = color_spikes.lerp(color_bg, 0.5)

window_center = pg.Vector2(window_size) / 2
sun_pos = window_center + (0, 100)

ground_pos = sun_pos[1] + 100
ground_rect = pg.Rect(0, ground_pos, window_size[0], window_size[1] - ground_pos)

overlay = pg.Surface(pg.Vector2(window_size) * 1.05)


run = True
t_origin = time()
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                generate_spikes()
            if ev.key == pg.K_e:
                t_origin = time()
                last_beat = 0
                beat_fade = 0
                beat_type = True
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_bg)
    t = time() - t_origin
    
    
    # the sun
    for i in range(10):
        color = color_bg.lerp(color_sun, i / 15)
        r = window_size[1] / 2 + sin(i / 2 + t / bpm * 4) * 10 - i * 20
        pg.draw.circle(canvas, color, sun_pos, r)
    # the inner circle
    pg.draw.circle(canvas, color_sun, sun_pos, window_size[1] / 2 - 200)
    
    
    # the ground because i'm too lazy to make more than 1 layer of spikes
    pg.draw.rect(canvas, color_ground, ground_rect)
    
    
    # the floating spiky boys
    for p1, p2, p3 in floating_stuff:
        p1 = p1 + (0, sin(t / bpm * 4 + p3.x) * 20)
        p2 = p2 + (0, sin(t / bpm * 4 + p3.x) * 20)
        p3 = p3 + (0, sin(t / bpm * 4 + p3.x) * 20)
        pg.draw.polygon(canvas, color_spikes_dark, (p1, p2, p3))
        pg.draw.polygon(canvas, color_black, (p1, p2, p3), 1)
    
    # the spiky boys
    for botleft, raw_top, botright, botmid in spike_data:
        x, y = raw_top
        top = (x + sin(t / bpm * 4 + x) * 10, y)
        
        pg.draw.polygon(canvas, color_spikes, (botleft, top, botright))
        
        if beat_fade > 0:
            if beat_type: # 2nd beat - spike flash
                color = color_spikes.lerp(color_sun, beat_fade)
                pg.draw.polygon(canvas, color, (botleft, top, botmid))
            else: # 1st beat - backside spike flash
                color = color_spikes.lerp(color_sun, beat_fade / 4)
                pg.draw.polygon(canvas, color, (botmid, top, botright))
        
        pg.draw.line(canvas, color_black, top, botleft)
        pg.draw.line(canvas, color_black, top, botmid)
        pg.draw.line(canvas, color_black, top, botright)
    
    
    # beat nonsense
    if beat_fade > 0:
        if beat_type: # 2nd beat - screen flash as well
            glow = pg.transform.scale_by(canvas, 1 + beat_fade / 20)
            
            # making it darker ig
            c = beat_fade * 100
            overlay.fill((c, c, c))
            glow.blit(overlay, (0, 0), None, pg.BLEND_MULT)
            
            canvas.blit(glow, glow.get_rect(center=window_center), None, pg.BLEND_ADD)
            
        beat_fade -= 1/30
    
    if last_beat < t:
        last_beat += 2 / bpm
        beat_fade = 1
        beat_type = not beat_type
    
    # finally end of the code
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    

pg.quit()
