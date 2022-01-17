import pygame as pg
import os
import sys

elements = pg.sprite.Group()
blocks = pg.sprite.Group()
borders = pg.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image



class Block(pg.sprite.Sprite):
    def __init__(self, size, pos, image, *group):
        # оптимальный размер - 128 на 128 пикселей
        super().__init__(*group)
        self.size = size
        self.pos = pos
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

    def get_pos(self):
        return self.pos
    
    def update(self, **kwargs):
        self.rect = self.rect.move(-kwargs['speed'], 0)
        if self.rect.x + self.rect.width < 0:
            self.kill()

    


class Runner(pg.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.size = (128, 128)
        self.pos = pos
        # runner_cut.png - версия runner.png без лишнего верха, чтобы визуально пространства между головой и блоком не было
        # потом сделаю нормальный спрайт и переворачивание в прыжке
        self.full_sprite = load_image('runner_cut.png')
        self.rect = self.full_sprite.get_rect()
        self.frame = 0
        self.grav = 1
        self.flip = False
        self.speed = 0
        self.frames = 2
        self.image = pg.transform.chop(self.full_sprite, pg.Rect(self.size[0] // self.frames * self.frame, 0,
                                                                 self.size[0] // self.frames, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.elapsed = 0
        
    def get_pos(self):
        return self.pos
    
    def is_gravity_down(self):
        return self.gravity_down
    
    def jump(self):
        self.flip = True if not self.flip else False
    
    def update(self, **kwargs):
        # animation stuff
        time = pg.time.get_ticks()
        if time - self.elapsed > 500:
            self.image = self.full_sprite
            self.image = pg.transform.chop(self.full_sprite, pg.Rect(self.size[0] // self.frames * self.frame, 0,
                                                                     self.size[0] // self.frames, 0))
            self.frame = (self.frame + 1) % self.frames
            self.elapsed = time
            
        #check for death
        is_dead = pg.sprite.spritecollideany(self, borders)
        if is_dead:
            print('KILLED!!')
            self.kill()
        
        # gravity things
        ground = pg.sprite.spritecollideany(self, blocks)
        if (not ground is None and 
            (self.flip and self.rect.y + self.rect.height > ground.rect.y + ground.rect.height or 
             not self.flip and self.rect.y < ground.rect.y)):
            self.speed = 0
        else:
            self.grav = 1 - bool(self.flip) * 2
            self.rect.y += int(self.speed)
            self.speed += kwargs.get('boost', 0) * self.grav
            
