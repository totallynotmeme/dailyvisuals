import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Fire/iceball")
clock = pg.time.Clock()


color_bg_fire = pg.Color(50, 20, 0)
color_bg_ice = pg.Color(0, 30, 50)
color_ball_fire = pg.Color(255, 200, 127)
color_ball_ice = pg.Color(230, 230, 255)
color_ball_edge_fire = pg.Color(255, 150, 0)
color_ball_edge_ice = pg.Color(0, 150, 255)
color_deco_fire = pg.Color(40, 40, 40)
color_deco_ice = pg.Color(200, 230, 255)
color_text = pg.Color(127, 127, 127)


window_center = pg.Vector2(window_size) / 2
ball_radius = min(window_center) / 2
line_width = window_size[1] // 10

line_pos = window_center.x
line_goal = window_center.x # gets set in the loop


mask = pg.Surface(window_size)
fire_buffer = pg.Surface(window_size)

decoration_circles = [pg.Vector2(-999999, 0)] * 40 # 40 circles buffer i guess
decoration_spikes = []

up = pg.Vector2(0, -1)
for i in range(10):
    pos = up.rotate(i * 36) * ball_radius / random.uniform(1.2, 2)
    decoration_spikes.append(window_center + pos)

grad_size_y = window_size[1] + 100
bg_gradient = pg.Surface((window_size[0], grad_size_y))
for i in range(11):
    c = 255 - i * 20
    y = grad_size_y * i / 10
    pg.draw.rect(bg_gradient, (c, c, c), pg.Rect(0, y, window_size[0], grad_size_y / 10))


up = pg.Vector2(0, -1)
unfocused_t = 0
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    unfocused_t += 1
    if pg.mouse.get_focused():
        line_goal = pg.mouse.get_pos()[0]
        unfocused_t = 0
    elif unfocused_t > 100:
        line_goal = window_center.x
    
    line_pos = (line_pos + line_goal) / 2
    real_ball_r = ball_radius + sin(t / 100) * 10
    
    if t % 10 == 0:
        shift = up.rotate(random.random() * 360) * (real_ball_r - 20)
        decoration_circles.append(window_center + shift)
        decoration_circles.pop(0)
    
    gradient_y = sin(t / 120) * 50 - 50
    
    
    # drawing ice (left)
    canvas.fill(color_bg_ice)
    canvas.blit(bg_gradient, (0, gradient_y), None, pg.BLEND_MULT)
    
    for ind, i in enumerate(decoration_circles):
        pg.draw.circle(canvas, color_deco_ice, i, ind//2 + 1)
    
    pg.draw.circle(canvas, color_ball_ice, window_center, real_ball_r)
    pg.draw.circle(canvas, color_ball_edge_ice, window_center, real_ball_r, 3)
    
    for ind, i in enumerate(decoration_spikes):
        points = (
            i + (-20, 0),
            i + (-10, 15 + sin(t/150 + ind) * 5),
            i + (0, 7),
            i + (10, 15 + sin(t/140 + ind + 3) * 5),
            i + (20, 0),
        )
        pg.draw.lines(canvas, color_ball_edge_ice, False, points, 3)
    
    
    # drawing fire (right)
    fire_buffer.fill(color_bg_fire)
    fire_buffer.blit(bg_gradient, (0, gradient_y), None, pg.BLEND_MULT)
    
    for ind, i in enumerate(decoration_circles): # a little bit of spaghetti
        pg.draw.circle(fire_buffer, color_deco_fire, i, ind//2 + 1)
        shift = (i - window_center).normalize()
        i += shift # shift now because it's not used until the next frame
    
    pg.draw.circle(fire_buffer, color_ball_fire, window_center, real_ball_r)
    pg.draw.circle(fire_buffer, color_ball_edge_fire, window_center, real_ball_r, 3)
    
    for ind, i in enumerate(decoration_spikes):
        points = (
            i + (-20, 10),
            i + (-10, -10 + sin(t/150 + ind) * 8),
            i + (0, 5),
            i + (10, -10 + sin(t/140 + ind + 3) * 8),
            i + (20, 10),
        )
        pg.draw.lines(fire_buffer, color_ball_edge_fire, False, points, 3)
    
    
    # applying the mask and merging the two planes of existence together
    mask.fill("white")
    pg.draw.rect(mask, "black", pg.Rect(line_pos, 0, window_size[0] - line_pos, window_size[1]))
    canvas.blit(mask, (0, 0), None, pg.BLEND_MULT)
    
    mask.fill("black")
    pg.draw.rect(mask, "white", pg.Rect(line_pos, 0, window_size[0] - line_pos, window_size[1]))
    fire_buffer.blit(mask, (0, 0), None, pg.BLEND_MULT)
    canvas.blit(fire_buffer, (0, 0), None, pg.BLEND_ADD)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
