import pygame as pg
import random
import math


window_size = (1600, 900)

class Stripe:
    c_from = pg.Color((100, 255, 100))
    c_to = pg.Color((255, 255, 100))
    color = lambda x: Stripe.c_from.lerp(Stripe.c_to, min(abs(x / 10), 1))
    
    def __init__(self, x, y):
        self.pos = pg.Vector3((x, y, 0))
        #self.t = random.random() * 3.1415 * 2
        self.t = x * 2
    
    def draw(self, canvas):
        col = Stripe.color(self.pos.z)
        for i in range(10, -1, -1):
            adder = 2 + i / (25 - self.pos.y)
            lerp = i/20
            proj_height = 100 * self.pos.z / (adder + self.pos.y)
            proj_width = 80 / (adder + self.pos.y)
            proj_x = 5 * self.pos.x / (adder + self.pos.y) - proj_width/2 + window_size[0]/2
            proj_y = 5 / (adder + self.pos.y) + window_size[1]-50 - proj_height - self.pos.y * 5
            pg.draw.rect(canvas, col.lerp(0, lerp), pg.Rect(proj_x, proj_y, proj_width, proj_height))
    
    def step(self):
        self.t += 0.05
        self.pos.z = (math.sin(self.t) + 1.1) * 5


stripes = []
for y in range(6, -1, -1):
    for x in range(-5-y*2, 6+y*2):
        stripes.append(Stripe(x*50, y*2))


pg.init()
pg.display.set_caption("Stripes")
canvas = pg.display.set_mode(window_size)
clock = pg.time.Clock()


run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    for i in stripes:
        i.step()
        i.draw(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
