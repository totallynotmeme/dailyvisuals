import pygame as pg
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Iceberg")
clock = pg.time.Clock()


class Triangle:
    def __init__(self, pos_x, width, height, water_h, c_light, c_dark, lerp=0.33):
        self.p_left = pg.Vector2(pos_x - width, water_h)
        self.p_top = pg.Vector2(pos_x, water_h - height)
        self.p_right = pg.Vector2(pos_x + width, water_h)
        self.p_mid = self.p_left.lerp(self.p_right, lerp)
        self.c_light = c_light
        self.c_dark = c_dark
    
    def draw(self, canvas, x):
        offset = (x, 0)
        p = (self.p_left + offset, self.p_top + offset, self.p_mid + offset)
        pg.draw.polygon(canvas, self.c_light, p)
        p = (self.p_mid + offset, self.p_top + offset, self.p_right + offset)
        pg.draw.polygon(canvas, self.c_dark, p)


window_center = pg.Vector2(window_size) / 2

color_sky = pg.Color(120, 230, 250)
color_water = pg.Color(150, 200, 255)

color_ice_lit = pg.Color(230, 240, 255)
color_ice_med = pg.Color(120, 180, 220)
color_ice_dark = pg.Color(30, 130, 200)
color_ice_black = pg.Color(5, 30, 50)

color_fih = pg.Color(0, 0, 0)
color_cloud = pg.Color(255, 255, 255)


water_pos = window_size[1] // 2 - 50
water_size = window_size[1] - water_pos

iceberg = []
# top
for x, h in [(135, 180), (-120, 210), (0, 320)]:
    x += window_center.x
    iceberg.append(Triangle(
        x, h/2, h, water_pos,
        color_ice_lit, color_ice_med
    ))
# bottom
iceberg.append(Triangle(
    window_center.x, 224, -500, water_pos,
    color_ice_dark, color_ice_black, lerp=0.38
))
iceberg.append(Triangle(
    window_center.x + 70, 80, -250, water_pos,
    color_ice_med, color_ice_black
))
iceberg.append(Triangle(
    window_center.x - 90, 120, -200, water_pos,
    color_ice_med, color_ice_black
))


water_mask = pg.Surface((window_size[0], water_size))
color_water_top = pg.Color(100, 230, 230)
color_water_bot = pg.Color(0, 50, 50)
for y in range(water_size):
    color = color_water_top.lerp(color_water_bot, y / water_size)
    pg.draw.line(water_mask, color, (0, y), (window_size[0], y))

brightness_mask = pg.Surface(window_size)
for i in range(255, 0, -20):
    c = 255 - i / 5
    r = (i/255) ** 0.5 * 255
    r *= max(window_size) / 360
    pg.draw.circle(brightness_mask, (c, c, c), window_center, r)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill(color_sky)
    pg.draw.rect(canvas, color_water, pg.Rect(0, water_pos, window_size[0], water_size))
    
    # you know what that means, FISH-
    for x in range(200, 350, 17):
        y = sin(x) * 40 + sin(t/20 + x) * 2 + water_pos + 150
        p = [(x-5, y-4), (x, y-2), (x+5, y-4), (x+10, y-1),
             (x+10, y+1), (x+5, y+4), (x, y+2), (x-5, y+4)]
        pg.draw.polygon(canvas, color_fih, p)
    for x in range(150, 350, 17):
        x = window_size[0] - x
        y = sin(x) * 45 + sin(t/20 + x) * 3 + water_pos + 210
        p = [(x+5, y-4), (x, y-2), (x-5, y-4), (x-10, y-1),
             (x-10, y+1), (x-5, y+4), (x, y+2), (x+5, y+4)]
        pg.draw.polygon(canvas, color_fih, p)
    
    # berg of ice
    for i in iceberg:
        i.draw(canvas, sin(t/200) * 20)
    
    # clouds
    for x in range(0, window_size[0]+1, 50):
        r = 80
        r += sin(x/20 + t/70) * 5
        r += sin(x/35 - t/100) * 10
        r += sin(x / 100 + t/150) * 15
        r *= (sin(x / 200 + t/350) ** 2 + sin(x / 150 - t/400) ** 2) / 2
        pg.draw.circle(canvas, color_cloud, (x, -10), r)
    
    # post-processing... in python. why am i doing this to myself
    canvas.blit(brightness_mask, (0, 0), None, pg.BLEND_MULT)
    canvas.blit(water_mask, (0, water_pos), None, pg.BLEND_MULT)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
