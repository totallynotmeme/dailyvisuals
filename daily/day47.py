import pygame as pg
from math import sin


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Lines")
clock = pg.time.Clock()


line_length = (window_size[0] ** 2 + window_size[1] ** 2) ** 0.5
goal_distance = min(window_size) / 2
window_center = pg.Vector2(window_size) / 2

overlay = pg.Surface(window_size)
overlay.fill((2, 2, 2))

point_count = 3
points = [pg.Vector2(window_center) for i in range(point_count)]
point_angles = [i * 180 / point_count for i in range(point_count)]
point_goal = pg.Vector2()

right = pg.Vector2(1, 0)
color = pg.Color(0)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(overlay, (0, 0), None, pg.BLEND_SUB)
    
    true_distance = goal_distance * sin(t / 200)
    point_goal = window_center + right.rotate(-t) * true_distance
    
    for i, point in enumerate(points):
        point_angles[i] += sin(i + t / 200) / 3
        point_angles[i] %= 360
        
        direction = right.rotate(point_angles[i])
        if point_goal != point:
            speed = (point_goal - point).normalize()
            speed = (1 - abs(direction * speed)) ** 2
            points[i] = point.lerp(point_goal, speed / 10)
            point = points[i]
        
        color.hsva = ((t + i * 74) % 360, 100, 100, 100)
        p_from = point + direction * line_length
        p_to = point - direction * line_length
        
        pg.draw.aaline(canvas, color, p_from, p_to)
        # pg.draw.circle(canvas, "red", point, 5)
    # pg.draw.circle(canvas, "green", point_goal, 7, 1)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
