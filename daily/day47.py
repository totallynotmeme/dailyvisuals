import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Graph")
clock = pg.time.Clock()
font = pg.font.SysFont("consolas", 15)


color_graph = pg.Color(0, 100, 200)
color_accent = pg.Color(50, 200, 255)

point_step = 64
window_center = pg.Vector2(window_size) / 2
max_points = int(window_size[0] / point_step + 0.999) # math.ceil doesn't exist

points = []
labels = []
state = "making" # / "labeling" / "showing" / "erasing"
# it would be alot better to use STATE_MAKING, STATE_SHOWING... enum for state
# but it's not like this is some enterprise level code i have to maintain
state_t = 0
label_chars = "<^>v"
label_showing = 0
label_length = 10

# uhhh don't worry about it
silly_thing = None
silly_thing_t = 0


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    if state == "making":
        while state_t <= 0:
            x = len(points) * point_step
            y = random.randint(0, window_size[1])
            factor = abs(window_center.x - x) / window_center.x
            y = y * (1 - factor) + window_center.y * factor
            
            state_t += factor * 3
            
            points.append(pg.Vector2(x, y))
            if x >= window_size[0]:
                state = "labeling"
                for i in range(5):
                    ind = random.uniform(i, i+0.9) * max_points / 6
                    label_point = points[int(ind)]
                    label_name = "".join(random.choice(label_chars) for _ in range(label_length-2))
                    label_name = "[" + label_name + "]"
                    labels.append((label_point, label_name))
                state_t = 6
    elif state == "labeling":
        if state_t <= 0:
            state_t = 6
            label_showing += 1
            if label_showing >= 10:
                state = "showing"
                state_t = 241
    elif state == "showing":
        if state_t <= 0:
            state = "erasing"
            state_t = 6
    elif state == "erasing":
        if state_t % 3 == 0:
            points.pop(0)
            
            if len(points) == 0:
                state = "making"
                labels = []
                label_showing = 0
        
        if state_t == 0:
            state_t = 6
            label_showing = max(label_showing - 1, 0)
    
    state_t -= 1
    for i in points:
        i.y += sin(t / 60 + i.x / 3) / 10
        # also draw a line while we're here
        pg.draw.line(canvas, color_graph, i, (i.x, window_size[1]))
    
    for p1, p2 in zip(points, points[1:]):
        pg.draw.aaline(canvas, color_graph, p1, p2)
    
    for point, text in labels:
        text = text[:label_showing]
        txt = font.render(text, True, color_accent)
        rect = txt.get_rect(midleft = point + (5, 0))
        pg.draw.rect(canvas, (0, 0, 0), rect)
        canvas.blit(txt, rect)
    
    # just for funzies TOTALLY NOT FORESHADOWING
    silly_thing_t -= 1
    if silly_thing_t < 0:
        chars = "0123456789ABCDEF"
        silly_thing = "".join(random.choice(chars) for _ in range(16))
        silly_thing_t = 20
    
    txt = font.render(f"graph.OS state | {state}", True, color_accent)
    canvas.blit(txt, (5, 5))
    txt = font.render(f"points alive   | {len(points)}", True, color_accent)
    canvas.blit(txt, (5, 25))
    txt = font.render(f"label showing  | {label_showing}", True, color_accent)
    canvas.blit(txt, (5, 45))
    txt = font.render(f"random numbers | {silly_thing}", True, color_accent)
    canvas.blit(txt, (5, 65))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
