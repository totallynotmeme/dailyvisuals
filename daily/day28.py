import pygame as pg
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Green thing") # i still don't know what it is
clock = pg.time.Clock()
font = pg.font.SysFont("consolas", 35)


window_half = pg.Vector2(window_size) / 2
green_thing_pos = int(window_size[1] / 1.7)

color_sky = pg.Color(100, 200, 255)
color_sun = pg.Color(255, 255, 230)
colors_green_thing = [
    pg.Color(30, 150, 30),
    pg.Color(35, 160, 35),
    pg.Color(25, 140, 25),
]
color_sun_glow = color_sky.lerp(color_sun, 0.2)
color_shadow = colors_green_thing[0].lerp("black", 0.1)

txt1 = font.render("it's 3:52 AM, idk what to do today", True, color_shadow)
txt2 = font.render("sry if this looks kinda empty lol", True, color_shadow)


blades = []
ind = 0
for x in range(25, window_size[0]-12, 25):
    if ind % 2 == 0:
        h = 70 * sin(x/20 + 0.2) + 5 * sin(x/50 - 1.5) + 110
    else:
        h = 60 * sin(x/20 - 3) + 110
    blades.append((x, h))
    ind += 1
    


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_sky)
    
    r = 120 + sin(t/60+0.2) * 3
    pg.draw.circle(canvas, color_sun_glow, (window_size[0] / 1.2, 0), r)
    r = 100 + sin(t/60) * 3
    pg.draw.circle(canvas, color_sun, (window_size[0] / 1.2, 0), r)
    
    pg.draw.rect(canvas, colors_green_thing[0],
                 pg.Rect(0, green_thing_pos, window_size[0], window_size[1]))
    
    ind = 0
    for x, height in blades:
        color = colors_green_thing[ind % 3]
        y_pos = (sin(x/5)+1) * 5
        p_to = (x, green_thing_pos - y_pos)
        p_to_shadow = (x - y_pos/5, green_thing_pos + y_pos/2)
        for i in range(10):
            p_from = p_to
            p_from_shadow = p_to_shadow
            x_pos = x + sin(i / 10 - t / 100 - x/7) * i
            y_pos = height*i/10
            p_to = (x_pos, green_thing_pos - y_pos)
            p_to_shadow = (x_pos - y_pos/5, green_thing_pos + y_pos/2)
            pg.draw.line(canvas, color_shadow, p_from_shadow, p_to_shadow, 25 - i*2)
            pg.draw.line(canvas, color, p_from, p_to, 25 - i*2)
        ind += 1
    
    pos1 = (window_half.x + sin(t/87) * 20, window_half.y * 1.7 + sin(t/140 + 3) * 20)
    pos2 = (window_half.x + sin(t/87 + 1) * 20, window_half.y * 1.7 + sin(t/140 + 4) * 20 + 50)
    canvas.blit(txt1, txt1.get_rect(center=pos1))
    canvas.blit(txt2, txt2.get_rect(center=pos2))
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
