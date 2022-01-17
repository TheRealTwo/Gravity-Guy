from classes import *
from maps import *


size = (1300, 800)
pg.init()
screen = pg.display.set_mode(size)
screen.fill((255, 255, 255))
pg.display.set_caption('Grunvity')
runner = Runner((200, 272), elements)
clock = pg.time.Clock()

for el in MAP_TEST:
    if el[-1] == 'border.png':
        gr = borders
        print('border detected')
    else:
        gr = blocks
    Block(*el, gr)

run = True
while run:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    runner.jump()
    screen.fill((255, 255, 255))
    tick = clock.tick()
    speed = 30 * tick / 100
    boost = 9.8 * tick / 1000
    blocks.draw(screen)
    blocks.update(speed=int(speed))
    elements.draw(screen)
    elements.update(boost=boost)
    borders.draw(screen)
    borders.update(speed=int(speed))
    pg.display.flip()
pg.quit()