import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Metaballs")
clock = pg.time.Clock()


class Ball:
    def __init__(self, pos):
        speed_x = random.uniform(-20, 20)
        speed_y = random.uniform(-20, 20)
        
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(speed_x, speed_y)
        self.r = random.randint(20, 70)
    
    def step(self):
        self.vel /= 1.01
        self.vel.x += (random.random() - 0.5) / 3
        self.vel.y += (random.random() - 0.5) / 3
        
        self.pos += self.vel
        
        # bounds check
        #      left/top walls      or          right/bottom walls
        if self.pos.x - self.r < 0 or self.pos.x + self.r > window_size[0]:
            self.pos.x -= self.vel.x
            self.vel.x *= -1
        if self.pos.y - self.r < 0 or self.pos.y + self.r > window_size[1]:
            self.pos.y -= self.vel.y
            self.vel.y *= -1
    
    def draw(self, target, color, add_r=0):
        pg.draw.circle(target, color, self.pos, self.r + add_r)


background = pg.Surface(window_size)
background.fill((3, 2, 1))
window_center = pg.Vector2(window_size) / 2

balls = [Ball(window_center) for _ in range(50)]

color_outer_ball = pg.Color("white")
color_inner_ball = pg.Color("black")

mouse_pos = pg.Vector2(0, 0)
mouse_rel = pg.Vector2(0, 0)


run = True
while run:
    mouse_rel.update(0, 0)
    for ev in pg.event.get():
        if ev.type == pg.MOUSEMOTION:
            mouse_rel += ev.rel
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(background, (0, 0), None, pg.BLEND_SUB)
    mouse_pos.update(pg.mouse.get_pos())
    
    # step
    for i in balls:
        if mouse_pos.distance_to(i.pos) < i.r:
            i.vel = i.vel.lerp(mouse_rel, 0.1)
        i.step()
    
    # draw outer circles
    for i in balls:
        i.draw(canvas, color_outer_ball, 5)
    # draw inner circles
    for i in balls:
        i.draw(canvas, color_inner_ball)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
