#!/usr/bin/env python3
"""Artifact Emporium — isometric autochess-style shop game."""

import asyncio
import pygame
import sys
import random
import math

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    GOLD_COLOR, RED, GREEN, DIM_TEXT, STARTING_GOLD, SHOP_SLOTS,
    REFRESH_COST, MAX_INVENTORY, RARITY_COLORS,
    SHOP_POSITIONS, TILE_W, TILE_H, DISPLAY_SIZE,
    REFRESH_BTN_W, REFRESH_BTN_H, REFRESH_BTN_Y,
    INV_X, INV_Y, INV_COLS, INV_CELL, INV_PAD,
    ORE_X, ORE_Y, ORE_MAX, ORE_COOLDOWN,
    ORE_GOLD_MIN, ORE_GOLD_MAX, ORE_RECHARGE, ORE_HIT_RADIUS,
)
from shop import Shop
from renderer import Renderer
from audio import Audio


# ── Small helper classes ─────────────────────────────────────────

class Notification:
    """Brief on-screen message that fades out."""
    def __init__(self, text, color, duration=2.0):
        self.text = text
        self.color = color
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt
        return self.age < self.duration

    @property
    def alpha(self):
        if self.age < 0.15:
            return self.age / 0.15
        if self.age > self.duration - 0.5:
            return max(0.0, (self.duration - self.age) / 0.5)
        return 1.0


class Particle:
    """Visual sparkle / burst particle."""
    __slots__ = ("x", "y", "vx", "vy", "color", "life", "max_life", "size")

    def __init__(self, x, y, vx, vy, color, life=1.0, size=2.0):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.color = color
        self.life = self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 30 * dt
        self.life -= dt
        return self.life > 0


# ── Main game ────────────────────────────────────────────────────

