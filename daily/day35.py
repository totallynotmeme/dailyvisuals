import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Eyes")
clock = pg.time.Clock()


cursor_pos = (0, 0)
cursor_in_window = False


class One:
    ind = 0
    
    def __init__(self, x, y):
        self.origin = pg.Vector2(x, y)
        self.pos = pg.Vector2(x, y)
        self.off = pg.Vector2(0, 0)
        self.blink_state = 0
        self.blink_t = 0
        self.eye_pos = pg.Vector2(0, 0)
        self.ind = One.ind % 4
        One.ind += 1
    
    def draw(self, canvas, follow_mouse):
        if follow_mouse:
            goal = cursor_pos - self.pos
            distance = min(goal.length() ** 0.5 / 3, 10)
            if distance > 0.1:
                goal = goal.normalize() * distance
                goal.y *= self.blink_state
        else:
            goal = (0, 0)
        self.eye_pos = self.eye_pos.lerp(goal, 0.3)
        
        points = (
            self.pos + (-20, 0),
            self.pos + (-12, 7*self.blink_state),
            self.pos + (0, 10*self.blink_state),
            self.pos + (12, 7*self.blink_state),
            self.pos + (20, 0),
            self.pos + (12, -7*self.blink_state),
            self.pos + (0, -10*self.blink_state),
            self.pos + (-12, -7*self.blink_state),
        )
        pg.draw.polygon(canvas, "white", points)
        pg.draw.circle(canvas, "black", self.pos + self.eye_pos, 5)
    
    def step(self):
        self.pos = self.pos.lerp(self.origin + self.off, 0.2)
        
        if cursor_in_window:
            chance = 0.03
        else:
            chance = 0.001
        
        if (t // 7 % 4 == self.ind) and random.random() < chance:
            self.off.x = random.random() * 2 - 1
            self.off.y = random.random() * 2 - 1
            self.off *= 10
        
        if cursor_in_window and (cursor_pos - self.pos).length() < 100:
            self.blink_t = 10
        
        self.blink_t -= 1
        if self.blink_t > 0:
            self.blink_state /= 2
        else:
            self.blink_state = (self.blink_state + 0.2) / 1.2

eyes = []
for y in range(40, window_size[1]-24, 75):
    offset = (y % 100) // 2
    for x in range(40 + offset, window_size[0]-24, 75):
        eyes.append(One(x, y))


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.WINDOWLEAVE:
            cursor_in_window = False
        if ev.type == pg.WINDOWENTER:
            cursor_in_window = True
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    cursor_pos = pg.mouse.get_pos()
    
    for i in eyes:
        i.step()
    for i in eyes:
        i.draw(canvas, cursor_in_window)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
