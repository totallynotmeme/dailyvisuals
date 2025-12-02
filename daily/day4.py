import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Tree")
clock = pg.time.Clock()


font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
WARNING this script is not crash-proof
R - generate new random tree
S - save current tree
D - show saved trees (random order)
F - delete rightmost tree in saved trees
Z - hide this text (on next screen refresh)
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))


class Tree:
    types = 4
    origin = pg.Vector2(window_size[0] / 2, window_size[1])
    up = pg.Vector2(0, -1)
    def __init__(self, genome=None, colors=None, pos=origin):
        if genome is None:
            genome = []
            for _ in range(Tree.types):
                thing = []
                branches = random.randint(0, 3)
                for i in range(branches):
                    to_what = [
                        random.randint(0, Tree.types - 1), # which branch type
                        random.random(), # scale factor
                        (random.random() - 0.5) * 90, # rotation degrees
                    ]
                    thing.extend(to_what)
                genome.append(tuple(thing))
        
        if colors is None:
            colors = [(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ) for _ in range(Tree.types)]
        
        self.genome = genome
        self.colors = colors
        self.branches = [(0, pos, 0, 100)]
    
    def copy(self, pos=origin):
        return Tree(genome=self.genome.copy(), colors=self.colors.copy(), pos=pos)
    
    def step(self, canvas):
        if not self.branches:
            return False
        type, pos, rot, scale = self.branches.pop(0)
        dest = pos + Tree.up.rotate(rot) * scale
        color = self.colors[type]
        pg.draw.aaline(canvas, color, pos, dest)
        pos = dest
        
        code = self.genome[type]
        for ind in range(0, len(code), 3):
            which_type = code[ind]
            which_scale = scale * code[ind+1]
            if which_scale < 5:
                pg.draw.circle(canvas, color, pos, 4)
                continue
            which_ang = rot + code[ind+2]
            packet = (which_type, pos, which_ang, which_scale)
            self.branches.append(packet)
        return True


active = [Tree()]
saved = []
draw_controls(canvas)


run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_r:
                canvas.fill((0, 0, 0))
                draw_controls(canvas)
                active = [Tree()]
            if ev.key == pg.K_s:
                saved.append(active[0])
            if ev.key == pg.K_d:
                canvas.fill((0, 0, 0))
                draw_controls(canvas)
                active = []
                random.shuffle(saved)
                for ind, i in enumerate(saved, start=1):
                    pos_x = (window_size[0] - 200) * ind / (len(saved) + 1) + 100
                    point = pg.Vector2(pos_x, window_size[1])
                    active.append(i.copy(pos=point))
            if ev.key == pg.K_f:
                saved.pop()
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    for i in active:
        limit = 0
        while i.step(canvas) and limit < 100:
            limit += 1
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
