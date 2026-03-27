"""Item definitions and procedural 32x32 sprite generation."""

import pygame
from config import RARITY_COLORS, DISPLAY_SIZE, SPRITE_SIZE

# ── Item templates ───────────────────────────────────────────────
# Every item has a globally unique price.
ITEM_TEMPLATES = [
    # Common (price 2-12)
    {"name": "Leather Satchel", "kind": "satchel", "rarity": "common", "price": 2,
     "desc": "+4 inventory slots.",
     "effect": {"trigger": "on_buy", "action": "expand_inventory", "amount": 4}},
    {"name": "Rusty Sword",   "kind": "sword",   "rarity": "common", "price": 3,  "desc": "A well-worn blade."},
    {"name": "Wooden Shield", "kind": "shield",  "rarity": "common", "price": 4,  "desc": "Splinters easily."},
    {"name": "Minor Potion",  "kind": "potion",  "rarity": "common", "price": 5,  "desc": "Faintly medicinal."},
    {"name": "Pebble",        "kind": "gem",     "rarity": "common", "price": 6,  "desc": "A shiny rock."},
    {"name": "Tin Ring",      "kind": "ring",    "rarity": "common", "price": 7,  "desc": "Turns fingers green."},
    {"name": "Walking Stick", "kind": "staff",   "rarity": "common", "price": 8,  "desc": "Good for hiking."},
    {"name": "Old Scroll",    "kind": "scroll",  "rarity": "common", "price": 9,  "desc": "Faded text."},
    {"name": "Iron Key",      "kind": "key",     "rarity": "common", "price": 10, "desc": "Opens something."},
    {"name": "Dull Dagger",   "kind": "dagger",  "rarity": "common", "price": 11, "desc": "Needs sharpening."},
    {"name": "Leather Helm",  "kind": "helmet",  "rarity": "common", "price": 12, "desc": "Better than nothing."},
    # Uncommon (price 13-22)
    {"name": "Steel Blade",   "kind": "sword",   "rarity": "uncommon", "price": 13, "desc": "Sharp and reliable."},
    {"name": "Iron Shield",   "kind": "shield",  "rarity": "uncommon", "price": 14, "desc": "Sturdy defense."},
    {"name": "Healing Potion", "kind": "potion", "rarity": "uncommon", "price": 15, "desc": "Restores health."},
    {"name": "Topaz",         "kind": "gem",     "rarity": "uncommon", "price": 16, "desc": "A warm yellow gem."},
    {"name": "Silver Ring",   "kind": "ring",    "rarity": "uncommon", "price": 17, "desc": "Faintly enchanted."},
    {"name": "Oak Staff",     "kind": "staff",   "rarity": "uncommon", "price": 18, "desc": "Channels nature."},
    {"name": "Bone Amulet",   "kind": "amulet",  "rarity": "uncommon", "price": 19, "desc": "Carved from ivory."},
    {"name": "Chain Helm",    "kind": "helmet",  "rarity": "uncommon", "price": 20, "desc": "Chainmail coif."},
    {"name": "Spell Scroll",  "kind": "scroll",  "rarity": "uncommon", "price": 21, "desc": "Contains a spell."},
    {"name": "Glass Orb",     "kind": "orb",     "rarity": "uncommon", "price": 22, "desc": "Faintly glows."},
    {"name": "Salvage Hammer", "kind": "hammer", "rarity": "uncommon", "price": 23,
     "desc": "Salvage items for 75% gold.",
     "effect": {"trigger": "use_on_target", "action": "salvage", "pct": 0.75}},
    # Rare (price 24-34)
    {"name": "Moonblade",      "kind": "sword",   "rarity": "rare", "price": 24, "desc": "Gleams in moonlight."},
    {"name": "Guardian Shield", "kind": "shield", "rarity": "rare", "price": 25, "desc": "Blocks magic."},
    {"name": "Elixir of Power", "kind": "potion", "rarity": "rare", "price": 26, "desc": "Surging energy."},
    {"name": "Sapphire",       "kind": "gem",     "rarity": "rare", "price": 27, "desc": "Deep blue beauty."},
    {"name": "Enchanted Ring", "kind": "ring",    "rarity": "rare", "price": 28, "desc": "Hums with power."},
    {"name": "Arcane Staff",   "kind": "staff",   "rarity": "rare", "price": 29, "desc": "Crackles with energy."},
    {"name": "Phoenix Amulet", "kind": "amulet",  "rarity": "rare", "price": 30, "desc": "Warm to the touch."},
    {"name": "Knight Helm",    "kind": "helmet",  "rarity": "rare", "price": 31, "desc": "Noble headpiece."},
    {"name": "Tome of Lore",   "kind": "book",    "rarity": "rare", "price": 32, "desc": "Ancient knowledge."},
    {"name": "Golden Chalice", "kind": "chalice", "rarity": "rare", "price": 34, "desc": "Ornate goblet."},
    # Epic (price 36-50)
    {"name": "Flamebrand",      "kind": "sword",  "rarity": "epic", "price": 36, "desc": "Burns with fire."},
    {"name": "Aegis",           "kind": "shield", "rarity": "epic", "price": 38, "desc": "Divine protection."},
    {"name": "Dragon Elixir",   "kind": "potion", "rarity": "epic", "price": 40, "desc": "Dragon's essence."},
    {"name": "Star Ruby",       "kind": "gem",    "rarity": "epic", "price": 42, "desc": "Fell from the sky."},
    {"name": "Voidwalker Staff", "kind": "staff", "rarity": "epic", "price": 44, "desc": "Bends reality."},
    {"name": "Demon Crown",    "kind": "crown",   "rarity": "epic", "price": 46, "desc": "Whispers secrets."},
    {"name": "Abyssal Orb",    "kind": "orb",     "rarity": "epic", "price": 48, "desc": "Pulls light inward."},
    {"name": "Skeleton Key",   "kind": "key",     "rarity": "epic", "price": 50, "desc": "Opens any lock."},
    # Legendary (price 60-80)
    {"name": "Excalibur",        "kind": "sword",  "rarity": "legendary", "price": 60, "desc": "The sword of kings."},
    {"name": "Infinity Gem",     "kind": "gem",    "rarity": "legendary", "price": 65, "desc": "Infinite power."},
    {"name": "Staff of Ages",    "kind": "staff",  "rarity": "legendary", "price": 70, "desc": "Transcends time."},
    {"name": "Philosopher Stone", "kind": "orb",   "rarity": "legendary", "price": 75, "desc": "Transmutes matter."},
    {"name": "Emperor Crown",   "kind": "crown",   "rarity": "legendary", "price": 80, "desc": "Rules all."},
]


