"""Procedural sprite generation - no external assets required."""

from __future__ import annotations

import math
import random

import pygame


def _circle_surf(size: int, color: tuple, outline: tuple | None = None) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r = size // 2
    if outline:
        pygame.draw.circle(surf, outline, (r, r), r)
    pygame.draw.circle(surf, color, (r, r), r - (2 if outline else 0))
    return surf


def make_player_sprite(size: int = 28) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    pygame.draw.circle(surf, (40, 90, 160), (cx, cy), size // 2 - 2)
    pygame.draw.circle(surf, (220, 190, 160), (cx, cy - 4), 7)
    pygame.draw.rect(surf, (50, 55, 65), (cx - 8, cy, 16, 12), border_radius=3)
    pygame.draw.line(surf, (180, 180, 190), (cx + 6, cy + 2), (cx + 14, cy - 2), 3)
    return surf


def make_survivor_sprite(color: tuple, size: int = 24) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    pygame.draw.circle(surf, color, (cx, cy), size // 2 - 1)
    pygame.draw.circle(surf, (210, 180, 150), (cx, cy - 3), 5)
    return surf


def make_infected_sprite(variant: str, size: int = 26) -> pygame.Surface:
    colors = {
        "walker": ((80, 120, 60), (60, 90, 40)),
        "runner": ((120, 60, 60), (90, 40, 40)),
        "brute": ((70, 70, 80), (50, 50, 55)),
        "spitter": ((90, 100, 50), (70, 80, 35)),
    }
    body, dark = colors.get(variant, colors["walker"])
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    pygame.draw.circle(surf, body, (cx, cy), size // 2 - 1)
    pygame.draw.circle(surf, dark, (cx - 4, cy - 2), 3)
    pygame.draw.circle(surf, dark, (cx + 4, cy - 2), 3)
    pygame.draw.circle(surf, (200, 30, 30), (cx, cy - 5), 4)
    if variant == "brute":
        pygame.draw.circle(surf, dark, (cx, cy), size // 2 + 2, 2)
    return surf


def make_animal_sprite(animal_type: str, infected: bool, size: int = 22) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    if animal_type == "dog":
        color = (140, 90, 50) if not infected else (100, 70, 45)
        pygame.draw.ellipse(surf, color, (2, 6, size - 4, size - 10))
        pygame.draw.circle(surf, color, (size - 6, 8), 6)
    elif animal_type == "wolf":
        color = (100, 100, 110) if not infected else (80, 70, 75)
        pygame.draw.ellipse(surf, color, (0, 8, size, size - 12))
        pygame.draw.polygon(surf, color, [(size - 4, 6), (size + 2, 10), (size - 2, 14)])
    elif animal_type == "rat":
        color = (90, 80, 70) if not infected else (70, 60, 55)
        pygame.draw.ellipse(surf, color, (4, 10, size - 8, size - 14))
        pygame.draw.line(surf, color, (4, 12), (0, 10), 2)
    elif animal_type == "bird":
        color = (60, 70, 90) if not infected else (50, 55, 65)
        pygame.draw.polygon(surf, color, [(cx, 4), (size - 2, cy), (cx, size - 4), (2, cy)])
    elif animal_type == "bear":
        color = (80, 60, 40) if not infected else (60, 45, 35)
        pygame.draw.circle(surf, color, (cx, cy), size // 2 - 1)
        pygame.draw.circle(surf, color, (cx - 8, cy - 8), 5)
        pygame.draw.circle(surf, color, (cx + 8, cy - 8), 5)
    else:
        pygame.draw.circle(surf, (120, 120, 100), (cx, cy), size // 2 - 2)

    if infected:
        pygame.draw.circle(surf, (200, 40, 40), (cx + 4, cy - 2), 2)
    return surf


def make_bullet_sprite(color: tuple = (255, 220, 80)) -> pygame.Surface:
    return _circle_surf(6, color, (200, 160, 40))


def make_tile_surface(tile_type: str, size: int = 32) -> pygame.Surface:
    surf = pygame.Surface((size, size))
    palettes = {
        "grass": ((45, 75, 45), (55, 90, 50), (40, 65, 40)),
        "snow": ((220, 230, 240), (200, 215, 230), (235, 240, 250)),
        "road": ((55, 55, 60), (65, 65, 70), (50, 50, 55)),
        "water": ((30, 60, 100), (40, 75, 120), (25, 50, 90)),
        "ruin": ((70, 65, 60), (85, 75, 65), (60, 55, 50)),
        "building": ((80, 85, 95), (95, 100, 110), (70, 75, 85)),
        "forest": ((30, 55, 30), (40, 70, 35), (25, 45, 25)),
        "ash": ((70, 70, 75), (80, 80, 85), (60, 60, 65)),
        "lava": ((180, 60, 20), (220, 100, 30), (140, 40, 10)),
        "ice": ((160, 200, 230), (180, 215, 245), (140, 185, 220)),
    }
    c1, c2, c3 = palettes.get(tile_type, palettes["grass"])
    for y in range(size):
        for x in range(size):
            noise = random.Random(x * 997 + y * 131).random()
            if noise < 0.33:
                surf.set_at((x, y), c1)
            elif noise < 0.66:
                surf.set_at((x, y), c2)
            else:
                surf.set_at((x, y), c3)
    if tile_type == "building":
        pygame.draw.rect(surf, (50, 55, 65), (4, 4, size - 8, size - 8), 2)
        pygame.draw.rect(surf, (120, 140, 180), (10, 12, 8, 10))
    elif tile_type == "ruin":
        pygame.draw.line(surf, (40, 38, 35), (0, size // 2), (size, size // 3), 2)
    elif tile_type == "forest":
        pygame.draw.circle(surf, (20, 40, 20), (size // 2, size // 2), 8)
    return surf


def make_particle(color: tuple, size: int = 4) -> pygame.Surface:
    return _circle_surf(size, color)


def draw_gun_icon(screen: pygame.Surface, weapon_id: str, x: int, y: int, selected: bool):
    from game.weapons import WEAPONS, WeaponCategory

    spec = WEAPONS.get(weapon_id)
    if not spec:
        return
    cat_colors = {
        WeaponCategory.PISTOL: (180, 180, 190),
        WeaponCategory.SMG: (160, 180, 200),
        WeaponCategory.RIFLE: (140, 170, 140),
        WeaponCategory.SHOTGUN: (200, 160, 100),
        WeaponCategory.SNIPER: (200, 140, 140),
        WeaponCategory.LMG: (180, 140, 200),
        WeaponCategory.SPECIAL: (220, 180, 80),
    }
    color = cat_colors.get(spec.category, (180, 180, 180))
    if selected:
        pygame.draw.rect(screen, (255, 140, 60), (x - 2, y - 2, 54, 22), 2, border_radius=4)
    pygame.draw.rect(screen, color, (x, y + 8, 30, 6), border_radius=2)
    pygame.draw.rect(screen, color, (x + 28, y + 6, 18, 4), border_radius=1)
    font = pygame.font.SysFont("arial", 10)
    label = font.render(spec.name_cn[:6], True, (220, 220, 230))
    screen.blit(label, (x, y))
