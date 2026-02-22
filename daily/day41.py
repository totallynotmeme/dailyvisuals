import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Fairies")
clock = pg.time.Clock()


class Point:
    def __init__(self):
        x = random.randint(0, window_size[0])
        y = random.randint(0, window_size[1])
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(random.random(), random.random()) * 10 - (5, 5)
        self.trail = [tuple(self.pos)] * 60
        self.grabbed = False
    
    def draw(self, target):
        color = pg.Color(0)
        ind = 0
        for p1, p2 in zip(self.trail, self.trail[1:]):
            color.hsva = (ind * 6, 100, 100, 100)
            pg.draw.aaline(target, color, p1, p2)
            ind += 1
    
    def step(self):
        if self.grabbed:
            self.vel.x = random.random() * 20 - 10
            self.vel.y = random.random() * 20 - 10
            self.pos += self.vel
            
            self.trail.pop()
            self.trail.insert(0, tuple(self.pos))
            return
        
        self.pos += self.vel
        self.vel += (random.random() - 0.5, random.random() - 0.5)
        self.vel /= 1.01
        
        if self.pos.x < 0:
            self.pos.x += 5
            self.vel.x *= -1
        if self.pos.x >= window_size[0]:
            self.pos.x -= 5
            self.vel.x *= -1
        
        if self.pos.y < 0:
            self.pos.y += 5
            self.vel.y *= -1
        if self.pos.y >= window_size[1]:
            self.pos.y -= 5
            self.vel.y *= -1
        
        self.trail.pop()
        self.trail.insert(0, tuple(self.pos))

points = [Point() for _ in range(20)]

dark_mask = pg.Surface(window_size)
dark_mask.fill((64, 64, 64))
dark_overlay = pg.Surface(window_size)
dark_overlay.fill((2, 2, 2))
buffer_1 = pg.Surface(window_size)
buffer_2 = pg.Surface(window_size)


mouse_pos = (0, 0)
mouse_rel = pg.Vector2(0, 0)
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    # magic (aka nonsense)
    buffer_1 = canvas.copy()
    buffer_1.blit(dark_mask, (0, 0), None, pg.BLEND_MULT)
    # blur left+right
    buffer_2.fill((0, 0, 0))
    buffer_2.blit(buffer_1, (-1, 0), None, pg.BLEND_ADD)
    buffer_2.blit(buffer_1, (1, 0), None, pg.BLEND_ADD)
    # blur up+down
    buffer_1.fill((0, 0 ,0))
    buffer_1.blit(buffer_2, (0, -1), None, pg.BLEND_ADD)
    buffer_1.blit(buffer_2, (0, 1), None, pg.BLEND_ADD)
    
    # making it a little darker so it's not filling the screen with white
    buffer_1.blit(dark_overlay, (0, 0), None, pg.BLEND_SUB)
    
    canvas.blit(buffer_1, (0, 0))
    
    grabbing = pg.mouse.get_pressed()[0] # left button
    if grabbing:
        current_pos = pg.Vector2(pg.mouse.get_pos())
        mouse_rel = current_pos - mouse_pos
        mouse_pos = current_pos
    
    for i in points:
        if grabbing:
            if i.pos.distance_squared_to(mouse_pos) < 1600:
                i.grabbed = True
        elif i.grabbed:
            i.grabbed = False
            i.vel.x, i.vel.y = mouse_rel
        
        if i.grabbed:
            i.pos.x, i.pos.y = mouse_pos
        
        i.step()
        i.draw(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
