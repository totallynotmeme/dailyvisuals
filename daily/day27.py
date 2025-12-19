import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Untiling")
clock = pg.time.Clock()


class Tile:
    gravity = pg.Vector2(0, 0.3)
    def __init__(self, x, y, size_x, size_y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.vel.x = random.random() * 16 - 8
        self.vel.y = -random.random() * 20
        self.size = pg.Vector2(size_x, size_y)
    
    def t_to_factor(self, t):
        t -= (burst_origin - self.pos).length() / 10
        t = max(t, 0)
        return (t / 20) ** 2
    
    def draw(self, canvas, color, t):
        t = self.t_to_factor(t)
        size = self.size / (1 + t / 10)
        rect = pg.Rect(self.pos - size/2, size)
        color_factor = min(max(t / 100, 0), 1)
        color = color.lerp("black", color_factor)
        pg.draw.rect(canvas, color, rect, 0, int(t))
    
    def step(self, t):
        t = self.t_to_factor(t)
        if t > 15:
            self.vel += Tile.gravity
            self.pos += self.vel
        return self.pos.y < window_size[1] + 100


tiles = []
t_size_x = 50
t_offs_x = -15
t_size_y = 50
t_offs_y = -37
burst_origin = pg.Vector2()

color_from = pg.Color(0)
color_to = pg.Color(0)


run = True
t = 0
do_redraw = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    if do_redraw:
        t = 0
        color_from = pg.Color(color_to) # copying the color
        hue = color_to.hsva[0] + random.randint(60, 240)
        color_to.hsva = (hue % 360, 75, 75, 100)
        
        t_size_x = random.randint(30, 150)
        t_size_y = random.randint(30, 150)
        t_offs_x = -int(t_size_x * random.random())
        t_offs_y = -int(t_size_y * random.random())
        
        burst_origin = pg.Vector2(window_size)
        burst_origin.x *= random.random()
        burst_origin.y *= random.random()
        
        tiles = []
        for x in range(t_offs_x, window_size[0]+t_size_x, t_size_x):
            for y in range(t_offs_y, window_size[1]+t_size_y, t_size_y):
                tiles.append(Tile(x, y, t_size_x, t_size_y))
    
    canvas.fill(color_to)
    
    do_redraw = True
    for ind, i in enumerate(tiles):
        if i is None:
            continue
        do_redraw = False
        i.draw(canvas, color_from, t)
        if not i.step(t):
            tiles[ind] = None # gone
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
