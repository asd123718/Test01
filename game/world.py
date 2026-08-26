"""World map generation and tile management."""

from __future__ import annotations

import random

from game.settings import TILE_SIZE, WORLD_HEIGHT, WORLD_WIDTH
from game.sprites import make_tile_surface


TILE_TYPES = ["grass", "snow", "road", "water", "ruin", "building", "forest", "ash", "ice"]


class World:
  def __init__(self, seed: int | None = None):
    self.seed = seed or random.randint(0, 999999)
    self.rng = random.Random(self.seed)
    self.width = WORLD_WIDTH
    self.height = WORLD_HEIGHT
    self.tiles: list[list[str]] = []
    self.tile_surfaces: dict[str, object] = {}
    self._generate()

  def _generate(self):
    # Base terrain - post-apocalyptic frozen world
    noise = [[self.rng.random() for _ in range(self.width)] for _ in range(self.height)]

  # Smooth noise
    for _ in range(3):
      for y in range(1, self.height - 1):
        for x in range(1, self.width - 1):
          avg = sum(
            noise[y + dy][x + dx]
            for dy in (-1, 0, 1) for dx in (-1, 0, 1)
          ) / 9
          noise[y][x] = avg * 0.6 + noise[y][x] * 0.4

    self.tiles = []
    for y in range(self.height):
      row = []
      for x in range(self.width):
        v = noise[y][x]
        if v < 0.15:
          t = "water"
        elif v < 0.25:
          t = "ice"
        elif v < 0.35:
          t = "snow"
        elif v < 0.45:
          t = "forest"
        elif v < 0.55:
          t = "grass"
        elif v < 0.65:
          t = "ruin"
        elif v < 0.75:
          t = "road"
        elif v < 0.85:
          t = "building"
        else:
          t = "ash"
        row.append(t)
      self.tiles.append(row)

    # Add city clusters
    for _ in range(8):
      cx = self.rng.randint(10, self.width - 10)
      cy = self.rng.randint(10, self.height - 10)
      for dy in range(-4, 5):
        for dx in range(-4, 5):
          tx, ty = cx + dx, cy + dy
          if 0 <= tx < self.width and 0 <= ty < self.height:
            if self.rng.random() < 0.7:
              self.tiles[ty][tx] = self.rng.choice(["building", "ruin", "road"])

    # Refuge zones (safer grass patches)
    for _ in range(5):
      cx = self.rng.randint(5, self.width - 5)
      cy = self.rng.randint(5, self.height - 5)
      for dy in range(-3, 4):
        for dx in range(-3, 4):
          tx, ty = cx + dx, cy + dy
          if 0 <= tx < self.width and 0 <= ty < self.height:
            self.tiles[ty][tx] = "grass"

    for t in TILE_TYPES:
      self.tile_surfaces[t] = make_tile_surface(t, TILE_SIZE)

  def get_tile(self, tx: int, ty: int) -> str:
    if 0 <= tx < self.width and 0 <= ty < self.height:
      return self.tiles[ty][tx]
    return "snow"

  def is_walkable(self, wx: float, wy: float) -> bool:
    tx = int(wx // TILE_SIZE)
    ty = int(wy // TILE_SIZE)
    t = self.get_tile(tx, ty)
    return t not in ("water", "building")

  def get_move_speed_mult(self, wx: float, wy: float) -> float:
    tx = int(wx // TILE_SIZE)
    ty = int(wy // TILE_SIZE)
    t = self.get_tile(tx, ty)
    return {
      "snow": 0.75, "ice": 0.6, "forest": 0.7, "ruin": 0.85,
      "ash": 0.8, "water": 0.3, "road": 1.1, "grass": 1.0,
      "building": 0.0,
    }.get(t, 1.0)

  def draw(self, screen, camera_x: float, camera_y: float, screen_w: int, screen_h: int):
    start_tx = max(0, int(camera_x // TILE_SIZE) - 1)
    start_ty = max(0, int(camera_y // TILE_SIZE) - 1)
    end_tx = min(self.width, start_tx + screen_w // TILE_SIZE + 3)
    end_ty = min(self.height, start_ty + screen_h // TILE_SIZE + 3)

    for ty in range(start_ty, end_ty):
      for tx in range(start_tx, end_tx):
        t = self.tiles[ty][tx]
        surf = self.tile_surfaces.get(t)
        if surf:
          sx = int(tx * TILE_SIZE - camera_x)
          sy = int(ty * TILE_SIZE - camera_y)
          screen.blit(surf, (sx, sy))

  def find_spawn_point(self, near_x: float | None = None, near_y: float | None = None) -> tuple[float, float]:
    for _ in range(200):
      if near_x is not None:
        tx = int(near_x // TILE_SIZE) + self.rng.randint(-15, 15)
        ty = int(near_y // TILE_SIZE) + self.rng.randint(-15, 15)
      else:
        tx = self.rng.randint(5, self.width - 5)
        ty = self.rng.randint(5, self.height - 5)
      if self.is_walkable(tx * TILE_SIZE, ty * TILE_SIZE):
        return tx * TILE_SIZE + TILE_SIZE // 2, ty * TILE_SIZE + TILE_SIZE // 2
    return self.width * TILE_SIZE // 2, self.height * TILE_SIZE // 2
