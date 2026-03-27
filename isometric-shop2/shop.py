"""Shop pool management — draw, buy, and refresh."""

import random
from items import Item, ITEM_TEMPLATES
from config import POOL_SIZES, SHOP_SLOTS


class Shop:
    """Maintains a finite item pool and a visible display of SHOP_SLOTS items."""

    def __init__(self):
        self.pool: list[Item] = []
        for tmpl in ITEM_TEMPLATES:
            for _ in range(POOL_SIZES[tmpl["rarity"]]):
                self.pool.append(Item(tmpl))
        random.shuffle(self.pool)

        self.display: list[Item | None] = [None] * SHOP_SLOTS
        self._fill()

    # ── public ───────────────────────────────────────────────────
    def refresh(self):
        """Return unsold items to pool and draw fresh ones."""
        for i in range(SHOP_SLOTS):
            if self.display[i] is not None:
                self.pool.append(self.display[i])
                self.display[i] = None
        random.shuffle(self.pool)
        self._fill()

    def buy(self, slot: int):
        """Remove item from display after purchase (gold handled by caller)."""
        self.display[slot] = None

    def pool_size(self) -> int:
        return len(self.pool)

    # ── private ──────────────────────────────────────────────────
    def _fill(self):
        for i in range(SHOP_SLOTS):
            if self.display[i] is None and self.pool:
                self.display[i] = self.pool.pop()
