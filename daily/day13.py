import pygame as pg


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Vapor")
clock = pg.time.Clock()


sky_top_color = pg.Color(0, 0, 0)
sky_bot_color = pg.Color(20, 0, 40)
ground_color = pg.Color(4)
line_color = pg.Color(0, 255, 255)
sun_top_color = pg.Color(255, 255, 0)
sun_bot_color = pg.Color(255, 127, 0)
sun_ray_colors = [
    pg.Color(255, 50, 50),  # red
    pg.Color(255, 255, 20), # yellow
    pg.Color(20, 255, 255), # blue
]
up = pg.Vector2(0, -sum(window_size))

screen_center = (window_size[0] // 2, window_size[1] // 2)
sun_radius = min(screen_center) - 150


sky_gradient = pg.Surface(window_size)
for y in range(window_size[1] - 300):
    col = sky_top_color.lerp(sky_bot_color, y / (window_size[1] - 300))
    pg.draw.line(sky_gradient, col, (0, y), (window_size[0], y))

sun = pg.Surface(window_size)
pg.draw.circle(sun, (255, 255, 255), screen_center, sun_radius)
temp = pg.Surface(window_size)
for y in range(window_size[1]):
    col = sun_top_color.lerp(sun_bot_color, y/window_size[1])
    pg.draw.line(temp, col, (0, y), (window_size[0], y))
sun.blit(temp, (0, 0), None, pg.BLEND_MULT)

temp.set_colorkey((0, 0, 0))

mask = pg.Surface(window_size)
for y in range(20, window_size[1], 40):
    pg.draw.rect(mask, (255, 255, 255), pg.Rect(0, y, window_size[0], 20))


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(sky_gradient, (0, 0))
    
    if t % 47 == 0:
        sun_ray_colors.append(sun_ray_colors.pop(0))
    
    for a in range(-6, 7): # don't say it
        direction = up.rotate(a * 10)
        pos_from = direction.normalize() * sun_radius + screen_center
        pos_from += (a*50, window_size[1] // 2)
        pos_to = direction + screen_center
        col = sun_ray_colors[a % len(sun_ray_colors)]
        pg.draw.line(canvas, col, pos_from, pos_to, 2)
    
    pg.draw.circle(canvas, (0, 0, 0), screen_center, sun_radius)
    temp.blit(sun, (0, 0))
    temp.blit(mask, (0, (t / 10) * 3 % 40), None, pg.BLEND_MULT)
    canvas.blit(temp, (0, 0))
    
    pg.draw.rect(canvas, ground_color, pg.Rect(0, window_size[1]-300, window_size[0], 300))
    
    for x in range(-4, 15):
        x *= window_size[0] / 10
        x -= screen_center[0]
        pos_far = (x / 2 + screen_center[0], window_size[1] - 300)
        pos_near = (x + screen_center[0], window_size[1])
        pg.draw.line(canvas, line_color, pos_far, pos_near)
    
    for y in range(10):
        pos = ((t / 10 * 4 + y * 30) % 300) / 300
        pos = pos ** 2 * 300
        pos += window_size[1]-300
        pg.draw.line(canvas, line_color, (0, pos), (window_size[0], pos))
    pg.draw.line(canvas, line_color, (0, window_size[1]-300), (window_size[0], window_size[1]-300), 2)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
