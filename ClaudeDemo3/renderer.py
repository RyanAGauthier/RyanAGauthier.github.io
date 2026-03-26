"""All drawing / rendering code."""

import pygame
import math
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BG_TOP, BG_BOTTOM,
    GOLD_COLOR, TEXT_COLOR, DIM_TEXT, WHITE, RED,
    PANEL_BORDER, BTN_COLOR, BTN_HOVER, BTN_DISABLED,
    TILE_W, TILE_H, TILE_D,
    TILE_TOP, TILE_LEFT, TILE_RIGHT,
    TILE_HL_TOP, TILE_HL_LEFT, TILE_HL_RIGHT,
    FLOOR_TOP, FLOOR_LEFT, FLOOR_RIGHT,
    RARITY_COLORS, RARITY_LABELS,
    SHOP_POSITIONS, SHOP_Y, SHOP_SLOTS,
    REFRESH_BTN_W, REFRESH_BTN_H, REFRESH_BTN_Y, REFRESH_COST,
    INV_X, INV_Y, INV_COLS, INV_CELL, INV_PAD,
    DISPLAY_SIZE,
    ORE_X, ORE_Y, ORE_MAX, ORE_COOLDOWN,
)


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.fonts = {
            "title": pygame.font.SysFont(None, 44, bold=True),
            "main":  pygame.font.SysFont(None, 24),
            "small": pygame.font.SysFont(None, 20),
            "gold":  pygame.font.SysFont(None, 32, bold=True),
        }
        # Pre-render gradient background
        self._bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
            pygame.draw.line(self._bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # ── public entry point ───────────────────────────────────────
    def draw_frame(self, *, shop_display, gold, inventory, total_spent,
                   max_inventory, hovered_shop, hovered_inv, hover_refresh,
                   hover_ore, mouse_pos, notifications, particles,
                   pool_remaining, ore_charges, ore_cooldown, targeting=None):
        self.screen.blit(self._bg, (0, 0))
        self._draw_floor()
        self._draw_shop(shop_display, hovered_shop, gold)
        self._draw_ore_pile(ore_charges, ore_cooldown, hover_ore)
        self._draw_title_bar(gold)
        self._draw_refresh_btn(gold, hover_refresh, pool_remaining)
        self._draw_inventory(inventory, hovered_inv, max_inventory, targeting)
        self._draw_stats(inventory, total_spent, max_inventory)
        self._draw_particles(particles)
        self._draw_notifications(notifications)
        if targeting:
            self._draw_targeting_banner()
        self._draw_hints()
        # Tooltips last (on top of everything)
        if not targeting and hovered_shop is not None:
            item = shop_display[hovered_shop]
            if item:
                self._draw_tooltip(item, mouse_pos, gold)
        elif hovered_inv is not None and hovered_inv < len(inventory):
            self._draw_tooltip(inventory[hovered_inv], mouse_pos, gold,
                               owned=True, targeting=targeting)

    # ── background / floor ───────────────────────────────────────
    def _draw_floor(self):
        cx, cy = SCREEN_WIDTH // 2, SHOP_Y + 35
        hw, hh, d = 380, 110, 8
        top  = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        left = [(cx - hw, cy), (cx, cy + hh), (cx, cy + hh + d), (cx - hw, cy + d)]
        right = [(cx + hw, cy), (cx, cy + hh), (cx, cy + hh + d), (cx + hw, cy + d)]
        pygame.draw.polygon(self.screen, FLOOR_LEFT, left)
        pygame.draw.polygon(self.screen, FLOOR_RIGHT, right)
        pygame.draw.polygon(self.screen, FLOOR_TOP, top)
        pygame.draw.polygon(self.screen, (40, 34, 58), top, 1)
        # Subtle grid lines on floor
        for i in range(1, 8):
            t = i / 8
            lx = int(cx - hw + (hw * 2) * t)
            pygame.draw.line(self.screen, (35, 29, 50),
                             (cx + int((lx - cx) * 0.5), cy - hh + int(hh * t)),
                             (cx - int((lx - cx) * 0.5), cy + hh - int(hh * t)), 1)

    # ── shop pedestals + items ───────────────────────────────────
    def _draw_shop(self, display, hovered, gold):
        for i, (cx, cy) in enumerate(SHOP_POSITIONS):
            item = display[i]
            hl = hovered == i and item is not None
            self._draw_pedestal(cx, cy, hl)
            if item:
                self._draw_item_on_pedestal(cx, cy, item, hl, gold)
            else:
                t = self.fonts["small"].render("EMPTY", True, DIM_TEXT)
                self.screen.blit(t, (cx - t.get_width() // 2, cy - t.get_height() // 2))

    def _draw_pedestal(self, cx, cy, highlight=False):
        hw, hh, d = TILE_W // 2, TILE_H // 2, TILE_D
        tc = TILE_HL_TOP if highlight else TILE_TOP
        lc = TILE_HL_LEFT if highlight else TILE_LEFT
        rc = TILE_HL_RIGHT if highlight else TILE_RIGHT
        top  = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        left = [(cx - hw, cy), (cx, cy + hh), (cx, cy + hh + d), (cx - hw, cy + d)]
        right = [(cx + hw, cy), (cx, cy + hh), (cx, cy + hh + d), (cx + hw, cy + d)]
        pygame.draw.polygon(self.screen, lc, left)
        pygame.draw.polygon(self.screen, rc, right)
        pygame.draw.polygon(self.screen, tc, top)
        edge = tuple(min(c + 20, 255) for c in tc)
        pygame.draw.polygon(self.screen, edge, top, 1)

    def _draw_item_on_pedestal(self, cx, cy, item, hovered, gold):
        # Glow behind item
        iy = cy - DISPLAY_SIZE + 4
        gcx, gcy = cx, iy + DISPLAY_SIZE // 2
        radius = 24
        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        rc = RARITY_COLORS[item.rarity]
        for r in range(radius, 0, -2):
            a = int(40 * r / radius)
            pygame.draw.circle(glow, (*rc, a), (radius, radius), r)
        self.screen.blit(glow, (gcx - radius, gcy - radius))
        # Sprite
        spr = item.display_sprite
        self.screen.blit(spr, (cx - spr.get_width() // 2, iy))
        # Price tag
        affordable = gold >= item.price
        pc = GOLD_COLOR if affordable else RED
        ptag = self.fonts["small"].render(f"{item.price}g", True, pc)
        self.screen.blit(ptag, (cx - ptag.get_width() // 2,
                                cy + TILE_H // 2 + TILE_D + 4))
        # Hover border
        if hovered:
            rect = pygame.Rect(cx - DISPLAY_SIZE // 2 - 3, iy - 3,
                               DISPLAY_SIZE + 6, DISPLAY_SIZE + 6)
            pygame.draw.rect(self.screen, rc, rect, 2, border_radius=4)

    # ── Ore pile ─────────────────────────────────────────────────
    def _draw_ore_pile(self, charges, cooldown, hovered):
        cx, cy = ORE_X, ORE_Y
        pct = charges / ORE_MAX if ORE_MAX > 0 else 0

        if charges <= 0:
            # Small rubble remnants
            for dx, dy in [(-8, 2), (5, 4), (-2, 6), (8, 0)]:
                pygame.draw.circle(self.screen, (70, 60, 50), (cx + dx, cy + dy), 3)
            lbl = self.fonts["small"].render("Depleted", True, DIM_TEXT)
            self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 15))
            return

        # Rock cluster — number visible scales with remaining charges
        rocks = [
            (0, 0, 14, (105, 90, 70)),
            (-12, 4, 10, (90, 78, 62)),
            (10, 5, 11, (80, 68, 55)),
            (-5, -8, 9, (95, 82, 65)),
            (7, -6, 8, (110, 95, 75)),
        ]
        n_rocks = max(1, int(len(rocks) * pct))
        for dx, dy, r, col in rocks[:n_rocks]:
            pygame.draw.circle(self.screen, col, (cx + dx, cy + dy), r)
            pygame.draw.circle(self.screen, (60, 50, 40), (cx + dx, cy + dy), r, 1)

        # Gold ore flecks
        flecks = [(-3, -2), (6, 1), (-8, 3), (2, -6), (9, -3), (-6, -7), (4, 5)]
        n_flecks = max(1, int(len(flecks) * pct))
        for gx, gy in flecks[:n_flecks]:
            pygame.draw.circle(self.screen, (220, 190, 60), (cx + gx, cy + gy), 2)

        # Hover glow
        if hovered and cooldown <= 0:
            glow = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 210, 50, 30), (32, 32), 30)
            self.screen.blit(glow, (cx - 32, cy - 32))

        # Cooldown bar
        if cooldown > 0:
            bw, bh = 40, 5
            bx, by = cx - bw // 2, cy + 22
            pygame.draw.rect(self.screen, (40, 35, 50), (bx, by, bw, bh), border_radius=2)
            fill = int(bw * (1.0 - cooldown / ORE_COOLDOWN))
            if fill > 0:
                pygame.draw.rect(self.screen, GOLD_COLOR, (bx, by, fill, bh), border_radius=2)

        # Label
        tc = GOLD_COLOR if (hovered and cooldown <= 0) else TEXT_COLOR
        lbl = self.fonts["small"].render(f"Mine ({charges})", True, tc)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 30))

    # ── UI: title / gold ─────────────────────────────────────────
    def _draw_title_bar(self, gold):
        f = self.fonts["title"]
        shadow = f.render("ARTIFACT EMPORIUM", True, (80, 60, 20))
        title  = f.render("ARTIFACT EMPORIUM", True, GOLD_COLOR)
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(shadow, (tx + 2, 17))
        self.screen.blit(title, (tx, 15))
        # Gold
        lbl = self.fonts["main"].render("Gold:", True, TEXT_COLOR)
        val = self.fonts["gold"].render(str(gold), True, GOLD_COLOR)
        self.screen.blit(lbl, (SCREEN_WIDTH - 150, 22))
        self.screen.blit(val, (SCREEN_WIDTH - 150 + lbl.get_width() + 8, 18))
        # Separator
        pygame.draw.line(self.screen, PANEL_BORDER, (50, 58), (SCREEN_WIDTH - 50, 58))

    # ── UI: refresh button ───────────────────────────────────────
    def _draw_refresh_btn(self, gold, hovered, pool_remaining):
        bx = SCREEN_WIDTH // 2 - REFRESH_BTN_W // 2
        by = REFRESH_BTN_Y
        can = gold >= REFRESH_COST
        bg = BTN_DISABLED if not can else (BTN_HOVER if hovered else BTN_COLOR)
        tc = DIM_TEXT if not can else (WHITE if hovered else TEXT_COLOR)
        pygame.draw.rect(self.screen, bg,
                         (bx, by, REFRESH_BTN_W, REFRESH_BTN_H), border_radius=8)
        pygame.draw.rect(self.screen, PANEL_BORDER,
                         (bx, by, REFRESH_BTN_W, REFRESH_BTN_H), width=2, border_radius=8)
        txt = self.fonts["main"].render(f"REFRESH  -  {REFRESH_COST} gold", True, tc)
        self.screen.blit(txt, (bx + (REFRESH_BTN_W - txt.get_width()) // 2,
                               by + (REFRESH_BTN_H - txt.get_height()) // 2))
        pool_txt = self.fonts["small"].render(f"Pool: {pool_remaining} items", True, DIM_TEXT)
        self.screen.blit(pool_txt, (SCREEN_WIDTH // 2 - pool_txt.get_width() // 2,
                                    by + REFRESH_BTN_H + 6))

    # ── Inventory ────────────────────────────────────────────────
    def _draw_inventory(self, inventory, hovered, max_inventory, targeting=None):
        label = self.fonts["main"].render("YOUR COLLECTION", True, TEXT_COLOR)
        lx = SCREEN_WIDTH // 2 - label.get_width() // 2
        ly = INV_Y - 28
        self.screen.blit(label, (lx, ly))
        deco_y = ly + label.get_height() // 2
        pygame.draw.line(self.screen, PANEL_BORDER, (lx - 50, deco_y), (lx - 5, deco_y))
        pygame.draw.line(self.screen, PANEL_BORDER,
                         (lx + label.get_width() + 5, deco_y),
                         (lx + label.get_width() + 50, deco_y))
        for idx in range(max_inventory):
            row, col = divmod(idx, INV_COLS)
            x = INV_X + col * (INV_CELL + INV_PAD)
            y = INV_Y + row * (INV_CELL + INV_PAD)
            item = inventory[idx] if idx < len(inventory) else None
            hl = hovered == idx and item is not None
            is_source = targeting is not None and idx == targeting.get("source")
            is_target = (targeting is not None and item is not None
                         and not is_source)
            self._draw_inv_cell(x, y, item, hl, is_source, is_target)

    def _draw_inv_cell(self, x, y, item, hovered,
                       is_source=False, is_target=False):
        sz = INV_CELL
        if item:
            rc = RARITY_COLORS[item.rarity]
            bg = tuple(c // 5 for c in rc)
        else:
            rc = (45, 40, 55)
            bg = (20, 16, 30)
        cell = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.rect(cell, (*bg, 180), (0, 0, sz, sz), border_radius=6)
        if hovered:
            pygame.draw.rect(cell, (*rc, 40), (0, 0, sz, sz), border_radius=6)
        border_c = rc
        border_w = 2
        if is_source:
            border_c = GOLD_COLOR
            border_w = 3
        elif is_target and hovered:
            border_c = (255, 100, 100)
            border_w = 3
        pygame.draw.rect(cell, border_c, (0, 0, sz, sz), width=border_w, border_radius=6)
        self.screen.blit(cell, (x, y))
        if item:
            spr = item.display_sprite
            self.screen.blit(spr, (x + (sz - spr.get_width()) // 2,
                                   y + (sz - spr.get_height()) // 2))
            if item.is_useable and not is_source:
                lbl = self.fonts["small"].render("USE", True, GOLD_COLOR)
                self.screen.blit(lbl, (x + sz - lbl.get_width() - 2,
                                       y + sz - lbl.get_height()))

    def _draw_stats(self, inventory, total_spent, max_inventory):
        rows = -(-max_inventory // INV_COLS)   # ceiling division
        y = INV_Y + rows * (INV_CELL + INV_PAD) + 8
        txt = self.fonts["small"].render(
            f"Items: {len(inventory)}/{max_inventory}    Total spent: {total_spent} gold",
            True, DIM_TEXT)
        self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, y))

    # ── Tooltip ──────────────────────────────────────────────────
    def _draw_tooltip(self, item, mouse_pos, gold, owned=False, targeting=None):
        pad, lh = 12, 22
        rc = RARITY_COLORS[item.rarity]
        name_s   = self.fonts["main"].render(item.name, True, rc)
        rarity_s = self.fonts["small"].render(
            f"{RARITY_LABELS[item.rarity]} {item.kind.title()}", True, DIM_TEXT)
        desc_s   = self.fonts["small"].render(item.desc, True, TEXT_COLOR)
        plbl = "Value" if owned else "Price"
        pc = GOLD_COLOR if (owned or gold >= item.price) else RED
        price_s  = self.fonts["main"].render(f"{plbl}: {item.price} gold", True, pc)
        lines = [name_s, rarity_s, None, desc_s, price_s]  # None = spacer
        # Extra line for useable items or targeting info
        if targeting and owned:
            pct = targeting["data"].get("pct", 0)
            gold_back = int(item.price * pct)
            extra = self.fonts["small"].render(
                f"[Salvage → {gold_back} gold]", True, GOLD_COLOR)
            lines.append(extra)
        elif owned and item.is_useable:
            extra = self.fonts["small"].render("[Click to use]", True, GOLD_COLOR)
            lines.append(extra)
        surfs = [l for l in lines if l is not None]
        mw = max(s.get_width() for s in surfs)
        tw = mw + pad * 2
        th = pad * 2 + lh * len(lines) + 6
        tx = max(10, min(mouse_pos[0] + 18, SCREEN_WIDTH - tw - 10))
        ty = max(10, min(mouse_pos[1] + 18, SCREEN_HEIGHT - th - 10))
        bg = pygame.Surface((tw, th), pygame.SRCALPHA)
        pygame.draw.rect(bg, (18, 14, 28, 235), (0, 0, tw, th), border_radius=8)
        pygame.draw.rect(bg, (*rc, 160), (0, 0, tw, th), width=2, border_radius=8)
        self.screen.blit(bg, (tx, ty))
        yo = ty + pad
        for entry in lines:
            if entry is None:
                yo += 6
            else:
                self.screen.blit(entry, (tx + pad, yo))
                yo += lh

    def _draw_targeting_banner(self):
        banner = pygame.Surface((SCREEN_WIDTH, 28), pygame.SRCALPHA)
        pygame.draw.rect(banner, (180, 60, 60, 50), (0, 0, SCREEN_WIDTH, 28))
        txt = self.fonts["main"].render(
            "SELECT A TARGET  |  ESC to cancel", True, (255, 200, 200))
        banner.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2,
                          (28 - txt.get_height()) // 2))
        self.screen.blit(banner, (0, INV_Y - 52))

    # ── Particles / notifications / hints ────────────────────────
    def _draw_particles(self, particles):
        for p in particles:
            a = max(0, min(255, int(255 * p.life / p.max_life)))
            sz = max(1, int(p.size * (p.life / p.max_life)))
            ps = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p.color[:3], a), (sz, sz), sz)
            self.screen.blit(ps, (int(p.x) - sz, int(p.y) - sz))

    def _draw_notifications(self, notifications):
        y = 68
        for n in notifications:
            a = max(0, min(255, int(255 * n.alpha)))
            surf = self.fonts["main"].render(n.text, True, n.color)
            surf.set_alpha(a)
            self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
            y += 24

    def _draw_hints(self):
        txt = self.fonts["small"].render(
            "R: Refresh   |   1-5: Quick Buy   |   ESC: Quit", True, DIM_TEXT)
        self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2,
                               SCREEN_HEIGHT - 25))