# ── Item class ───────────────────────────────────────────────────
class Item:
    """An artifact with name, stats, an optional effect, and a procedural sprite.

    Effects are dicts stored on the template.  Two trigger types are supported:

    * ``"on_buy"``        – executed at purchase time; item is consumed (never
      enters inventory).  The ``"action"`` key selects the handler in
      ``Game._apply_buy_effect``.
    * ``"use_on_target"`` – item goes into inventory and can be activated by
      clicking it.  The game enters targeting mode and the ``"action"`` key
      selects the handler in ``Game._apply_target``.

    To add a new effect, create a template with the appropriate ``"effect"``
    dict and add a handler branch in the corresponding Game method.
    """

    _sprite_cache: dict = {}
    _scaled_cache: dict = {}

    def __init__(self, template: dict):
        self.name: str = template["name"]
        self.kind: str = template["kind"]
        self.rarity: str = template["rarity"]
        self.price: int = template["price"]
        self.desc: str = template["desc"]
        self.effect: dict | None = template.get("effect")

    # ── effect queries ───────────────────────────────────────────
    @property
    def consumed_on_buy(self) -> bool:
        """Item is consumed on purchase and never enters inventory."""
        return self.effect is not None and self.effect.get("trigger") == "on_buy"

    @property
    def is_useable(self) -> bool:
        """Item can be activated from inventory on a target."""
        return self.effect is not None and self.effect.get("trigger") == "use_on_target"

    # ── sprites ──────────────────────────────────────────────────
    @property
    def sprite(self) -> pygame.Surface:
        key = (self.kind, self.rarity)
        if key not in Item._sprite_cache:
            Item._sprite_cache[key] = _generate_sprite(self.kind, self.rarity)
        return Item._sprite_cache[key]

    @property
    def display_sprite(self) -> pygame.Surface:
        key = (self.kind, self.rarity)
        if key not in Item._scaled_cache:
            Item._scaled_cache[key] = pygame.transform.scale(
                self.sprite, (DISPLAY_SIZE, DISPLAY_SIZE)
            )
        return Item._scaled_cache[key]


