import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Network")
clock = pg.time.Clock()


window_center = pg.Vector2(window_size) / 2
color_ping = pg.Color(120, 200, 255)
#color_idle = pg.Color(230, 255, 230)

random_vec2 = lambda: pg.Vector2(random.random() - 0.5, random.random() - 0.5)

class Node:
    grid = {}
    neighbors = [
        ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)),
        ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))
    ]
    pings = 0
    
    def __init__(self, x, y):
        self.pos = pg.Vector2()
        self.vel = pg.Vector2()
        self.origin = pg.Vector2()
        self.state = "idle"
        self.state_t = 0
        self.light_up = []
        self.con_from = []
        self.con_to = []
        self.x = x
        self.y = y
        Node.grid[(x, y)] = self
    
    def make_cons(self):
        for off_x, off_y in Node.neighbors[self.y%2]:
            n = Node.grid.get((self.x + off_x, self.y + off_y), False)
            if n:
                self.con_to.append(n)
                n.con_from.append(self)
    
    def draw_cons(self, canvas):
        if self.state == "ping":
            for i in self.light_up:
                pg.draw.aaline(canvas, color_ping, self.pos, i.pos, 2)
        if self.state == "fade":
            color = color_ping.lerp("black", (1 - self.state_t / 128) ** 2)
            for i in self.light_up:
                pg.draw.aaline(canvas, color, self.pos, i.pos, 2)
    
    def draw_self(self, canvas):
        r = 2 + (self.state != "idle") * 2
        #pg.draw.circle(canvas, color_idle, self.pos, r)
        if self.state == "ping":
            ping_r = ((30 - self.state_t) / 30) ** 0.5 * 50
            ping_color = color_ping.lerp("black", (1 - self.state_t / 30) ** 2)
            pg.draw.circle(canvas, ping_color, self.pos, ping_r, 3)
    
    def step(self):
        self.pos += self.vel
        self.pos = (self.pos * 19 + self.origin) / 20
        self.vel += random_vec2() / 5
        self.vel /= 1.01
        # can be refactored, but i'm too lazy.
        # not like i'm gonna maintain this project, it's just a silly little demo
        if self.state == "ping":
            if self.state_t == 20:
                for i in self.con_to:
                    if random.random() > 0.2 and i.ping():
                        self.light_up.append(i)
            if self.state_t <= 0:
                self.state_t = 128
                self.state = "fade"
        if self.state == "fade":
            if self.state_t <= 0:
                self.state = "idle"
                Node.pings -= 1
        self.state_t -= 1
    
    def ping(self):
        if self.state != "idle":
            return False
        self.light_up = []
        self.state = "ping"
        self.state_t = 30
        Node.pings += 1
        return True

for y in range(10):
    pos_y = y * window_size[1] // 10
    pos_y += window_size[1] // 20
    for x in range(16 - y%2):
        pos_x = x * window_size[0] // 16
        pos_x += window_size[0] // 32 * (y%2 + 1)
        n = Node(x, y)
        n.pos = window_center
        n.origin = pg.Vector2(pos_x, pos_y)

for i in Node.grid.values():
    i.make_cons()


run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    Node.drawn = []
    for i in Node.grid.values():
        i.step()
    for i in Node.grid.values():
        i.draw_cons(canvas)
    for i in Node.grid.values():
        i.draw_self(canvas)
    
    if Node.pings < 2:
        random.choice(list(Node.grid.values())).ping()
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
