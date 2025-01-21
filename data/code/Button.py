import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font_size, screen, btn_color='gray'):
        super().__init__()
        self.line_text = text
        self.color = btn_color
        self.font_size = font_size
        self.screen = screen

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(surf, pygame.color(color), x, y, width, height)
        self.font = pygame.font.Font(None, font_size)

        color_font = (255, 255, 255)
        if len([i for i in pygame.color(color) if int(i) < 180]) == 3:
            color_font = (0, 0, 0)
        self.text = self.font.render(self.line_text, True, color_font)
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        self.surf.blit(self.text, (text_x, text_y))

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        return False


class MenuButton(Button):
    def __init__(self, x, y, width, height, image_path, text, font_size, screen, text_color=(0, 0, 0)):
        super().__init__(x, y, width, height, text, text_color, font_size)
        self.line_text = text
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.screen = screen

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.surf, (255, 255, 255, 0), x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font = pygame.font.Font(None, font_size)

        self.text = self.font.render(self.line_text, True, self.text_color)
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2

        self.surf.blit(self.image, (0, 0))
        self.surf.blit(self.text, (text_x, text_y))

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        return False
