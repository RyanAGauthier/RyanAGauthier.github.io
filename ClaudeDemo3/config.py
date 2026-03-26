"""Game configuration constants."""

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Artifact Emporium"

# ── Colours ──────────────────────────────────────────────────────
BG_TOP = (22, 16, 35)
BG_BOTTOM = (12, 8, 22)
GOLD_COLOR = (255, 210, 50)
TEXT_COLOR = (225, 220, 215)
DIM_TEXT = (120, 115, 110)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 200, 80)

PANEL_BG = (28, 22, 42)
PANEL_BORDER = (50, 42, 70)
BTN_COLOR = (42, 35, 60)
BTN_HOVER = (58, 48, 82)
BTN_DISABLED = (32, 28, 45)

# Isometric tile palette
TILE_TOP = (48, 40, 68)
TILE_LEFT = (35, 28, 52)
TILE_RIGHT = (24, 19, 38)
TILE_HL_TOP = (68, 58, 100)
TILE_HL_LEFT = (50, 42, 72)
TILE_HL_RIGHT = (38, 32, 55)
FLOOR_TOP = (30, 25, 45)
FLOOR_LEFT = (22, 18, 35)
FLOOR_RIGHT = (16, 13, 26)

# Rarity
RARITY_COLORS = {
    "common": (170, 170, 180),
    "uncommon": (50, 200, 55),
    "rare": (60, 130, 255),
    "epic": (180, 75, 255),
    "legendary": (255, 150, 30),
}
RARITY_LABELS = {
    "common": "Common",
    "uncommon": "Uncommon",
    "rare": "Rare",
    "epic": "Epic",
    "legendary": "Legendary",
}
POOL_SIZES = {"common": 8, "uncommon": 6, "rare": 4, "epic": 3, "legendary": 1}

# ── Game mechanics ───────────────────────────────────────────────
STARTING_GOLD = 100
SHOP_SLOTS = 5
REFRESH_COST = 2
MAX_INVENTORY = 16

# ── Layout ───────────────────────────────────────────────────────
TILE_W = 96
TILE_H = 48
TILE_D = 16
SHOP_Y = 230
SHOP_SPACING = 130

SHOP_POSITIONS = []
_span = (SHOP_SLOTS - 1) * SHOP_SPACING
_sx = (SCREEN_WIDTH - _span) // 2
for _i in range(SHOP_SLOTS):
    SHOP_POSITIONS.append((_sx + _i * SHOP_SPACING, SHOP_Y))

REFRESH_BTN_W = 200
REFRESH_BTN_H = 38
REFRESH_BTN_Y = 365

# Ore pile
ORE_X = 920
ORE_Y = 300
ORE_MAX = 15
ORE_COOLDOWN = 1.5        # seconds between mines
ORE_GOLD_MIN = 1
ORE_GOLD_MAX = 3
ORE_RECHARGE = 3           # charges restored per shop refresh
ORE_HIT_RADIUS = 30

INV_COLS = 8
INV_CELL = 58
INV_PAD = 8
INV_Y = 480
INV_X = (SCREEN_WIDTH - INV_COLS * (INV_CELL + INV_PAD) + INV_PAD) // 2

SPRITE_SIZE = 32
DISPLAY_SIZE = 44
