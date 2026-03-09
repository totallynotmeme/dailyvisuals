import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Sand")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
Scroll wheel - switch material
Left click - draw
Right click - erase
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


# the code is a spaghetti-fest and it's a little hard to add new materials,
# but let's be fair: this is supposed to be a small silly visual demo,
# not an actual project. it works, it's good enough, i won't come back to this.


grid_surface = pg.Surface(window_size)
color_materials = [
    pg.Color(5, 5, 10), # blank
    pg.Color(100, 100, 100), # wall
    pg.Color(210, 200, 50), # sand
    pg.Color(50, 100, 200), # water
]

cell_size = 20
grid_size = (window_size[0] // cell_size, window_size[1] // cell_size)
grid = [0] * grid_size[0] * grid_size[1]


def is_in_grid(x, y):
    if x < 0 or x >= grid_size[0]:
        return False
    if y < 0 or y >= grid_size[1]:
        return False
    return True


def get_neighbours(x, y):
    this = []
    that = [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y),   (x, y),   (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1),
    ]
    for i in that:
        if is_in_grid(*i):
            this.append(i)
    return this


def get_cell(x, y):
    if not is_in_grid(x, y):
        return 1 # wall
    return grid[y * grid_size[0] + x]


to_update = []
next_to_update = [(x, y) for y in range(grid_size[1]) for x in range(grid_size[0])]

def update(surface, x, y):
    if not is_in_grid(x, y):
        return
    ind = y * grid_size[0] + x
    material = grid[ind]
    rect = pg.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
    pg.draw.rect(surface, color_materials[material], rect)
    
    if material == 2: # sand
        # vv
        cell = get_cell(x, y+1)
        if cell in (0, 3):
            grid[ind] = cell
            grid[ind + grid_size[0]] = 2
            around = set(get_neighbours(x, y)) | set(get_neighbours(x, y+1))
            next_to_update.extend(around)
            return
        # v> or <v
        dir_x = random.choice([1, -1])
        cell = get_cell(x + dir_x, y+1)
        if cell in (0, 3):
            grid[ind] = cell
            grid[ind + grid_size[0] + dir_x] = 2
            around = set(get_neighbours(x, y)) | set(get_neighbours(x+dir_x, y+1))
            next_to_update.extend(around)
            return
        # or the opposite way
        cell = get_cell(x - dir_x, y+1)
        if cell in (0, 3):
            grid[ind] = cell
            grid[ind + grid_size[0] - dir_x] = 2
            around = set(get_neighbours(x, y)) | set(get_neighbours(x-dir_x, y+1))
            next_to_update.extend(around)
            return
    
    if material == 3: # water
        # no need for cell=get_cell(...) because only one check
        # it's spaghetti but WHO CARES THIS WON'T BE MAINTAINED-
        if get_cell(x, y+1) == 0:
            grid[ind] = 0
            grid[ind + grid_size[0]] = 3
            around = set(get_neighbours(x, y)) | set(get_neighbours(x, y+1))
            next_to_update.extend(around)
            return
        # v> or <v
        dir_x = random.choice([1, -1])
        if get_cell(x + dir_x, y+1) == 0:
            grid[ind] = 0
            grid[ind + grid_size[0] + dir_x] = 3
            around = set(get_neighbours(x, y)) | set(get_neighbours(x+dir_x, y+1))
            next_to_update.extend(around)
            return
        if get_cell(x - dir_x, y+1) == 0:
            grid[ind] = 0
            grid[ind + grid_size[0] - dir_x] = 3
            around = set(get_neighbours(x, y)) | set(get_neighbours(x-dir_x, y+1))
            next_to_update.extend(around)
            return
        # >> or <<
        dir_x = random.choice([1, -1])
        if get_cell(x + dir_x, y) == 0:
            grid[ind] = 0
            grid[ind + dir_x] = 3
            around = set(get_neighbours(x, y)) | set(get_neighbours(x+dir_x, y))
            next_to_update.extend(around)
            return
        if get_cell(x - dir_x, y) == 0:
            grid[ind] = 0
            grid[ind - dir_x] = 3
            around = set(get_neighbours(x, y)) | set(get_neighbours(x-dir_x, y))
            next_to_update.extend(around)
            return


for x in range(5, 15):
    for y in range(5, 10):
        grid[x + y * grid_size[0]] = 2
        grid[x + 10 + y * grid_size[0]] = 3


material_drawing = 0
run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.MOUSEWHEEL:
            material_drawing = (material_drawing + ev.y - 1) % 3 + 1
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.blit(grid_surface, (0, 0))
    
    to_update = next_to_update
    next_to_update = []
    for i in set(to_update):
        update(grid_surface, *i)
    
    hovering_cell = tuple(i // cell_size for i in pg.mouse.get_pos())
    x = hovering_cell[0] * cell_size
    y = hovering_cell[1] * cell_size
    color = color_materials[material_drawing]
    pg.draw.rect(canvas, color, pg.Rect(x, y, cell_size, cell_size), 1)
    
    mouse_keys = pg.mouse.get_pressed()
    if mouse_keys[0]:
        if is_in_grid(*hovering_cell):
            x, y = hovering_cell
            ind = y * grid_size[0] + x
            if grid[ind] == 0:
                grid[ind] = material_drawing
                next_to_update.extend(get_neighbours(x, y))
    if mouse_keys[2]:
        if is_in_grid(*hovering_cell):
            x, y = hovering_cell
            ind = y * grid_size[0] + x
            if grid[ind] > 0:
                grid[ind] = 0
                next_to_update.extend(get_neighbours(x, y))
    
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
