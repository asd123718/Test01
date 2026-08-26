"""Ongoing disaster system - inspired by The Day After Tomorrow & 2012."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum, auto

import pygame

from game.settings import (
    COLOR_ASH,
    COLOR_COLD,
    COLOR_DANGER,
    DISASTER_COOLDOWN,
    DISASTER_MAX_DURATION,
    DISASTER_MIN_DURATION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class DisasterType(Enum):
    BLIZZARD = auto()
    EARTHQUAKE = auto()
    FLOOD = auto()
    VOLCANIC_ASH = auto()
    EXTREME_COLD = auto()
    METEOR_SHOWER = auto()
    TOXIC_FOG = auto()
    SOLAR_FLARE = auto()


@dataclass
class DisasterInfo:
    type: DisasterType
    name_cn: str
    name_en: str
    description: str
    damage_per_sec: float
    visibility: float  # 0-1
    move_penalty: float  # multiplier


DISASTER_CATALOG: dict[DisasterType, DisasterInfo] = {
    DisasterType.BLIZZARD: DisasterInfo(
        DisasterType.BLIZZARD, "超级暴风雪", "Super Blizzard",
        "《后天》式的极寒风暴席卷全球，能见度骤降，体温持续流失。", 2.0, 0.35, 0.7,
    ),
    DisasterType.EARTHQUAKE: DisasterInfo(
        DisasterType.EARTHQUAKE, "连环地震", "Chain Earthquakes",
        "《2012》的地壳撕裂从未停止，大地持续震颤。", 3.0, 0.8, 0.85,
    ),
    DisasterType.FLOOD: DisasterInfo(
        DisasterType.FLOOD, "无尽洪涝", "Endless Flooding",
        "海平面上升与冰川融化使洪水永不停歇。", 4.0, 0.6, 0.6,
    ),
    DisasterType.VOLCANIC_ASH: DisasterInfo(
        DisasterType.VOLCANIC_ASH, "火山灰幕", "Volcanic Ash Cloud",
        "超级火山持续喷发，天空被灰烬遮蔽，呼吸变得困难。", 1.5, 0.45, 0.8,
    ),
    DisasterType.EXTREME_COLD: DisasterInfo(
        DisasterType.EXTREME_COLD, "极寒冻结", "Extreme Freeze",
        "温度跌破临界点，暴露在外将迅速失温。", 3.5, 0.7, 0.75,
    ),
    DisasterType.METEOR_SHOWER: DisasterInfo(
        DisasterType.METEOR_SHOWER, "陨石雨", "Meteor Shower",
        "地磁紊乱导致近地轨道碎片不断坠落。", 5.0, 0.75, 0.9,
    ),
    DisasterType.TOXIC_FOG: DisasterInfo(
        DisasterType.TOXIC_FOG, "剧毒迷雾", "Toxic Fog",
        "工业残骸与生化泄漏形成的毒雾在废墟中蔓延。", 2.5, 0.4, 0.7,
    ),
    DisasterType.SOLAR_FLARE: DisasterInfo(
        DisasterType.SOLAR_FLARE, "太阳风暴", "Solar Storm",
        "太阳耀斑持续轰击，电磁设备失灵，辐射增强。", 1.0, 0.85, 0.95,
    ),
}


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: tuple
    size: float


@dataclass
class Meteor:
    x: float
    y: float
    target_x: float
    target_y: float
    speed: float
    damage_radius: float


class DisasterManager:
    def __init__(self):
        self.active: DisasterType | None = None
        self.timer = 0.0
        self.cooldown = 3.0
        self.duration = 30.0
        self.shake = 0.0
        self.particles: list[Particle] = []
        self.meteors: list[Meteor] = []
        self.story_index = 0
        self.story_lines = [
            "【广播杂音】……全球气候崩溃已进入第847天……没有春天了……",
            "【求救信号】方舟计划失败了……地表不适合人类……重复……",
            "【军方频道】所有单位注意：极寒风暴前锋将于六小时内抵达……",
            "【科学家录音】地磁北极偏移超过40度……灾难不会结束……",
            "【幸存者日记】它们不再是动物了……感染在寒冷中变异得更快……",
            "【联合国残骸】……海平面上升37米……大陆架持续下沉……",
            "【神秘电台】2012年那天……门没有关上……",
            "【气象站】暴风雪强度突破历史极值……后天永远不会到来……",
        ]

    def update(self, dt: float, player_pos: tuple[float, float], world_bounds: tuple):
        self.timer += dt
        if self.active is None:
            self.cooldown -= dt
            if self.cooldown <= 0:
                self._start_random_disaster()
        else:
            self.duration -= dt
            if self.duration <= 0:
                self._end_disaster()
            else:
                self._update_active(dt, player_pos, world_bounds)

        for p in self.particles[:]:
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.life -= dt
            if p.life <= 0:
                self.particles.remove(p)

        for m in self.meteors[:]:
            dx = m.target_x - m.x
            dy = m.target_y - m.y
            dist = math.hypot(dx, dy)
            if dist < 8:
                self.meteors.remove(m)
                self.shake = max(self.shake, 8.0)
            else:
                m.x += dx / dist * m.speed * dt
                m.y += dy / dist * m.speed * dt

        if self.shake > 0:
            self.shake = max(0, self.shake - dt * 12)

    def _start_random_disaster(self):
        self.active = random.choice(list(DisasterType))
        self.duration = random.uniform(DISASTER_MIN_DURATION, DISASTER_MAX_DURATION)
        self.cooldown = DISASTER_COOLDOWN
        self.story_index = (self.story_index + 1) % len(self.story_lines)

    def _end_disaster(self):
        self.active = None
        self.cooldown = DISASTER_COOLDOWN
        self.particles.clear()
        self.meteors.clear()

    def _update_active(self, dt: float, player_pos: tuple[float, float], world_bounds: tuple):
        if self.active == DisasterType.BLIZZARD:
            for _ in range(3):
                self.particles.append(Particle(
                    random.uniform(0, SCREEN_WIDTH), -10,
                    random.uniform(-30, 30), random.uniform(80, 200),
                    random.uniform(2, 5), COLOR_COLD, random.uniform(2, 5),
                ))
        elif self.active == DisasterType.EARTHQUAKE:
            self.shake = max(self.shake, random.uniform(2, 6))
        elif self.active == DisasterType.VOLCANIC_ASH:
            for _ in range(2):
                self.particles.append(Particle(
                    random.uniform(0, SCREEN_WIDTH), -5,
                    random.uniform(-20, 20), random.uniform(40, 100),
                    random.uniform(3, 8), COLOR_ASH, random.uniform(1, 4),
                ))
        elif self.active == DisasterType.METEOR_SHOWER:
            if random.random() < 0.08:
                px, py = player_pos
                tx = px + random.uniform(-400, 400)
                ty = py + random.uniform(-400, 400)
                self.meteors.append(Meteor(
                    tx + random.uniform(-200, 200), ty - 500,
                    tx, ty, random.uniform(400, 700), 60,
                ))
        elif self.active == DisasterType.TOXIC_FOG:
            for _ in range(2):
                self.particles.append(Particle(
                    random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT),
                    random.uniform(-10, 10), random.uniform(-10, 10),
                    random.uniform(4, 10), (60, 120, 60, 120), random.uniform(8, 20),
                ))
        elif self.active == DisasterType.FLOOD:
            pass  # handled via tile overlay

    def get_damage(self) -> float:
        if self.active is None:
            return 0.0
        return DISASTER_CATALOG[self.active].damage_per_sec

    def get_move_multiplier(self) -> float:
        if self.active is None:
            return 1.0
        return DISASTER_CATALOG[self.active].move_penalty

    def get_visibility(self) -> float:
        if self.active is None:
            return 1.0
        return DISASTER_CATALOG[self.active].visibility

    def get_current_story(self) -> str:
        return self.story_lines[self.story_index]

    def get_status_text(self) -> str:
        if self.active is None:
            return "灾难间歇期 - 抓紧时间搜刮资源"
        info = DISASTER_CATALOG[self.active]
        return f"⚠ {info.name_cn} | 剩余 {int(self.duration)}秒"

    def draw_overlay(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        if self.active is None:
            return
        info = DISASTER_CATALOG[self.active]
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        if self.active == DisasterType.BLIZZARD:
            overlay.fill((180, 210, 255, int(80 * (1 - info.visibility))))
        elif self.active == DisasterType.FLOOD:
            overlay.fill((30, 60, 120, 60))
        elif self.active == DisasterType.VOLCANIC_ASH:
            overlay.fill((80, 80, 85, 100))
        elif self.active == DisasterType.EXTREME_COLD:
            overlay.fill((150, 200, 255, 70))
        elif self.active == DisasterType.TOXIC_FOG:
            overlay.fill((40, 100, 40, 90))
        elif self.active == DisasterType.SOLAR_FLARE:
            overlay.fill((255, 200, 100, 40))
        screen.blit(overlay, (0, 0))

        cam_x, cam_y = camera_offset
        for p in self.particles:
            sx = int(p.x - cam_x * 0.1)
            sy = int(p.y - cam_y * 0.1)
            if 0 <= sx < SCREEN_WIDTH and 0 <= sy < SCREEN_HEIGHT:
                c = p.color[:3] if len(p.color) >= 3 else p.color
                pygame.draw.circle(screen, c, (sx, sy), int(p.size))

        for m in self.meteors:
            sx = int(m.x - cam_x)
            sy = int(m.y - cam_y)
            pygame.draw.circle(screen, (255, 120, 40), (sx, sy), 6)
            pygame.draw.line(screen, (255, 200, 100), (sx, sy), (sx, sy - 20), 3)

    def check_meteor_hit(self, x: float, y: float) -> float:
        for m in self.meteors:
            if math.hypot(x - m.target_x, y - m.target_y) < m.damage_radius:
                return 25.0
        return 0.0

    def get_shake_offset(self) -> tuple[int, int]:
        if self.shake <= 0:
            return 0, 0
        import random as r
        return int(r.uniform(-self.shake, self.shake)), int(r.uniform(-self.shake, self.shake))
