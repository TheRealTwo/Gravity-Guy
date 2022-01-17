import pygame
from pygame import *

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 320  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
MOVE_SPEED = 3
GRAVITY_FLAG = False
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
GRAVITY = 2.5  # Сила, которая будет тянуть нас вниз или вверх


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.GRAVITY_FLAG = GRAVITY_FLAG
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                if not self.GRAVITY_FLAG:
                    self.GRAVITY_FLAG = True
                else:
                    self.GRAVITY_FLAG = False

        if not self.onGround:
            if not self.GRAVITY_FLAG:
                self.yvel += GRAVITY
            else:
                self.yvel -= GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(self.yvel, platforms)
        self.collide(0, platforms)

    def collide(self, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    self.onGround = True


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load('block1.png')
        self.image = transform.scale(self.image, (30, 30))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Gravity Guy")  # Пишем в шапку
    bg = image.load('galaxy_background.jpg')  # Создание видимой поверхности
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)
    level = [
        "-------  -------  -------   ---                  ",
        "                               ----              ",
        "                                                 ",
        "                                                 ",
        "                                                 ",
        "                                                 ",
        "                                    ----  ---    ",
        "                                                 ",
        "                                 ----  ---       ",
        "-------------- -------------  ----          -----"]

    x = y = 0
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    running = True
    while running:
        pygame.time.delay(15)  # Основной цикл программы
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                running = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
        if hero.rect.top < 32 or hero.rect.bottom > 288:
            running = False

        for i in platforms:
            i.rect.left -= MOVE_SPEED

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        hero.update(up, platforms)  # передвижение
        entities.draw(screen)
        display.update()


if __name__ == "__main__":
    main()
