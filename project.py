import pygame as pg
import os
import sys
from time import sleep

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 320  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
MOVE_SPEED = 2.2
GRAVITY_FLAG = False
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
GRAVITY = 2.5  # Сила, которая будет тянуть нас вниз или вверх
death = False
entities = pg.sprite.Group()  # Все обьекты
finish_sprite = pg.sprite.Group()
buttons = pg.sprite.Group()



class Button(pg.sprite.Sprite):
    def __init__(self, pos, level, unlocked, *group):
        super().__init__(*group)
        self.unlocked = unlocked
        self.size = (100, 100)
        self.image = pg.Surface(self.size)
        self.level = level
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.fill((27, 188, 40)) if self.unlocked else self.image.fill((61, 75, 63))
        self.font = pg.font.SysFont(None, 24)
        self.text = self.font.render(str(level + 1), True, (0, 0, 0))
        self.image.blit(self.text, (45, 45))        
    
    def update(self):
        if self.unlocked:
            if self.image.get_rect().collidepoint(pg.mouse.get_pos()):
                self.image = pg.transform.scale(self.image, (150, 150))
                self.image.fill((27, 188, 63))
                self.image.blit(self.text, (70, 70))
            else:
                self.image = pg.transform.scale(self.image, (100, 100))
                self.image.fill((27, 188, 40))
                self.image.blit(self.text, (45, 45))


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Sprite_Mouse_Location(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x,y,1,1)

