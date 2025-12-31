import pygame as pg
import random


window_size = (1600, 900)

pg.init()
canvas = pg.display.set_mode(window_size)
pg.display.set_caption("2026 AM")
clock = pg.time.Clock()

font = pg.font.SysFont("consolas", 25)
font_big = pg.font.SysFont("consolas", 45)


# this takes up almost 2kb lol
eepy_nekos_raw = """
.........................   =======..................
.........................   @@@@@=@..................
.........................   ..=.=@...................
.........................   ..@=@....................
.........................   ..=@=.....=====..........
.........................   .=@.@.....@@@=@..........
..======.................   =======.....=@...........
..@@@@=@....====.........   @@@@@@@...=====..........
....==@.....@@=@.........   ..........@@@@@..........
....=@.......=@..==......   ..................=......
..======....=====@=......   .................=@=.....
..@@@@@@.=..@@@==@=......   ..........=.....=@@=.....
........===....=@@@=.....   .........=@=...=@@@=.....
.....====@======@@@==....   ........=@@=====@@@==....
...==@@=@@@=@@=@@@@=@=...   .....===@@@@=@=@@@@=@=...
..=@@@@=@@@@==@@@@@@=@=..   ...==@@=@@@@@==@@@@@=@=..
.=@@@@=@@@@@@@@@@@@@@==..   ..=@@@=@@@@@@@@@@@@@@==..
.=@@@@=@@@@@@@@@@@@@@==..   ..=@@@=@@@@@@@@@@@@@@==..
.=@@@@=@@@@@@@@@@@@@@===.   .=@@@@=@@@@@@@@@@@@@@===.
=@@@@@=@@@@@@@@@@@@=@=@=.   =@@@@@=@@@@@@@@@@@@@==@=.
=@@@@@@=@===@@@@@@=@@=@=.   =@@@@@@=@==@@@@@@@==@=@=.
=@@@@@@=@@@@==@@@=@@@=@==   =@@@@@@=@@@===@@@=@@@=@==
=@@@@@@@=@@@@@=@@@@@=@=@=   =@@@@@@@=@@@@@=@@@@@=@=@=
=@@@@@@@@=@@@@@@=@==@==@=   =@@@@@@@@=@@@@@@=@==@==@=
.=@@@@@@@@========@@==@@=   .=@@@@@@@@========@@==@@=
..======@@@@@@====@@=@@==   ..======@@@@@@====@@=@@==
.......========..=======.   .......========..=======.
"""[1:-1]

eepy_neko = [bytearray(), bytearray()]
colormap = {
    ".": bytes((0, 0, 0, 0)),
    "=": bytes((0, 0, 0, 255)),
    "@": bytes((255, 255, 255, 255)),
}
for neko1, neko2 in map(str.split, eepy_nekos_raw.splitlines()):
    eepy_neko[0].extend(b"".join(colormap[i] for i in neko1))
    eepy_neko[1].extend(b"".join(colormap[i] for i in neko2))

eepy_neko[0] = pg.image.frombytes(bytes(eepy_neko[0]), (25, 27), "RGBA")
eepy_neko[0] = pg.transform.scale_by(eepy_neko[0], 4)
eepy_neko[1] = pg.image.frombytes(bytes(eepy_neko[1]), (25, 27), "RGBA")
eepy_neko[1] = pg.transform.scale_by(eepy_neko[1], 4)

eepy_neko_pos = eepy_neko[0].get_rect(bottomright=window_size).topleft # spaghetti

text = """
2025 will definitely be studied in History classes in the future:
Age verification, social media bans, messenger MAX (in russia)...
I don't have much more to say.

let's hope 2026 won't be the year when Black Mirror becomes reality


i'll take a break from daily visuals for a few days or weeks
you can left click to replay the animation
"""[1:-1].split("\n")


window_center = pg.Vector2(window_size) / 2
size_7seg = min(window_size) // 5
up = pg.Vector2(0, -6)

s = size_7seg
a = size_7seg // 10
x1 = a
x2 = s - a
y1 = a
y2 = s
y3 = 2*s - a
# this is a mess
points_7seg = [
    ((x1+5, y1), (x1+a+5, y1-a), (x2-a-5, y1-a), (x2-5, y1), (x2-a-5, y1+a), (x1+a+5, y1+a)), # top
    ((x1, y1+5), (x1+a, y1+a+5), (x1+a, y2-a-5), (x1, y2-5), (x1-a, y2-a-5), (x1-a, y1+a+5)), # top left
    ((x2, y1+5), (x2+a, y1+a+5), (x2+a, y2-a-5), (x2, y2-5), (x2-a, y2-a-5), (x2-a, y1+a+5)), # top right
    ((x1+5, y2), (x1+a+5, y2-a), (x2-a-5, y2-a), (x2-5, y2), (x2-a-5, y2+a), (x1+a+5, y2+a)), # mid
    ((x1, y2+5), (x1+a, y2+a+5), (x1+a, y3-a-5), (x1, y3-5), (x1-a, y3-a-5), (x1-a, y2+a+5)), # bot left
    ((x2, y2+5), (x2+a, y2+a+5), (x2+a, y3-a-5), (x2, y3-5), (x2-a, y3-a-5), (x2-a, y2+a+5)), # bot right
    ((x1+5, y3), (x1+a+5, y3-a), (x2-a-5, y3-a), (x2-5, y3), (x2-a-5, y3+a), (x1+a+5, y3+a)), # bot
]

