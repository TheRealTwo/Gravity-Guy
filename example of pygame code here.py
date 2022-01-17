'----------EXAMPLE OF PYGAME CODE HERE----------'


from classes import *
import pygame as pg




if __name__ == '__main__':
    size = (800, 600)
    pg.init()
    screen = pg.display.set_mode(size)
    screen.fill('blue')
    pg.display.set_caption('Шарики')
    running = True
    screen.fill((0, 0, 0))
    balls = []
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                balls.append([-100, -100, [*event.pos]])
        screen.fill((0, 0, 0))
        tick = clock.tick()
        for info in balls:
            speed_x = info[0] * tick / 1000
            speed_y = info[1] * tick / 1000
            pg.draw.circle(screen, (255, 255, 255), (int(info[-1][0]), int(info[-1][1])), 10)
            if (info[-1][0] + speed_x - 10 <= 0 and speed_x < 0 or
                info[-1][0] + speed_x + 10 >= size[0] and speed_x > 0):
                info[0] = -info[0]
            if (info[-1][1] + speed_y - 10 <= 0 and speed_y < 0 or
                info[-1][1] + speed_y + 10 >= size[1] and speed_y > 0):
                info[1] = -info[1]
            info[-1][0] += speed_x
            info[-1][1] += speed_y
        pg.display.flip()
    pg.quit()