# ── Sprite generation ────────────────────────────────────────────

def _clamp(c):
    """Clamp colour tuple to 0-255."""
    return tuple(max(0, min(255, v)) for v in c)

def _lighter(c, amt=50):
    return _clamp((c[0] + amt, c[1] + amt, c[2] + amt))

def _darker(c, amt=40):
    return _clamp((c[0] - amt, c[1] - amt, c[2] - amt))


def _draw_sword(s, c):
    """Blade pointing up, crossguard, wrapped handle, pommel."""
    blade = (190, 195, 210)
    pygame.draw.polygon(s, blade, [(14, 3), (18, 3), (19, 19), (13, 19)])
    pygame.draw.line(s, _lighter(blade, 30), (16, 4), (16, 18))
    pygame.draw.polygon(s, _darker(blade, 20), [(14, 3), (16, 2), (18, 3), (16, 4)])
    pygame.draw.rect(s, c, (9, 19, 14, 3))
    pygame.draw.line(s, _lighter(c), (10, 20), (22, 20))
    pygame.draw.rect(s, (110, 75, 35), (14, 22, 4, 6))
    pygame.draw.line(s, (90, 60, 25), (15, 23), (15, 27))
    pygame.draw.circle(s, c, (16, 30), 2)


def _draw_shield(s, c):
    """Heater shield with cross emblem."""
    body = (140, 110, 70)
    pts = [(8, 5), (24, 5), (26, 17), (16, 28), (6, 17)]
    pygame.draw.polygon(s, body, pts)
    pygame.draw.polygon(s, c, pts, 2)
    pygame.draw.line(s, c, (16, 9), (16, 23), 2)
    pygame.draw.line(s, c, (10, 15), (22, 15), 2)
    pygame.draw.polygon(s, _lighter(body, 20), [(8, 5), (16, 5), (16, 16), (6, 17)])


def _draw_potion(s, c):
    """Glass bottle with coloured liquid."""
    glass = (180, 195, 210)
    pygame.draw.rect(s, glass, (10, 15, 12, 13), border_radius=3)
    pygame.draw.rect(s, c, (11, 20, 10, 7), border_radius=2)
    pygame.draw.rect(s, glass, (13, 9, 6, 7))
    pygame.draw.rect(s, (160, 120, 60), (13, 6, 6, 4), border_radius=1)
    pygame.draw.line(s, _lighter(glass, 40), (12, 11), (12, 24))


def _draw_gem(s, c):
    """Faceted octagonal gemstone."""
    pts = [(16, 4), (22, 8), (24, 16), (22, 24),
           (16, 28), (10, 24), (8, 16), (10, 8)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, _lighter(c, 60), [(16, 4), (22, 8), (18, 16), (16, 14)])
    pygame.draw.polygon(s, _lighter(c, 40), [(16, 4), (10, 8), (14, 16), (16, 14)])
    pygame.draw.polygon(s, _darker(c), pts, 1)
    pygame.draw.circle(s, (255, 255, 255), (14, 10), 1)


def _draw_ring(s, c):
    """Band with mounted gem."""
    band = (200, 180, 80)
    pygame.draw.circle(s, band, (16, 18), 8, 3)
    pygame.draw.circle(s, _lighter(band), (16, 18), 8, 1)
    pygame.draw.circle(s, c, (16, 10), 4)
    pygame.draw.circle(s, _lighter(c, 60), (15, 9), 2)