class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.shop = Shop()
        self.renderer = Renderer(self.screen)
        self.audio = Audio()

        self.gold = STARTING_GOLD
        self.inventory: list = []
        self.total_spent = 0
        self.max_inventory = MAX_INVENTORY

        # Ore pile state
        self.ore_charges = ORE_MAX
        self.ore_cooldown = 0.0

        self.hovered_shop: int | None = None
        self.hovered_inv: int | None = None
        self.hover_refresh = False
        self.hover_ore = False
        self.mouse_pos = (0, 0)

        # Targeting mode: {"source": inv_index, "data": effect_dict}
        self.targeting: dict | None = None

        self.notifications: list[Notification] = []
        self.particles: list[Particle] = []
        self._ambient_timer = 0.0
        self.running = True

    # ── loop ─────────────────────────────────────────────────────
    async def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._render()
            pygame.display.flip()
            await asyncio.sleep(0)   # yield to browser event loop (pygbag)
        pygame.quit()

    # ── events ───────────────────────────────────────────────────
    def _handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEMOTION:
                self.mouse_pos = ev.pos
                self._update_hover()
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._handle_click()
            elif ev.type == pygame.KEYDOWN:
                self._handle_key(ev.key)

    def _handle_key(self, key):
        if key == pygame.K_ESCAPE:
            if self.targeting:
                self.targeting = None
                self._notify("Targeting cancelled.", DIM_TEXT)
            else:
                self.running = False
        elif key == pygame.K_r:
            self._refresh_shop()
        elif key == pygame.K_m:
            muted = self.audio.toggle_mute()
            self._notify("Sound muted" if muted else "Sound enabled", DIM_TEXT)
        elif pygame.K_1 <= key <= pygame.K_5:
            self._buy_item(key - pygame.K_1)

    def _handle_click(self):
        if self.targeting:
            if self.hovered_inv is not None:
                self._apply_target(self.hovered_inv)
            else:
                self.targeting = None
                self._notify("Targeting cancelled.", DIM_TEXT)
            return
        if self.hovered_shop is not None:
            self._buy_item(self.hovered_shop)
        elif self.hovered_inv is not None:
            self._click_inventory(self.hovered_inv)
        elif self.hover_refresh:
            self._refresh_shop()
        elif self.hover_ore:
            self._mine_ore()

    # ── hover detection ──────────────────────────────────────────
    def _update_hover(self):
        mx, my = self.mouse_pos

        # Shop slots
        self.hovered_shop = None
        for i, (cx, cy) in enumerate(SHOP_POSITIONS):
            if self.shop.display[i] is not None:
                if abs(mx - cx) < TILE_W // 2 + 4 and abs(my - (cy - 15)) < TILE_H // 2 + 22:
                    self.hovered_shop = i
                    break

        # Inventory cells
        self.hovered_inv = None
        for i in range(len(self.inventory)):
            row, col = divmod(i, INV_COLS)
            cx = INV_X + col * (INV_CELL + INV_PAD)
            cy = INV_Y + row * (INV_CELL + INV_PAD)
            if cx <= mx < cx + INV_CELL and cy <= my < cy + INV_CELL:
                self.hovered_inv = i
                break

        # Refresh button
        bx = SCREEN_WIDTH // 2 - REFRESH_BTN_W // 2
        self.hover_refresh = (
            bx <= mx < bx + REFRESH_BTN_W
            and REFRESH_BTN_Y <= my < REFRESH_BTN_Y + REFRESH_BTN_H
        )

        # Ore pile
        dx, dy = mx - ORE_X, my - ORE_Y
        self.hover_ore = (dx * dx + dy * dy < ORE_HIT_RADIUS ** 2
                          and self.ore_charges > 0)

    # ── game actions ─────────────────────────────────────────────
    def _buy_item(self, slot):
        if slot < 0 or slot >= SHOP_SLOTS:
            return
        item = self.shop.display[slot]
        if item is None:
            return
        if self.gold < item.price:
            self.audio.play("error")
            self._notify("Not enough gold!", RED)
            return

        if not item.consumed_on_buy and len(self.inventory) >= self.max_inventory:
            self.audio.play("error")
            self._notify("Inventory full!", RED)
            return

        self.gold -= item.price
        self.total_spent += item.price
        self.shop.buy(slot)
        self._update_hover()

        cx, cy = SHOP_POSITIONS[slot]
        if item.consumed_on_buy:
            self._apply_buy_effect(item, cx, cy)
        else:
            self.inventory.append(item)
            self._burst(cx, cy - 25, RARITY_COLORS[item.rarity])
            self.audio.play_buy(item.rarity)
            self._notify(f"Purchased {item.name}!", RARITY_COLORS[item.rarity])

    def _apply_buy_effect(self, item, cx, cy):
        eff = item.effect
        action = eff["action"]
        if action == "expand_inventory":
            amt = eff["amount"]
            self.max_inventory += amt
            self._burst(cx, cy - 25, GREEN)
            self.audio.play("expand")
            self._notify(f"Inventory expanded! (+{amt} slots)", GREEN)

    def _click_inventory(self, idx):
        if idx >= len(self.inventory):
            return
        item = self.inventory[idx]
        if item.is_useable:
            self._use_item(idx)

    def _use_item(self, idx):
        item = self.inventory[idx]
        self.targeting = {"source": idx, "data": item.effect}
        self.audio.play("use")
        self._notify(f"Select a target for {item.name}...", RARITY_COLORS[item.rarity])

    def _apply_target(self, target_idx):
        if target_idx >= len(self.inventory):
            self.targeting = None
            return
        src = self.targeting["source"]
        data = self.targeting["data"]
        self.targeting = None

        if target_idx == src:
            self._notify("Can't target itself!", RED)
            return

        action = data["action"]
        if action == "salvage":
            target_item = self.inventory[target_idx]
            gold_back = int(target_item.price * data["pct"])
            self.gold += gold_back
            # Remove target first (higher index first if needed)
            to_remove = sorted([src, target_idx], reverse=True)
            for i in to_remove:
                self.inventory.pop(i)
            row, col = divmod(target_idx, INV_COLS)
            bx = INV_X + col * (INV_CELL + INV_PAD) + INV_CELL // 2
            by = INV_Y + row * (INV_CELL + INV_PAD) + INV_CELL // 2
            self._burst(bx, by, GOLD_COLOR)
            self.audio.play("salvage")
            self._notify(f"Salvaged {target_item.name} for {gold_back} gold!", GOLD_COLOR)

    def _refresh_shop(self):
        if self.gold < REFRESH_COST:
            self.audio.play("error")
            self._notify("Not enough gold to refresh!", RED)
            return
        self.gold -= REFRESH_COST
        self.total_spent += REFRESH_COST
        self.shop.refresh()
        # Ore recharges on refresh
        self.ore_charges = min(ORE_MAX, self.ore_charges + ORE_RECHARGE)
        self._update_hover()
        self.audio.play("refresh")
        self._notify("Shop refreshed!", GOLD_COLOR)

    def _mine_ore(self):
        if self.ore_charges <= 0:
            self.audio.play("error")
            self._notify("Ore depleted!", DIM_TEXT)
            return
        if self.ore_cooldown > 0:
            return
        gold_gained = random.randint(ORE_GOLD_MIN, ORE_GOLD_MAX)
        self.gold += gold_gained
        self.ore_charges -= 1
        self.ore_cooldown = ORE_COOLDOWN
        self._burst(ORE_X, ORE_Y - 10, (200, 180, 60))
        self.audio.play("mine")
        self._notify(f"Mined {gold_gained} gold!", GOLD_COLOR)

    # ── effects ──────────────────────────────────────────────────
    def _notify(self, text, color):
        self.notifications.append(Notification(text, color))

    def _burst(self, x, y, color):
        lighter = tuple(min(c + 60, 255) for c in color)
        for _ in range(20):
            a = random.uniform(0, math.tau)
            spd = random.uniform(50, 150)
            self.particles.append(
                Particle(x, y, math.cos(a) * spd, math.sin(a) * spd - 50,
                         lighter, random.uniform(0.5, 1.2), random.uniform(2, 5))
            )

    # ── update ───────────────────────────────────────────────────
    def _update(self, dt):
        self.notifications = [n for n in self.notifications if n.update(dt)]
        self.particles = [p for p in self.particles if p.update(dt)]

        if self.ore_cooldown > 0:
            self.ore_cooldown = max(0.0, self.ore_cooldown - dt)

        self._ambient_timer += dt
        if self._ambient_timer > 0.3:
            self._ambient_timer = 0.0
            self.particles.append(
                Particle(
                    random.randint(100, SCREEN_WIDTH - 100),
                    random.randint(100, 380),
                    random.uniform(-5, 5),
                    random.uniform(-20, -8),
                    (255, 215, 100),
                    random.uniform(1.5, 3.0),
                    random.uniform(1, 2),
                )
            )

    # ── render ───────────────────────────────────────────────────
    def _render(self):
        self.renderer.draw_frame(
            shop_display=self.shop.display,
            gold=self.gold,
            inventory=self.inventory,
            total_spent=self.total_spent,
            max_inventory=self.max_inventory,
            hovered_shop=self.hovered_shop,
            hovered_inv=self.hovered_inv,
            hover_refresh=self.hover_refresh,
            hover_ore=self.hover_ore,
            mouse_pos=self.mouse_pos,
            notifications=self.notifications,
            particles=self.particles,
            pool_remaining=self.shop.pool_size(),
            ore_charges=self.ore_charges,
            ore_cooldown=self.ore_cooldown,
            targeting=self.targeting,
            muted=self.audio.muted,
        )


if __name__ == "__main__":
    asyncio.run(Game().run())
