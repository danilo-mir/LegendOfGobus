import pygame
from settings import *
from math import pi
from support import fetch_weapon_data


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.bigger_font = pygame.font.Font(UI_FONT, UI_BIGGER_FONT_SIZE)

        # Barra de vida
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        
        # Carregar imagens de munição
        self.ammo_images = []
        for i in range(6):  # 0 a 5 balas
            img = pygame.image.load(f'graphics/weapons/municao/municao_{i}.png').convert_alpha()
            # Reduzir pela metade o tamanho da imagem
            img_width = img.get_width() // 2
            img_height = img.get_height() // 2
            img = pygame.transform.scale(img, (img_width, img_height))
            self.ammo_images.append(img)
        
        # Posição da imagem de munição (ajustada para o novo tamanho)
        self.ammo_rect = pygame.Rect(10, 40, 50, 20)  # x, y, width, height reduzidos pela metade

        self.weapon_data = fetch_weapon_data()

    def show_bar(self, current, max_amount, bg_rect, color):
        # Background da barra
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Desenhar a barra
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
    
    def show_ammo(self, ammo):
        # Garantir que ammo esteja nos limites (0-5)
        ammo_index = max(0, min(ammo, 5))
        
        # Mostrar a imagem correspondente à quantidade de munição
        ammo_image = self.ammo_images[ammo_index]
        self.display_surface.blit(ammo_image, self.ammo_rect)

    # Mostrar o XP
    def show_exp(self, exp):
        text_surf = self.font.render('EXP: ' + str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(WIDTH - EXP_PADDING_X, HEIGHT - EXP_PADDING_Y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, current_weapon):
        bg_rect = self.selection_box(10, 630)
        weapon_surf = self.weapon_data[current_weapon]['graphic']
        weapon_image = pygame.image.load(weapon_surf + '/up.png').convert_alpha()
        weapon_rect = weapon_image.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_image, weapon_rect)


    # Mostrar o círculo do super ataque
    def show_super(self, current, max_amount, color):
        ratio = current / max_amount
        current_angle = ratio * 2 * pi
        if ratio >= 1:
            ratio = 1
            color_button = SUPER_BUTTON_AVAILABLE_COLOR
        else:
            color_button = SUPER_BUTTON_NOT_AVAILABLE_COLOR
        current_angle = ratio * 2 * pi

        # Círculo do super ataque
        pos = (WIDTH - SUPER_PADDING_X - SUPER_RADIUS, HEIGHT - SUPER_PADDING_Y - SUPER_RADIUS)
        text_surf = self.bigger_font.render('R', False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=pos)
        pygame.draw.circle(self.display_surface, color_button, pos, SUPER_RADIUS)
        self.display_surface.blit(text_surf, text_rect)

        # Barra de carregamento do super ataque
        load_rect = pygame.Rect(pos[0] - SUPER_RADIUS, pos[1] - SUPER_RADIUS, 2 * SUPER_RADIUS, 2 * SUPER_RADIUS)
        pygame.draw.arc(self.display_surface, color, load_rect, pi / 2, pi / 2 + current_angle)

    def display(self, player):
        self.show_bar(player.health, player.player_stats['max_health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_ammo(player.ammo)  # Mostrar munição ao invés da barra de energia
        self.show_exp(player.exp)
        self.show_super(player.super_counter, player.player_stats['super_threshold'], SUPER_LOADING_COLOR)
        self.weapon_overlay(player.current_weapon)