def _draw_staff(s, c):
    """Wooden staff with glowing orb tip."""
    wood = (120, 85, 45)
    pygame.draw.line(s, wood, (16, 10), (16, 29), 3)
    pygame.draw.line(s, _lighter(wood, 20), (15, 10), (15, 29), 1)
    pygame.draw.circle(s, c, (16, 7), 6)
    pygame.draw.circle(s, _lighter(c, 70), (14, 5), 3)
    pygame.draw.circle(s, (255, 255, 255), (13, 4), 1)
    pygame.draw.line(s, _darker(wood), (13, 28), (19, 28), 2)


def _draw_amulet(s, c):
    """Chain necklace with gemmed pendant."""
    chain = (200, 180, 80)
    pygame.draw.lines(s, chain, False, [(8, 3), (16, 13), (24, 3)], 2)
    pygame.draw.circle(s, _darker(chain), (16, 18), 7)
    pygame.draw.circle(s, c, (16, 18), 5)
    pygame.draw.circle(s, _lighter(c, 55), (15, 17), 2)


def _draw_helmet(s, c):
    """Domed helm with visor slit."""
    metal = (150, 155, 165)
    pygame.draw.ellipse(s, metal, (7, 5, 18, 16))
    pygame.draw.rect(s, _darker(metal, 20), (9, 17, 14, 7))
    pygame.draw.rect(s, (30, 25, 40), (10, 18, 12, 2))
    pygame.draw.line(s, c, (16, 5), (16, 21), 2)
    pygame.draw.ellipse(s, c, (7, 20, 18, 6), 1)


def _draw_scroll(s, c):
    """Rolled parchment with wax seal."""
    parch = (220, 200, 160)
    pygame.draw.rect(s, parch, (10, 8, 12, 16))
    pygame.draw.ellipse(s, _darker(parch, 20), (8, 5, 16, 7))
    pygame.draw.ellipse(s, _darker(parch, 20), (8, 20, 16, 7))
    pygame.draw.circle(s, c, (16, 16), 3)
    for y in range(10, 22, 3):
        pygame.draw.line(s, _darker(parch, 40), (12, y), (20, y))


def _draw_orb(s, c):
    """Translucent magical sphere."""
    glow = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*c, 35), (16, 16), 14)
    s.blit(glow, (0, 0))
    pygame.draw.circle(s, c, (16, 16), 10)
    pygame.draw.circle(s, _lighter(c, 80), (13, 12), 4)
    pygame.draw.circle(s, (255, 255, 255), (12, 11), 2)
    pygame.draw.circle(s, _darker(c), (16, 16), 10, 1)


def _draw_dagger(s, c):
    """Short blade angled slightly."""
    blade = (185, 190, 205)
    pygame.draw.polygon(s, blade, [(15, 4), (19, 7), (17, 20), (15, 20)])
    pygame.draw.line(s, _lighter(blade, 30), (16, 5), (16, 19))
    pygame.draw.rect(s, c, (12, 20, 8, 2))
    pygame.draw.rect(s, (110, 75, 35), (14, 22, 4, 5))
    pygame.draw.circle(s, c, (16, 28), 2)


