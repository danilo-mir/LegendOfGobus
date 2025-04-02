import pygame
import os


def import_folder(folder_path):
    # Carregar todos os sprites de uma pasta e retornar uma lista de sprites
    sprites = []

    supported_extensions = {".png", ".jpg", ".jpeg"}

    for filename in os.listdir(folder_path):
        _, ext = os.path.splitext(filename)
        if ext.lower() in supported_extensions:
            file_path = os.path.join(folder_path, filename)
            try:
                sprite = pygame.image.load(file_path).convert_alpha()
                sprites.append(sprite)
            except pygame.error as e:
                print(f"Error loading {file_path}: {e}")

    return sprites
