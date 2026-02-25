import pygame as pg
import random
from math import sin, copysign


# idea given to me by a random person on discord (if you see this, you know who you are)
# tried to make something else, but then added .rotate() for funzies and got... this.
# it actually looks amazing so im not complaining-

# (just ignore the random flashes that can happen)

window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Kaleidoscope")
clock = pg.time.Clock()


colors = [
    pg.Color(150, 40, 210), # purple
    pg.Color(50, 230, 30), # green
    pg.Color(200, 120, 50), # orange to mix things up
]

window_center = pg.Vector2(window_size) / 2

dark_thing = pg.Surface(window_size)
dark_thing.fill((10, 10, 10))

circles = []
for _ in range(20):
    # doing this with vectors so it's easy to modify in place, i guess??
    pos = pg.Vector2(window_center)
    pos.x *= random.random()
    pos.x += window_center.x / 2
    pos.y *= random.random()
    pos.y += window_center.y / 2
    
    vel = pg.Vector2()
    vel.x = random.uniform(1, 4) * random.choice([1, -1])
    vel.y = random.uniform(1, 4) * random.choice([1, -1])
    
    col = pg.Vector3() # x = 0-255 color progress, y = color id, z = color speed
    col.x = random.random() * 255
    col.y = random.randint(0, len(colors)-1)
    col.z = random.random() * 3 + 1
    
    circles.append((pos, vel, col))


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(dark_thing, (0, 0), None, pg.BLEND_SUB)
    rotated = pg.transform.rotate(canvas, sin(t / 200) * 9.9 + 10)
    canvas.blit(rotated, rotated.get_rect(center=window_center))
    
    for pos, vel, col in circles:
        pos += vel
        # bounce
        if pos.x < 0:
            vel.x = copysign(random.uniform(1, 4), -vel.x)
            pos.x += 3
        if pos.x > window_size[0]:
            vel.x = copysign(random.uniform(1, 4), -vel.x)
            pos.x -= 3
        if pos.y < 0:
            vel.y = copysign(random.uniform(1, 4), -vel.y)
            pos.y += 3
        if pos.y > window_size[1]:
            vel.y = copysign(random.uniform(1, 4), -vel.y)
            pos.y -= 3
        # change color
        col.x += col.z
        if col.x >= 255:
            col.x %= 255
            col.y = (col.y + 1) % len(colors)
            col.z = random.random() * 3 + 1
        # calculate the real color
        next_color = colors[int(col.y + 1) % len(colors)] # spaghetti on top of-
        color = colors[int(col.y)].lerp(next_color, col.x / 255)
        # draw the thing!!1
        pg.draw.circle(canvas, color, pos, 10)
    
    # copy the canvas so it looks kinda kaleidoscop'ish???
    canvas.blit(pg.transform.flip(canvas, True, False), (0, 0), None, pg.BLEND_MAX)
    canvas.blit(pg.transform.flip(canvas, False, True), (0, 0), None, pg.BLEND_MAX)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
