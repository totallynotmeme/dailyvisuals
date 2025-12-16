import pygame as pg


window_size = (1600, 900)


step = 25
lines = []
lines_x = window_size[0] // step
lines_y = window_size[1] // step
half_step = step // 2
og_vector = pg.Vector2(20, 0)
for i in range(lines_x * lines_y):
    lines.append(og_vector.rotate(i/3))


pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Lines")
clock = pg.time.Clock()


color = pg.Color(0)
run = True
t = 0
while run:
    mouserel = pg.Vector2()
    for ev in pg.event.get():
        if ev.type == pg.MOUSEMOTION:
            mouserel += ev.rel
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    
    mapped_x, mapped_y = pg.mouse.get_pos()
    mapped_x = mapped_x // step
    mapped_y = mapped_y // step
    
    for near_y in range(-5, 6):
        y = mapped_y + near_y
        if y < 0 or y >= lines_y:
            continue
        for near_x in range(-5, 6):
            x = mapped_x + near_x
            if x < 0 or x >= lines_x:
                continue
            ind = y * lines_x + x
            dist = abs(near_x) + abs(near_y) + 1
            lines[ind] -= mouserel / dist
    
    
    for ind, i in enumerate(lines):
        y, x = divmod(ind, lines_x)
        hue = (x * 5 + y * 5 - t) % 360
        color.hsva = (hue, 100, 100, 100)
        from_x = x * step + half_step
        from_y = y * step + half_step
        to_x = from_x + i.x
        to_y = from_y + i.y
        width = int(min(i.length(), step))
        pg.draw.line(canvas, color, (from_x, from_y), (to_x, to_y), width)
        i /= 1.05
        i.rotate_ip(-10)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
