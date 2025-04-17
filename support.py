from csv import reader
from os import walk
import os
import json
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder_player(folder_path):
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


def import_folder_enemy(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def fetch_weapon_data():
    with open('weapons.json') as weapon_data_json:
        return json.load(weapon_data_json)


def fetch_enemy_data():
    with open('enemies.json') as enemies_data_json:
        return json.load(enemies_data_json)