two = (True, False, True, True, True, False, True)
zero = (True, True, True, False, True, True, True)
five = (True, True, False, True, False, True, True)
six = (True, True, False, True, True, True, True)

def draw_7seg(*args):
    surf = pg.Surface((size_7seg + 1, size_7seg*2 + 1), pg.SRCALPHA)
    for do, points in zip(args, points_7seg):
        if do:
            pg.draw.polygon(surf, (255, 255, 255), points)
    return surf


two_7seg = draw_7seg(*two)
zero_7seg = draw_7seg(*zero)
five_7seg = draw_7seg(*five)

scene = "first"
run = True
t = 0
while run:
    for ev in pg.event.get():
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == pg.BUTTON_LEFT:
            if scene == "first" or scene == "last":
                scene = "transition"
                snapshot = canvas.copy()
                t = 0
        if ev.type == pg.QUIT:
            run = False
            break
    
    canvas.fill((0, 0, 0))
    
    if scene == "first":
        txt = font.render("Left click to play the animation", True, (255, 255, 255))
        canvas.blit(txt, txt.get_rect(center=window_center))
        txt = font.render("there are no sounds, so use your IMAGINATION", True, (255, 255, 255))
        canvas.blit(txt, txt.get_rect(center=window_center + (0, 30)))
    elif scene == "transition":
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center - (3*size_7seg//2 + 30, 0)))
        canvas.blit(zero_7seg, zero_7seg.get_rect(center=window_center - (size_7seg//2 + 10, 0)))
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center + (size_7seg//2 + 10, 0)))
        canvas.blit(five_7seg, five_7seg.get_rect(center=window_center + (3*size_7seg//2 + 30, 0)))
        snapshot.set_alpha(255 - t*4)
        canvas.blit(snapshot, (0, 0))
        if t >= 100:
            scene = "5_fadeout"
            segment = list(five)
            t = 0
    elif scene == "5_fadeout":
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center - (3*size_7seg//2 + 30, 0)))
        canvas.blit(zero_7seg, zero_7seg.get_rect(center=window_center - (size_7seg//2 + 10, 0)))
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center + (size_7seg//2 + 10, 0)))
        surf = draw_7seg(*segment)
        canvas.blit(surf, surf.get_rect(center=window_center + (3*size_7seg//2 + 30, 0)))
        if t % 15 == 0:
            if True in segment:
                ind = segment.index(True)
                segment[ind] = False
            else:
                scene = "6_appear"
                confetti = []
                goal = list(six)
                t = 0
    elif scene == "6_appear":
        for i in confetti:
            i[0] += i[1]
            i[3] += (t % 7 == 0) * 29
            points = []
            for j in range(3):
                angle = i[3] + j * 120
                points.append(i[0] + up.rotate(angle))
            pg.draw.polygon(canvas, i[2], points)
        
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center - (3*size_7seg//2 + 30, 0)))
        canvas.blit(zero_7seg, zero_7seg.get_rect(center=window_center - (size_7seg//2 + 10, 0)))
        canvas.blit(two_7seg, two_7seg.get_rect(center=window_center + (size_7seg//2 + 10, 0)))
        surf = draw_7seg(*segment)
        canvas.blit(surf, surf.get_rect(center=window_center + (3*size_7seg//2 + 30, 0)))
        
        if t % 6 == 0:
            hue = random.randint(0, 359)
            color = pg.Color(0)
            color.hsva = (hue, 50, 100, 100)
            confetti.append([
                pg.Vector2(random.randint(150, window_size[0] - 150), 0), # pos
                pg.Vector2(random.uniform(-2, 2), 2), # vel
                color, # color
                random.random() * 360, # angle
            ])
        
        if t % 15 == 0:
            if True in goal:
                ind = goal.index(True)
                segment[ind] = True
                goal[ind] = False
            elif t > 360:
                scene = "night2026"
                t = 0
    elif scene == "night2026":
        for i in range(20 - t*2):
            size = random.randint(2, 7) ** 2
            pos = random.randint(0, window_size[1] - size)
            pg.draw.line(canvas, (255, 255, 255), (0, pos), (window_size[0], pos), size)
        txt = font_big.render("12:00 AM", True, (255, 255, 255))
        canvas.blit(txt, txt.get_rect(center = window_center - (0, 40)))
        txt = font_big.render("2026th Year", True, (255, 255, 255))
        canvas.blit(txt, txt.get_rect(center = window_center + (0, 40)))
        if t > 180:
            scene = "last"
            t = 0
    elif scene == "last":
        for i in range(10 - t):
            size = random.randint(2, 7)
            pos = random.randint(100, window_size[1] - size - 100)
            pg.draw.line(canvas, (63, 127, 255), (0, pos), (window_size[0], pos), size)
        txt = font_big.render("happy new year chat", True, (255, 255, 255))
        canvas.blit(txt, txt.get_rect(center = window_center - (0, 150)))
        for ind, i in enumerate(text):
            if i == "":
                continue
            txt = font.render(i, True, (255, 255, 255))
            canvas.blit(txt, txt.get_rect(center = window_center + (0, ind*30 - 50)))
        canvas.blit(eepy_neko[t // 25 % 2], eepy_neko_pos)
    
    
    pg.display.flip()
    print(f"{clock.get_fps():.2f} fps", end="\r")
    clock.tick(60)
    t += 1

pg.quit()