def _draw_crown(s, c):
    """Royal crown with three jewels."""
    pts = [(7, 20), (9, 8), (12, 16), (16, 4), (20, 16), (23, 8), (25, 20)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.rect(s, c, (7, 20, 18, 6))
    pygame.draw.line(s, _lighter(c, 40), (8, 21), (24, 21))
    pygame.draw.circle(s, (255, 50, 50), (16, 8), 2)
    pygame.draw.circle(s, (50, 50, 255), (10, 14), 2)
    pygame.draw.circle(s, (50, 220, 50), (22, 14), 2)


def _draw_book(s, c):
    """Leather-bound tome with clasp."""
    pygame.draw.rect(s, c, (8, 6, 16, 22))
    pygame.draw.rect(s, _darker(c, 60), (8, 6, 3, 22))
    pygame.draw.rect(s, (230, 220, 200), (11, 8, 11, 18))
    for y in range(10, 24, 3):
        pygame.draw.line(s, (190, 180, 160), (13, y), (20, y))
    pygame.draw.rect(s, _darker(c), (8, 6, 16, 22), 1)
    pygame.draw.rect(s, (200, 180, 80), (23, 15, 2, 4))


def _draw_chalice(s, c):
    """Ornate goblet with liquid inside."""
    pygame.draw.polygon(s, c, [(8, 6), (24, 6), (22, 16), (10, 16)])
    pygame.draw.ellipse(s, _lighter(c, 40), (8, 3, 16, 7), 1)
    pygame.draw.rect(s, (150, 30, 40), (10, 8, 12, 7))
    pygame.draw.rect(s, c, (14, 16, 4, 6))
    pygame.draw.ellipse(s, c, (10, 22, 12, 6))
    pygame.draw.ellipse(s, _lighter(c, 30), (10, 22, 12, 6), 1)


def _draw_key(s, c):
    """Ornate key with circular bow."""
    pygame.draw.circle(s, c, (16, 9), 6, 2)
    pygame.draw.circle(s, _lighter(c, 40), (16, 9), 3)
    pygame.draw.rect(s, c, (15, 14, 3, 13))
    pygame.draw.rect(s, c, (18, 21, 4, 2))
    pygame.draw.rect(s, c, (18, 25, 3, 2))


def _draw_hammer(s, c):
    """Salvage hammer with a heavy head."""
    wood = (120, 85, 45)
    # Handle (diagonal)
    pygame.draw.line(s, wood, (10, 28), (18, 10), 3)
    pygame.draw.line(s, _lighter(wood, 20), (9, 28), (17, 10), 1)
    # Head
    head = (160, 155, 170)
    pygame.draw.rect(s, head, (12, 4, 14, 9), border_radius=2)
    pygame.draw.rect(s, _darker(head, 20), (12, 4, 14, 9), 1, border_radius=2)
    pygame.draw.line(s, _lighter(head, 40), (13, 5), (25, 5))
    # Accent gem on head
    pygame.draw.circle(s, c, (19, 8), 3)
    pygame.draw.circle(s, _lighter(c, 50), (18, 7), 1)


def _draw_satchel(s, c):
    """Leather bag that expands inventory."""
    leather = (155, 105, 55)
    dark = (120, 80, 40)
    # Body
    pygame.draw.rect(s, leather, (7, 13, 18, 14), border_radius=4)
    pygame.draw.rect(s, dark, (7, 13, 18, 14), 1, border_radius=4)
    # Flap
    pygame.draw.polygon(s, _lighter(leather, 15), [(7, 13), (25, 13), (23, 7), (9, 7)])
    pygame.draw.polygon(s, dark, [(7, 13), (25, 13), (23, 7), (9, 7)], 1)
    # Buckle
    pygame.draw.rect(s, (200, 180, 80), (14, 9, 4, 4), border_radius=1)
    # Straps
    pygame.draw.line(s, dark, (10, 7), (13, 3), 2)
    pygame.draw.line(s, dark, (22, 7), (19, 3), 2)
    # Plus sign (indicates expansion)
    pygame.draw.line(s, c, (13, 21), (19, 21), 2)
    pygame.draw.line(s, c, (16, 18), (16, 24), 2)


# ── Lookup table ─────────────────────────────────────────────────
_DRAW_FUNCS = {
    "sword": _draw_sword,
    "shield": _draw_shield,
    "potion": _draw_potion,
    "gem": _draw_gem,
    "ring": _draw_ring,
    "staff": _draw_staff,
    "amulet": _draw_amulet,
    "helmet": _draw_helmet,
    "scroll": _draw_scroll,
    "orb": _draw_orb,
    "dagger": _draw_dagger,
    "crown": _draw_crown,
    "book": _draw_book,
    "chalice": _draw_chalice,
    "key": _draw_key,
    "satchel": _draw_satchel,
    "hammer": _draw_hammer,
}


def _generate_sprite(kind: str, rarity: str) -> pygame.Surface:
    color = RARITY_COLORS[rarity]
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    _DRAW_FUNCS.get(kind, _draw_gem)(surf, color)
    return surf
