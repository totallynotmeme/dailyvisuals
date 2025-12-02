import pygame as pg


window_size = (1600, 900)
# if you wanna do stuff to an image:
#path = input("Path to image file: ").strip("'\" ")

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("Title")
clock = pg.time.Clock()


# if this script is interactive:
font = pg.font.SysFont("consolas", 15)
do_draw_ctrl = True
controls = """
C - do something
B - do something else
A - do another thing
Z - hide this text
""".strip().split("\n")

def draw_controls(canvas):
    if not do_draw_ctrl:
        return
    for ind, i in enumerate(controls):
        y = ind*15 + 5
        txt = font.render(i, True, (255, 255, 255))
        canvas.blit(txt, (5, y))
# end


run = True
while run:
    for ev in pg.event.get():
        # if interactive:
        if ev.type == pg.KEYDOWN:
            # handle other keys
            # ...
            if ev.key == pg.K_z:
                do_draw_ctrl = not do_draw_ctrl
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    # visual stuff go here
    
    # if interactive:
    draw_controls(canvas)
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)

pg.quit()
