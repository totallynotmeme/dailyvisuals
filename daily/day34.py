import pygame as pg
import random
import math


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("ASCII* cube")
clock = pg.time.Clock()


window_center = pg.Vector2(window_size) / 2
scale_factor = min(window_center)

# you can change this to any other character, or even multiple (wasn't intended lol)
char = "@"
font_size = 20

# drawing the mask
mask = pg.Surface(window_size)
font = pg.font.SysFont("consolas", font_size)
txt = font.render(char, True, (255, 255, 255))
mask.blit(txt, (0, 0))

char_size = font.size(char)
text_resolution = (math.ceil(window_size[0] / char_size[0]),
                   math.ceil(window_size[1] / char_size[1]))

# have to do this so it aligns properly
actual_resolution = (text_resolution[0] * char_size[0],
                     text_resolution[1] * char_size[1])


# filling the row
iterations = math.log2(text_resolution[0])
for i in range(math.ceil(iterations)):
    mask.blit(mask, (char_size[0] * 2**i, 0))

# filling the column
iterations = math.log2(text_resolution[1])
for i in range(math.ceil(iterations)):
    mask.blit(mask, (0, char_size[1] * 2**i))


# background gradient
bg_size = (4, 3)
bg_color = pg.Color(0) # will get overwritten, we just need the .Color() object

bg_current = pg.Surface(window_size)
bg_prev = pg.Surface(window_size)
bg_buffer = pg.Surface(bg_size)


# the actual cube stuff
cube_colors = (
    pg.Color(200, 0,   0),
    pg.Color(200, 200, 0),
    pg.Color(0,   200, 0),
    pg.Color(0,   200, 200),
    pg.Color(0,   0,   200),
    pg.Color(200, 0,   200),
)

cube_points = (
    ( 1,  1,  1),
    ( 1,  1, -1),
    ( 1, -1,  1),
    ( 1, -1, -1),
    (-1,  1,  1),
    (-1,  1, -1),
    (-1, -1,  1),
    (-1, -1, -1),
)

"""
from the camera's pov:

.     6        2
.   7        3  
.               
.               
.               
.     4        0
.   5        1  
"""
cube_sides = (
    (0, 1, 3, 2),
    (4, 5, 7, 6),
    (0, 4, 6, 2),
    (1, 5, 7, 3),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
)
cube_normals = ( # for lighting
    (1, 0, 0),
    (-1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
)


run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    # background (just abusing smoothscale to get a cool gradient)
    if t % 240 == 0:
        bg_current.set_alpha(255)
        bg_prev.blit(bg_current, (0, 0))
        bg_color.hsva = (t / 3.14 % 360, 100, 50, 100)
        
        for i in range(bg_size[0] * bg_size[1]):
            y, x = divmod(i, bg_size[0])
            bg_buffer.set_at((x, y), bg_color.lerp("black", random.random()))
        bg_current.blit(pg.transform.smoothscale(bg_buffer, window_size), (0, 0))
    
    bg_current.set_alpha(t % 240 / 240 * 255)
    canvas.blit(bg_prev, (0, 0))
    canvas.blit(bg_current, (0, 0))
    #canvas.blit(pg.transform.scale_by(bg_buffer, 10), (0, 0))
    
    
    # the 3d SQUAR
    projected = []
    points_z = []
    for x, y, z in cube_points:
        # rotate along Y axis
        ox, oz = x, z
        x = ox * math.cos(t / 100) + oz * math.sin(t / 100)
        z = ox * -math.sin(t / 100) + oz * math.cos(t / 100)
        
        # rotate along X axis
        oy, oz = y, z
        y = oy * math.cos(t / 155) + oz * math.sin(t / 155)
        z = oy * -math.sin(t / 155) + oz * math.cos(t / 155)
        
        z += 3 # set cube position to (0, 0, 3)
        
        x /= z
        y /= z
        
        x = x * scale_factor + window_center.x
        y = y * scale_factor + window_center.y
        projected.append((x, y))
        points_z.append(z)
    
    normal_dots = []
    for nx, ny, nz in cube_normals:
        # copying rotations from the previous loop
        nz = nx * -math.sin(t / 100) + nz * math.cos(t / 100)
        nz = ny * -math.sin(t / 150) + nz * math.cos(t / 150)
        normal_dots.append(nz / 2 + 0.5) # map from [-1, 1] to [0, 1]
    
    # (color, points, z_distance)
    to_draw = []
    
    for color, data, normal in zip(cube_colors, cube_sides, normal_dots):
        points = [projected[i] for i in data]
        color = color.lerp("black", normal)
        z_distance = sum(points_z[i] for i in data)
        to_draw.append((color, points, z_distance))
    
    to_draw.sort(key=lambda x: x[2], reverse=True)
    for color, points, _ in to_draw:
        pg.draw.polygon(canvas, color, points)
    
    
    # post-processing
    # we're not actually rendering stuff in text, just resizing and applying a mask
    actual = pg.transform.scale(canvas, text_resolution)
    actual = pg.transform.scale(actual, actual_resolution)
    canvas.blit(actual, (0, 0))
    canvas.blit(mask, (0, 0), None, pg.BLEND_MULT)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