class Player(pg.sprite.Sprite):

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.GRAVITY_FLAG = GRAVITY_FLAG
        self.rect = pg.Rect(x, y, WIDTH, HEIGHT)
        self.speed = 0
        self.pos = (x, y)
        self.full_sprite = load_image('SteamMan_run.png')
        self.size = (288, 34)
        self.image = self.full_sprite.subsurface(0, 0, 48, 34)
        self.rect = self.image.get_rect()
        self.frame = 0
        self.frames = 6
        self.elapsed = 0
        self.flip = False
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.rect.width = self.rect.height = 30
        self.win = False

    def update(self, up, platforms):
        time = pg.time.get_ticks()
        if time - self.elapsed > 60:
            self.image = self.full_sprite
            self.image = self.full_sprite.subsurface(self.size[0] // self.frames * self.frame,
                                                     0,
                                                     self.size[0] // self.frames,
                                                     self.size[1])
            if self.GRAVITY_FLAG:
                self.image = pg.transform.flip(self.image, False, True)
            self.frame = (self.frame + 1) % self.frames
            self.elapsed = time        
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
        self.collide(platforms)

    def collide(self, platforms):
        for i in finish_sprite:
            if pg.sprite.collide_rect(self, i):
                self.win = True     
        
        global death
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                if self.yvel == 0:
                    death = True
                if self.yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
    
                if self.yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    self.onGround = True
                
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image('block1.png')
        self.rect = pg.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Flag(pg.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image('flag_finish.png', -1)
        self.image = pg.transform.scale(self.image, (35, 35))
        self.rect = pg.Rect(x, y, 100, 100)


def main():
    global buttons, entities, finish_sprite
    
    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    pg.display.set_caption("Gravity Guy")
    up = False
    platforms = []  # то, во что мы будем врезаться или опираться
    level1 = [
        "-------  -------  ------- ----       ---------                                                     ",
        "                                                                      ----------------             ",
        "                                                                                                   ",
        "                             ---------       -------                                               ",
        "                                                                                                   ",
        "                                                   -----           ---                             ",
        "                                                                                                   ",
        "                                                                                                   ",
        "                                                                                                 @ ",
        "------------- -------------                            -------------                ---------------"]

    level2 = [
        "         -----                       ----      -----------                     -----              ---        ",
        "                                                                                                             ",
        "                 -----  ----                                     ---------- ----                --           ",
        "                                         ------                                    --         --             ",
        "                                                         --                          --     --               ",
        "              ----   ----  ----                                                        --                    ",
        "                                                                                         ---                 ",
        "                                -----                     --------         -                                 ",
        "                                                                                                            @",
        "---------                                                                                            --------"]

    level3 = [
        "                 ---           ---                        ----- ---   ",
        "                                                                      ",
        "              --   --                                                 ",
        "                      --                                       -      ",
        "                        -----             -------                     ",
        "                                                                      ",
        "        ----    ----              ---------    ------                 ",
        "                                                                      ",
        "                                                      --             @",
        "--------   -----              ----                      -          ---"]
    start = False
    unl = [True, False, False]
    level = 0
    
    while True:
        GRAVITY_FLAG = death = up = False
        platforms = []
        entities = pg.sprite.Group()  # Все обьекты
        finish_sprite = pg.sprite.Group()
        buttons = pg.sprite.Group()
        screen.fill('black')
        font = pg.font.SysFont(None, 80)
        text = font.render('Gravity Guy', True, (0, 136, 30))
        screen.blit(text, (250, 50))
        font = pg.font.SysFont(None, 40)
        text = font.render('Выберите уровень:', True, (0, 136, 30))
        screen.blit(text, (270, 110))
        for i in range(150, 601, 200):
            btn = Button((i, 150), ((i - 150) // 200), unl[((i - 150) // 200)], buttons)
        for e in pg.event.get():  # Обрабатываем события
                if e.type == pg.QUIT:
                    sys.exit()
                if e.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    pos = Sprite_Mouse_Location(*pos)
                    clicked = pg.sprite.spritecollideany(pos, buttons)
                    if clicked:
                        if clicked.unlocked:
                            level = clicked.level
                            start = True
                        
        
        
        if start:
            bg_pos_1 = 0
            bg_pos_2 = 800
            speed = 0.4
            bg_w, bg_h = 800, WIN_HEIGHT
            bg = pg.transform.smoothscale(load_image('moving_bg.png'), (bg_w, bg_h))   # Создание фона
            
            screen.fill((0, 0, 0))
            hourglass = load_image('hourglass.png')
            screen.blit(hourglass, (367, 20))
            text = font.render('loading...', True, (255, 255, 255))
            screen.blit(text, (350, 160))
            pg.display.flip()
            
            
            hero = Player(55, 55, entities)  # создаем героя по (x,y) координатам
            '''--------------Начало первого цикла------------------'''
            x = y = 0
            if level == 0:
                load_level = level1
            elif level == 1:
                load_level = level2
            else:
                load_level = level3
            for row in load_level:  # вся строка
                for col in row:  # каждый символ
                    if col == "-":
                        pf = Platform(x, y, entities)
                        platforms.append(pf)
                    elif col == '@':
                        flag = Flag(x, y, entities, finish_sprite)
                        platforms.append(flag)
                    x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                y += PLATFORM_HEIGHT  # то же самое и с высотой
                x = 0
        
            running = True
            while running:  # Основной цикл программы
                pg.time.delay(15)

                for e in pg.event.get():  # Обрабатываем события
                        if e.type == pg.QUIT:
                            sys.exit()
                    
                        if e.type == pg.KEYDOWN and e.key == pg.K_UP:
                            up = True
                    
                        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                            up = True
                    
                        if e.type == pg.KEYUP and e.key == pg.K_UP:
                            up = False
                    
                        if e.type == pg.KEYUP and e.key == pg.K_SPACE:
                            up = False
                if hero.rect.top < 32 or hero.rect.bottom > 288 or death:
                    running = False
                    log = 'Вы проиграли!'
                if hero.win:
                    running = False
                    log = 'Вы выиграли!'
                    level += 1 if level < 2 else 0
        
                if running:
                    for i in platforms:
                        i.rect.left -= MOVE_SPEED                    
                    
                    bg_pos_1 -= speed
                    if bg_pos_1 <= -800:
                        bg_pos_1 = abs(bg_pos_1)
                    bg_pos_2 -= speed
                    if bg_pos_2 <= -800:
                        bg_pos_2 = abs(bg_pos_2)

                    screen.fill((0, 0, 0))
                    screen.blit(bg, (bg_pos_1, 0))
                    screen.blit(pg.transform.flip(bg, True, False), (bg_pos_2, 0))
                    
                    hero.update(up, platforms)  # передвижение
                    entities.draw(screen)
                    pg.display.flip()
                else:
                    screen.fill((0, 0, 0))
                    text = font.render(log, True, (255, 255, 255))
                    screen.blit(text, (330, 140))
                    pg.display.flip()
                    sleep(3)
            '''--------------Конец первого цикла------------------'''
        unl[level] = True
        buttons.draw(screen)
        buttons.update()
        pg.display.flip()
        start = False


if __name__ == "__main__":
    main()
