import pygame as pg
from math import sin
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Beam")
clock = pg.time.Clock()


window_center = pg.Vector2(window_size) / 2
ground_pos = window_center.y * 1.8
ground_rect = pg.Rect(0, ground_pos, *window_size)

color_background = pg.Color((0, 5, 20))
color_background_brighter = pg.Color((0, 8, 25))
color_accent = pg.Color((100, 200, 255))
color_ground = pg.Color((5, 10, 20))


glow = pg.Surface((window_size[0], 12))
for y in range(0, 12, 4):
    color = color_accent.lerp(color_ground, y/12)
    pg.draw.rect(glow, color, pg.Rect(0, y, window_size[0], 4))

beam_width = window_size[0] // 8
beam = pg.Surface((beam_width*2, window_size[1]))

background = pg.Surface(window_size)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    # redraw the BEAM
    if t % 40 == 0:
        # beam.fill("red") # making sure all of it is updated
        pg.draw.rect(beam, color_accent, pg.Rect(beam_width - 32, 0, 64, window_size[1]))
        for x in range(32, beam_width, 4):
            color = (x / beam_width) ** 0.5 + random.random() / 10
            color = color_accent.lerp("black", min(color, 1))
            x_right = beam_width + x + 1 # what the-
            x_left = beam_width - x - 3  # ...well, if it works it works
            pg.draw.line(beam, color, (x_right, 0), (x_right, window_size[1]), 4)
            pg.draw.line(beam, color, (x_left, 0), (x_left, window_size[1]), 4)
    
    if t % 60 == 0:
        # also redraw the background i guess
        background.fill(color_background)
        for real_x in range(20, window_size[0] + 70, 69):
            for real_y in range(50, window_size[1] + 60, 73):
                x = real_x + random.randint(-20, 20)
                y = real_y + random.randint(-20, 20)
                r = random.randint(50, 100)
                color = random.random()
                color = color_background.lerp(color_background_brighter, color)
                pg.draw.circle(background, color, (x, y), r)
    
    canvas.blit(background, (0, 0))
    
    # draw the beam- BUT FIRST DRAW THE WAVES!!
    for y in range(10, int(ground_pos), 20):
        x = beam_width
        x += sin(y + t / 50) * 5 + 5
        x += sin(y / 3.3 - t / 60) * 15 + 10
        pg.draw.line(canvas, "black", (window_center.x - x, y), (window_center.x + x, y), 20)
    
    canvas.blit(beam, beam.get_rect(midtop = (window_center.x, 0)))
    
    # glow
    y = int(ground_pos - sin(t / 100) * 6 - 6)
    canvas.blit(glow, (0, y))
    
    # dust?? from the BEAM
    for x in range(20 - beam_width, beam_width - 10, 10):
        x += window_center.x
        r = sin(t / 120 + x / 3) * 5 + 10
        pg.draw.circle(canvas, color_accent, (x, ground_pos - 5), r)
    
    # ground
    pg.draw.rect(canvas, color_ground, ground_rect)
    
    # ground glow
    for x in range(0, beam_width + 32, 8):
        factor = 1 - x / (beam_width + 32)
        color = color_ground.lerp(color_accent, factor ** 2 / 10)
        height = factor ** 0.5 * 64
        pg.draw.rect(canvas, color, pg.Rect(x + window_center.x, ground_pos, 8, height))
        pg.draw.rect(canvas, color, pg.Rect(window_center.x - x - 8, ground_pos, 8, height))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
