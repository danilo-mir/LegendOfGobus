WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 56
GRASSSIZE = 25
PLAYERSIZE = 30

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE= 80
UI_FONT = 'graphics/font/medieval-pixel.otf'
UI_FONT_SIZE = 30
UI_BIGGER_FONT_SIZE = 30
EXP_PADDING_X = 70
EXP_PADDING_Y = 45
SUPER_PADDING_X = 150
SUPER_PADDING_Y = 10
SUPER_RADIUS = 35
BORDER = 3

# Levels
FORESTBG = 'graphics/tilemap/forestground.jpeg'
DESERTBG = 'graphics/tilemap/desertground.png'

# Menu
BG = 'graphics/tilemap/menuimage.png'

# Cores
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
SUPER_BUTTON_NOT_AVAILABLE_COLOR = (64, 64, 64)
SUPER_BUTTON_AVAILABLE_COLOR = (218, 165, 32)
SUPER_LOADING_COLOR = (218, 165, 32)


# Cores da UI
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

DEFAULT_PLAYER_STATS = {
  'max_health': 100,
  'max_energy': 100,
  'speed': 5,
  'super_threshold': 10
}

# Mapas
WORLD_MAP = [
 ['T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', ',', ',' , ',', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2'],
 ['T2', ',', ',', ',' , ',', ',', ',', ',', 'G2', ',', ',', ',' , ',', ',', ',' , ',', ',', 'G2', ',', ',', ',', ',', 'T2'],
 ['T2', ',', ',', ',' , ',', ',', 'T3', ',', ',', ',', 'T3', ',' , 'G2', ',', ',' , ',', ',', ',', ',', ',', ',', ',', 'T2'],
 ['T2', ',', 'T3', ',' , 'T1', ',', ',', ',', ',', ',', ',', ',' , ',', ',', 'TR2' , ',', ',', ',', 'T2', ',', ',', ',', 'T2'],
 ['T2', ',', ',', ',' , ',', ',', 'T2', ',', ',', ',', ',', 'TR2' , ',', ',', ',' , ',', ',', ',', ',', ',', ',', ',', 'T2'],
 ['T2', ',', ',', ',' , ',', ',', ',', ',', 'TR1', ',', ',', ',' , ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'T2'],
 [',', ',', ',', ',' , ',', 'G2', ',', ',', ',', ',', ',', 'P' , ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ','],
 ['T2', ',', 'TR2', ',' , ',', ',', ',', ',', ',', ',', ',', ',' , ',', ',', 'T3' , ',', 'G2', ',', ',', 'TR1', ',', ',', 'T2'],
 ['T2', ',', ',', ',' , ',', ',', 'G1', ',', 'TR1', ',', ',', ',' , 'G3', ',', ',' , ',', ',', ',', ',', ',', ',', ',', 'T2'],
 ['T2', ',', ',', 'T1' , ',', ',', ',', ',', ',', ',', 'G3', ',' , ',', ',', ',' , ',', ',', ',', 'T3', ',', ',', ',', 'T2'],
 ['T2', 'G3', ',', ',' , ',', 'G2', ',', ',', 'R', ',', ',', 'G1' , ',', 'TR2', ',' , ',', ',', ',', ',', ',', ',', ',', 'T2'],
 ['T2', ',', ',', ',' , 'T1', ',', ',', ',', ',', ',', ',', ',' , ',', ',', ',' , ',', ',', ',', ',', ',', ',', ',', 'T2'],
 ['T2', 'T2', 'T2', 'T2' , 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', ',', ',', ',', 'T2', 'T2' , 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2'],
]

monster_symbol = {'sq': "squid", 'rc': "raccoon"}

monster_data = {
    'squid': {
      'health': 100, 
      'exp': 100,
      'damage': 20, 
      'attack_type': 'slash', 
      'attack_sound': '../audio/attack/slash.wav',
      'speed': 3, 'resistance': 3, 
      'attack_radius': 80, 
      'notice_radius': 360
      },

    'raccoon': {
      'health': 300, 
      'exp':250, 
      'damage': 40, 
      'attack_type': 
      'claw',  'attack_sound': '../audio/attack/claw.wav',
      'speed': 2, 'resistance': 3, 
      'attack_radius': 120, 
      'notice_radius': 400
      },

    'spirit': {
      'health': 100,
      'exp':110, 
      'damage': 8, 
      'attack_type': 
      'thunder', 
      'attack_sound': '../audio/attack/fireball.wav', 
      'speed': 4, 
      'resistance': 3, 
      'attack_radius': 60, 
      'notice_radius': 350
      },
      
    'bamboo': {
      'health': 70,
      'exp':120, 
      'damage': 6, 
      'attack_type': 'leaf_attack', 
      'attack_sound': '../audio/attack/slash.wav', 
      'speed': 3, 'resistance': 3, 
      'attack_radius': 50, 
      'notice_radius': 300
      }
}
