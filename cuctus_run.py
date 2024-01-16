import pygame
import sys
import os
from pygame import freetype
# Глобвльная переменная, определяющая скорость игры, с течением времени уменьшается, при перезапуске игры принимает
# первоначальное значение

V = -3

# Когда True работают основные действия в цикле игры

GAME_RUNNING = True


# Бэкграунд представляет из себя два класса картинок, которые двигаются друг за другом и перемещаются в конец по
# достижению края экрана

class Background1(pygame.sprite.Sprite):  # первый класс картинки
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0

    # Возвращение бэкграунда на первоначальное положение

    def update(self, *args):
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -1200:
            self.rect.x = 1200


class Background2(pygame.sprite.Sprite):  # второй класс картинки
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 1200

    # Возвращение бэкграунда на первоначальное положение

    def update(self, *args):
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -1200:
            self.rect[0] = 1200


# Класс главного персонажа, анимированный спрайт прыгающего кактуса, может подпрыгивать на пробел или клик мыши, падать
# с ускорением, при столкновении с врагом меняет глобальную переменную GAME_RUNNING на False

class Running_cactus(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.v = -14
        self.g = 0.6
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    # Нарезка спрайта на кадры

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def get_y(self):
        return self.rect[1]

    # Механика прыжка объекта

    def jump(self):
        self.v += self.g
        self.rect = self.rect.move(0, self.v)
        if self.rect[1] > 430:
            self.rect[1] = 430
            self.v = -14

    # Обновление спрайта

    def update(self):
        global GAME_RUNNING
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.g += 0.0002
        if pygame.sprite.collide_mask(self, enemy):
            GAME_RUNNING = False
            music.stop_music()
            music.play(1)


# Тот же класс в виде анимированного спрайта, двигается от края до края экрана с заданным ускорением глобальной
# переменной V, при достижении края перемещается обратно

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(1200, 450)
        self.mask = pygame.mask.from_surface(self.image)

    # Нарезка спрайта на кадры

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # Обновление спрайта

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -100:
            self.rect[0] = 1300

    # Возвращение объекта на изначальное положение

    def reload(self):
        self.rect[0] = 1300


# Класс, отвечающий за музыку игры

class Music():

    # Смена музыки

    def play(self, number):
        if number == 0:
            sound2.play(-1)
            self.now_playing = 0

        if number == 1:
            self.now_playing = 1
            sound1.play(-1)

        if number == 2:
            sound3.play(-1)
            self.now_playing = 2

        if number == 3:
            sound4.play(-1)
            self.now_playing = 3

    # Остановка музыки, которая играет в данный момент

    def stop_music(self):
        if self.now_playing == 0:
            sound2.stop()

        if self.now_playing == 1:
            sound1.stop()

        if self.now_playing == 2:
            sound3.stop()

        if self.now_playing == 3:
            sound4.stop()

    # Проверка, совпадает ли номер переданной музыки с играющей в данный момент

    def different_music(self, music):
        if self.now_playing == music:
            return False
        else:
            return True


# Функция загрузки изображений из папки data

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


fon = pygame.image.load("data/fon.jpg")

# Основной цикл игры

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Сactus Run')
    size = width, height = 1200, 600
    screen = pygame.display.set_mode(size)
    font = pygame.freetype.Font(None, 40)

    all_sprites = pygame.sprite.Group()
    pygame.display.set_icon(pygame.image.load("icon.png"))

    # музыка

    sound1 = pygame.mixer.Sound('data/fail.mp3')
    sound2 = pygame.mixer.Sound('data/music_fon.mp3')
    sound3 = pygame.mixer.Sound('data/music_fon2.mp3')
    sound4 = pygame.mixer.Sound('data/music_fon3.mp3')

    # загружает рекорд предыдущих запусков из файла в папке

    record = open('record.txt', 'r')
    best_score = int(record.readline())
    record.close()

    # загрузка спрайтов

    background1 = Background1(load_image('background1.png'))
    background2 = Background2(load_image('background2.png'))
    cactus = Running_cactus(load_image("cactus_running.png"), 8, 1, 250, 430)
    enemy = Enemy(load_image('enemy.png'), 8, 2)

    running = True

    # start_window = Start()

    music = Music()
    music.play(0)
    jumping = False
    score = 0
    clock = pygame.time.Clock()
    start_window = True
    while running:

        # остановка движения по вертикали в момент касания земли

        if cactus.get_y() == 430:
            jumping = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Основные действия типа прыжка или перезапуска игры по нажатию пробела или кнопки мыши

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if GAME_RUNNING is True:
                    jumping = True

                elif 550 <= event.pos[0] <= 740 and 300 <= event.pos[1] <= 490:
                    GAME_RUNNING = True
                    V = -3
                    enemy.reload()
                    score = 0
                    music.stop_music()
                    music.play(0)

            # старт. окно

            if start_window:
                collor = (168, 107, 20)
                screen.fill((255, 0, 55))

                screen.blit(fon, (0, 0))
                font.render_to(screen, (220, 80), "Пишем код за еду company", collor)
                font.render_to(screen, (240, 140), "Представляет Cuctus Run", collor)
                font.render_to(screen, (220, 200), "Разработчики: Лукин, Носов", collor)
                font.render_to(screen, (300, 260), f'Текущий Рекорд: {str(best_score)}', collor)
                font.render_to(screen, (170, 320), "Для начала игры нажмите SPACE", collor)

                pygame.display.flip()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:

                        start_window = False

        if start_window == False:

            # Отрисовка всех спрайтов

            all_sprites.draw(screen)

            # Уровни сложности

            if int(score) <= 15:
                pygame.draw.rect(screen, (179, 149, 68), ((-5, 50), (400, 60)), 0, 10)
                font.render_to(screen, (5, 60), "Сложность: Халява", (0, 0, 0))

            if 15 < int(score) <= 75:
                pygame.draw.rect(screen, (179, 149, 68), ((-5, 50), (400, 60)), 0, 10)
                font.render_to(screen, (5, 60), "Сложность: Норм", (0, 0, 0))

            if int(score) > 75:
                pygame.draw.rect(screen, (179, 149, 68), ((-5, 50), (400, 60)), 0, 10)
                font.render_to(screen, (5, 60), "Сложность: Хард", (0, 0, 0))

            # Музыка, соответствующая сложности

            if GAME_RUNNING is True:
                if int(score) < 15 and music.different_music(0):
                    music.play(0)
                elif 15 < int(score) <= 75 and music.different_music(2):
                    music.stop_music()
                    music.play(2)
                elif int(score) > 75 and music.different_music(3):
                    music.stop_music()
                    music.play(3)

            # Отрисовка счёта и рекорда в белом окне поверх спрайтов

            pygame.draw.rect(screen, (179, 149, 68), ((940, 40), (270, 90)), 0, 10)
            font.render_to(screen, (1000, 50), f'Счёт: {str(round(score))}', (0, 0, 0))

            # Отрисовка рекорда, если равен нынешнему счёту - дублируется счёт

            if round(score) < best_score:
                font.render_to(screen, (950, 90), f'Рекорд: {str(best_score)}', (0, 0, 0))

            else:
                font.render_to(screen, (950, 90), f'Рекорд: {str(round(score))}', (0, 0, 0))

            # Действия, выполняемые в цикле в ходе игры (ускорение, падение и тд)

            if GAME_RUNNING is True:
                enemy.update()
                background1.update()
                background2.update()
                pygame.mouse.set_visible(False)

                score += -V / 100
                V -= 0.005

                if jumping is True:
                    cactus.jump()

                else:
                    cactus.update()

            else:

                # Действия, выполняемые в случае проигрыша (столкновения персонажа с врагом): отрисовывается
                # итоговый счёт, кнопка перезапуска, в случае если рекорд побит - дополнительное сообщение

                pygame.mouse.set_visible(True)

                pygame.draw.rect(screen, (179, 149, 68), ((450, 190), (320, 55)), 0, 20)
                font.render_to(screen, (460, 200), f'Игра окончена!', (0, 0, 0))

                if round(score) >= best_score:
                    record = open('record.txt', 'w')
                    record.write(str(round(score)))
                    record.close()

                    pygame.draw.rect(screen, (179, 149, 68), ((450, 143), (320, 90)), 0, 20)
                    font.render_to(screen, (460, 200), f'Игра окончена!', (0, 0, 0))
                    font.render_to(screen, (460, 150), f'Новый рекорд!', (0, 0, 0))
                    best_score = round(score)

                restart = load_image('restart2.png')
                screen.blit(restart, (480, 270))

        clock.tick(30)
        pygame.display.flip()

    pygame.quit()
