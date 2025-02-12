import pygame


def load_image(fullname, color_key=None):  # Функция для загрузки текстур
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font_size, font=None, type=0, crop: tuple[int, int, int, int] = None,
                 selected_crop=None, offset=(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.selected = False
        self.type = type
        self.text = text
        self.offset = offset
        self.text_font = font
        self.font_size = font_size
        self.image_path = 'data/textures/button-ui.png'

        # 1: играть, 2: ларек, 3: выход, 4: кнопка-в-ларьке, 5: мал-кнопка-в-ларьке, 6: назад (ларек), 7: выйти (игра)
        # 8: заново (проигрыш), 9: выйти (проигрыш), 10: заново (выигрыш), 11: выйти (выигрыш)
        self.im2tp = {0: [crop, selected_crop],
                      1: [(0, 397, 404, 118), 405],
                      2: [(0, 516, 403, 94), 404],
                      3: [(0, 611, 403, 97), 404],
                      4: [(0, 261, 134, 75), 135],
                      5: [(174, 337, 86, 59), 261],
                      6: [(0, 185, 509, 75), 510],
                      7: [(1020, 185, 134, 39), 1155],
                      8: [(0, 0, 309, 91), 310],
                      9: [(0, 92, 309, 92), 310],
                      10: [(620, 0, 309, 91), 930],
                      11: [(620, 92, 309, 92), 931]}
        if type != 0:
            crop, selected_crop = self.im2tp[type]

        self.screen = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.screen.get_rect(topleft=(x, y))

        self.base_image = load_image(self.image_path).subsurface(crop)
        self.image = pygame.transform.scale(self.base_image, (width, height))
        self.selected_image = None
        if selected_crop:  # Если у кнопки есть текстура выделения кнопки, то настраиваем её
            self.selected_image = load_image(self.image_path).subsurface((selected_crop, crop[1], crop[2], crop[3]))
            self.selected_image = pygame.transform.scale(self.selected_image, (width, height))

        self.screen.blit(self.image, (0, 0))

        # Текст на кнопке
        self.font = pygame.font.Font(self.text_font, self.font_size)
        if isinstance(self.text, list):  # "Переносит строчку" при помощи листа
            self.text_label = [self.font.render(i, True, (0, 0, 0)) for i in self.text]
            self.text_x = (width // 2 - self.text_label[0].get_width() // 2) + self.offset[0]
            self.text_y = [((height // 2 - i.get_height() // 2) - 10 + i.get_height() * n + self.offset[1]) for n, i in
                           enumerate(self.text_label)]
            for i in range(len(self.text_label)):
                self.screen.blit(self.text_label[i], (self.text_x, self.text_y[i]))
        else:
            self.text_label = self.font.render(self.text, True, (0, 0, 0))
            self.text_x = width // 2 - self.text_label.get_width() // 2 + self.offset[0]
            self.text_y = (height // 2 - self.text_label.get_height() // 2) + self.offset[1]
            self.screen.blit(self.text_label, (self.text_x, self.text_y))

    def check_cursor_position(self):  # Функция для проверки положения курсора
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):  # Функция для проверки нажатия
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        return False

    def get_rect_coord(self):  # Фукнция для получения координат "хитбокса"
        return self.screen, self.rect.topleft

    def get_text(self):  # Функция для получения текста кнопки
        if isinstance(self.text, list):
            return ''.join(self.text)
        return self.text

    def selecting(self):  # Функция для замены на текстуру выделенной кнопки/возращение на стандартную
        changed = self.selected
        if self.check_cursor_position():
            self.image = self.selected_image
            self.selected = True
        else:
            self.image = self.base_image
            self.selected = False

        # Рендер
        self.screen.blit(self.image, (0, 0))
        if isinstance(self.text_label, list):
            for i in range(len(self.text_label)):
                self.screen.blit(self.text_label[i], (self.text_x, self.text_y[i]))
        else:
            self.screen.blit(self.text_label, (self.text_x, self.text_y))
        return changed != self.selected and self.selected

    def set_image(self, crop: tuple[int, int, int, int] = None,
                  selected_crop=None):  # Функция для постановки новых текстур
        self.base_image = load_image(self.image_path).subsurface(crop)
        self.image = pygame.transform.scale(self.base_image, (self.width, self.height))
        self.selected_image = None
        if selected_crop:  # Если у кнопки есть текстура выделения кнопки, то настраиваем её
            self.selected_image = load_image(self.image_path).subsurface((selected_crop, crop[1], crop[2], crop[3]))
            self.selected_image = pygame.transform.scale(self.selected_image, (self.width, self.height))

        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.text_label, (self.text_x, self.text_y))
