"""Game entities: player, NPCs, infected, animals, bullets."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum, auto

import pygame

from game.settings import (
  BULLET_LIFETIME,
  MAX_ANIMALS,
  MAX_INFECTED,
  MAX_NPCS,
  MELEE_RANGE,
  PLAYER_MAX_HEALTH,
  PLAYER_MAX_STAMINA,
  PLAYER_SPEED,
  SPAWN_RADIUS,
  TILE_SIZE,
)
from game.sprites import (
  make_animal_sprite,
  make_bullet_sprite,
  make_infected_sprite,
  make_player_sprite,
  make_survivor_sprite,
)
from game.weapons import STARTER_WEAPONS, WEAPONS, WeaponSpec, get_weapon


class Faction(Enum):
  PLAYER = auto()
  SURVIVOR = auto()
  RAIDER = auto()
  MILITIA = auto()
  SCIENTIST = auto()
  TRADER = auto()
  INFECTED = auto()
  ANIMAL = auto()


class NPCRole(Enum):
  CIVILIAN = "平民幸存者"
  DOCTOR = "医生"
  SOLDIER = "士兵"
  SCAVENGER = "拾荒者"
  CHILD = "孩童"
  ELDER = "老人"
  ENGINEER = "工程师"
  HUNTER = "猎人"
  JOURNALIST = "记者"
  PRIEST = "牧师"
  RAIDER = "掠夺者"
  MILITIA = "民兵"
  SCIENTIST = "科学家"
  TRADER = "商人"
  REFUGEE = "难民"


INFECTED_TYPES = {
  "walker": {"hp": 40, "speed": 55, "damage": 8, "name": "蹒跚感染者"},
  "runner": {"hp": 25, "speed": 130, "damage": 12, "name": "狂奔感染者"},
  "brute": {"hp": 120, "speed": 40, "damage": 25, "name": "蛮力感染者"},
  "spitter": {"hp": 35, "speed": 70, "damage": 15, "name": "喷吐感染者"},
}

ANIMAL_TYPES = {
  "dog": {"hp": 30, "speed": 100, "damage": 10, "name": "感染犬"},
  "wolf": {"hp": 45, "speed": 120, "damage": 18, "name": "感染狼"},
  "rat": {"hp": 10, "speed": 80, "damage": 4, "name": "感染鼠群"},
  "bird": {"hp": 8, "speed": 150, "damage": 3, "name": "感染鸟群"},
  "bear": {"hp": 150, "speed": 70, "damage": 35, "name": "感染熊"},
}

DIALOGUES = {
  NPCRole.CIVILIAN: [
    "暴风雪又来了……我们还能撑多久？",
    "听说方舟计划早就放弃了，地表没有希望了。",
    "小心那些跑得快的东西，被咬到就完了。",
  ],
  NPCRole.DOCTOR: [
    "这种病毒在极寒中会加速变异，我在研究抗体。",
    "你需要抗生素吗？用子弹换。",
    "伤员太多了……医疗物资快用完了。",
  ],
  NPCRole.SOLDIER: [
    "军方频道已经三个月没信号了。",
    "守住这片区域，感染者晚上更活跃。",
    "我的弹药用光了，你有多余的吗？",
  ],
  NPCRole.SCIENTIST: [
    "地磁北极偏移超过40度，灾难不会结束。",
    "2012年那天，门没有关上……数据还在我脑子里。",
    "感染者的神经毒素在低温下结晶，这解释了它们的狂暴。",
  ],
  NPCRole.TRADER: [
    "子弹就是货币，朋友。",
    "我有把好枪，价格公道。",
    "以物易物，不收纸币——那玩意儿擦屁股都嫌硬。",
  ],
  NPCRole.REFUGEE: [
    "我们从沿海逃出来的，洪水一直没退。",
    "孩子……我的孩子还在废墟里……",
    "求求你，给点食物吧。",
  ],
  NPCRole.HUNTER: [
    "感染动物比感染者更危险，它们会埋伏。",
    "熊被打中要害也会倒，但你要够快。",
    "这片森林曾经是我的家。",
  ],
  NPCRole.ENGINEER: [
    "发电机快没燃料了，需要有人去电厂。",
    "我可以改装你的武器，给我零件。",
    "地下掩体还有一层，但入口被堵了。",
  ],
}


@dataclass
class Bullet:
  x: float
  y: float
  vx: float
  vy: float
  damage: float
  owner_faction: Faction
  lifetime: float = BULLET_LIFETIME
  sprite: pygame.Surface = field(default_factory=make_bullet_sprite)

  def update(self, dt: float) -> bool:
    self.x += self.vx * dt
    self.y += self.vy * dt
    self.lifetime -= dt
    return self.lifetime > 0


class WeaponState:
  def __init__(self, weapon_id: str):
    self.spec = get_weapon(weapon_id)
    self.ammo = self.spec.magazine
    self.cooldown = 0.0
    self.reloading = False
    self.reload_timer = 0.0

  def can_fire(self) -> bool:
    if self.reloading:
      return False
    if self.spec.id in ("machete", "combat_knife"):
      return self.cooldown <= 0
    return self.cooldown <= 0 and self.ammo > 0

  def fire(self) -> bool:
    if not self.can_fire():
      return False
    if self.spec.id in ("machete", "combat_knife"):
      self.cooldown = 1.0 / self.spec.fire_rate
      return True
    self.ammo -= 1
    self.cooldown = 1.0 / self.spec.fire_rate
    if self.ammo <= 0 and self.spec.magazine < 999:
      self.start_reload()
    return True

  def start_reload(self):
    if self.spec.magazine >= 999:
      return
    self.reloading = True
    self.reload_timer = self.spec.reload_time

  def update(self, dt: float):
    if self.cooldown > 0:
      self.cooldown -= dt
    if self.reloading:
      self.reload_timer -= dt
      if self.reload_timer <= 0:
        self.ammo = self.spec.magazine
        self.reloading = False


class Entity:
  def __init__(self, x: float, y: float, faction: Faction):
    self.x = x
    self.y = y
    self.faction = faction
    self.health = 100.0
    self.max_health = 100.0
    self.speed = 80.0
    self.alive = True
    self.angle = 0.0
    self.sprite: pygame.Surface | None = None
    self.radius = 14
    self.damage_flash = 0.0
    self.name = "Entity"

  def take_damage(self, amount: float):
    self.health -= amount
    self.damage_flash = 0.15
    if self.health <= 0:
      self.alive = False

  def distance_to(self, other) -> float:
    return math.hypot(self.x - other.x, self.y - other.y)

  def update(self, dt: float, world, player):
    if self.damage_flash > 0:
      self.damage_flash -= dt


class Player(Entity):
  def __init__(self, x: float, y: float):
    super().__init__(x, y, Faction.PLAYER)
    self.health = PLAYER_MAX_HEALTH
    self.max_health = PLAYER_MAX_HEALTH
    self.stamina = PLAYER_MAX_STAMINA
    self.sprite = make_player_sprite()
    self.radius = 14
    self.name = "幸存者"
    self.weapons: list[WeaponState] = [WeaponState(w) for w in STARTER_WEAPONS]
    self.weapon_index = 0
    self.inventory: list[str] = []
    self.kills = 0
    self.day = 1
    self.experience = 0

  @property
  def current_weapon(self) -> WeaponState:
    return self.weapons[self.weapon_index]

  def add_weapon(self, weapon_id: str):
    if weapon_id in WEAPONS and not any(w.spec.id == weapon_id for w in self.weapons):
      self.weapons.append(WeaponState(weapon_id))

  def switch_weapon(self, index: int):
    if 0 <= index < len(self.weapons):
      self.weapon_index = index

  def next_weapon(self):
    self.weapon_index = (self.weapon_index + 1) % len(self.weapons)

  def update(self, dt: float, world, move_dir: tuple[float, float], speed_mult: float = 1.0):
    mx, my = move_dir
    if mx or my:
      length = math.hypot(mx, my)
      mx /= length
      my /= length
      tile_mult = world.get_move_speed_mult(self.x, self.y)
      spd = PLAYER_SPEED * speed_mult * tile_mult
      nx = self.x + mx * spd * dt
      ny = self.y + my * spd * dt
      if world.is_walkable(nx, self.y):
        self.x = nx
      if world.is_walkable(self.x, ny):
        self.y = ny
      self.angle = math.atan2(my, mx)
    self.current_weapon.update(dt)
    super().update(dt, world, self)


class NPC(Entity):
  _id_counter = 0

  def __init__(self, x: float, y: float, role: NPCRole, hostile: bool = False):
    NPC._id_counter += 1
    faction = Faction.RAIDER if hostile else Faction.SURVIVOR
    super().__init__(x, y, faction)
    self.role = role
    self.hostile = hostile
    self.name = role.value
    self.npc_id = NPC._id_counter
    colors = {
      NPCRole.CIVILIAN: (100, 140, 180),
      NPCRole.DOCTOR: (200, 200, 220),
      NPCRole.SOLDIER: (80, 100, 60),
      NPCRole.SCIENTIST: (180, 160, 100),
      NPCRole.TRADER: (160, 120, 60),
      NPCRole.RAIDER: (140, 50, 50),
      NPCRole.REFUGEE: (120, 110, 100),
      NPCRole.HUNTER: (90, 70, 50),
      NPCRole.ENGINEER: (100, 100, 120),
      NPCRole.CHILD: (180, 160, 140),
      NPCRole.ELDER: (130, 120, 110),
      NPCRole.JOURNALIST: (150, 130, 90),
      NPCRole.PRIEST: (80, 80, 100),
      NPCRole.MILITIA: (70, 90, 70),
      NPCRole.SCAVENGER: (110, 100, 80),
    }
    self.sprite = make_survivor_sprite(colors.get(role, (120, 120, 130)))
    self.speed = random.uniform(40, 70)
    self.wander_timer = random.uniform(1, 4)
    self.wander_dir = (0.0, 0.0)
    self.dialogue = random.choice(DIALOGUES.get(role, ["……"]))
    self.weapon_id = random.choice(["glock17", "makarov", "mp5", "ak47", None, None])
    self.attack_cooldown = 0.0

  def update(self, dt: float, world, player: Player):
    if not self.alive:
      return
    super().update(dt, world, player)
    dist = self.distance_to(player)

    if self.hostile and dist < 350:
      dx = player.x - self.x
      dy = player.y - self.y
      length = math.hypot(dx, dy) or 1
      self.x += dx / length * self.speed * 1.2 * dt
      self.y += dy / length * self.speed * 1.2 * dt
      self.angle = math.atan2(dy, dx)
    else:
      self.wander_timer -= dt
      if self.wander_timer <= 0:
        self.wander_timer = random.uniform(2, 5)
        angle = random.uniform(0, math.pi * 2)
        self.wander_dir = (math.cos(angle), math.sin(angle))
      wx, wy = self.wander_dir
      nx = self.x + wx * self.speed * dt
      ny = self.y + wy * self.speed * dt
      if world.is_walkable(nx, ny):
        self.x = nx
        self.y = ny

    if self.attack_cooldown > 0:
      self.attack_cooldown -= dt


class Infected(Entity):
  def __init__(self, x: float, y: float, variant: str = "walker"):
    super().__init__(x, y, Faction.INFECTED)
    self.variant = variant
    stats = INFECTED_TYPES[variant]
    self.max_health = stats["hp"]
    self.health = stats["hp"]
    self.speed = stats["speed"]
    self.damage = stats["damage"]
    self.name = stats["name"]
    self.sprite = make_infected_sprite(variant)
    self.attack_cooldown = 0.0
    self.radius = 16 if variant == "brute" else 13

  def update(self, dt: float, world, player: Player):
    if not self.alive:
      return
    super().update(dt, world, player)
    dist = self.distance_to(player)
    aggro_range = 400 if self.variant == "runner" else 280

    if dist < aggro_range:
      dx = player.x - self.x
      dy = player.y - self.y
      length = math.hypot(dx, dy) or 1
      self.x += dx / length * self.speed * dt
      self.y += dy / length * self.speed * dt
      self.angle = math.atan2(dy, dx)

      if dist < 22 and self.attack_cooldown <= 0:
        player.take_damage(self.damage)
        self.attack_cooldown = 0.8

    if self.attack_cooldown > 0:
      self.attack_cooldown -= dt


class InfectedAnimal(Entity):
  def __init__(self, x: float, y: float, animal_type: str):
    super().__init__(x, y, Faction.ANIMAL)
    self.animal_type = animal_type
    stats = ANIMAL_TYPES[animal_type]
    self.max_health = stats["hp"]
    self.health = stats["hp"]
    self.speed = stats["speed"]
    self.damage = stats["damage"]
    self.name = stats["name"]
    self.sprite = make_animal_sprite(animal_type, infected=True)
    self.attack_cooldown = 0.0
    self.radius = 18 if animal_type == "bear" else 11

  def update(self, dt: float, world, player: Player):
    if not self.alive:
      return
    super().update(dt, world, player)
    dist = self.distance_to(player)
    if dist < 320:
      dx = player.x - self.x
      dy = player.y - self.y
      length = math.hypot(dx, dy) or 1
      mult = 1.3 if self.animal_type in ("wolf", "bear") else 1.0
      self.x += dx / length * self.speed * mult * dt
      self.y += dy / length * self.speed * mult * dt
      self.angle = math.atan2(dy, dx)
      if dist < 20 and self.attack_cooldown <= 0:
        player.take_damage(self.damage)
        self.attack_cooldown = 0.7
    if self.attack_cooldown > 0:
      self.attack_cooldown -= dt


def spawn_entities(world, player: Player, npcs: list, infected: list, animals: list):
  """Maintain entity population around player."""
  px, py = player.x, player.y

  while len(npcs) < MAX_NPCS:
    x, y = world.find_spawn_point(px, py)
    if math.hypot(x - px, y - py) > 200:
      role = random.choice(list(NPCRole))
      hostile = role in (NPCRole.RAIDER,) or (random.random() < 0.08 and role == NPCRole.SCAVENGER)
      npcs.append(NPC(x, y, role, hostile))

  while len(infected) < MAX_INFECTED:
    x, y = world.find_spawn_point(px, py)
    if 150 < math.hypot(x - px, y - py) < SPAWN_RADIUS:
      variant = random.choices(
        ["walker", "runner", "brute", "spitter"],
        weights=[50, 25, 10, 15],
      )[0]
      infected.append(Infected(x, y, variant))

  while len(animals) < MAX_ANIMALS:
    x, y = world.find_spawn_point(px, py)
    if 100 < math.hypot(x - px, y - py) < SPAWN_RADIUS:
      atype = random.choices(
        ["dog", "wolf", "rat", "bird", "bear"],
        weights=[30, 20, 25, 15, 10],
      )[0]
      animals.append(InfectedAnimal(x, y, atype))

  # Cull far entities
  for lst in (npcs, infected, animals):
    for e in lst[:]:
      if not e.alive or math.hypot(e.x - px, e.y - py) > SPAWN_RADIUS + 200:
        lst.remove(e)


def fire_weapon(player: Player, target_x: float, target_y: float) -> list[Bullet]:
  ws = player.current_weapon
  spec = ws.spec
  if not ws.fire():
    return []

  bullets = []
  dx = target_x - player.x
  dy = target_y - player.y
  base_angle = math.atan2(dy, dx)

  if spec.id in ("machete", "combat_knife"):
    return []  # melee handled separately

  for _ in range(spec.pellets):
    spread = random.uniform(-spec.spread, spec.spread)
    angle = base_angle + spread
    speed = spec.bullet_speed
    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed
    color = (255, 200, 80)
    if spec.category.name == "SNIPER":
      color = (255, 100, 100)
    elif spec.category.name == "SHOTGUN":
      color = (255, 180, 60)
    b = Bullet(player.x, player.y, vx, vy, spec.damage, Faction.PLAYER)
    b.sprite = make_bullet_sprite(color)
    bullets.append(b)

  return bullets


def melee_attack(player: Player, entities: list) -> int:
  ws = player.current_weapon
  if ws.spec.id not in ("machete", "combat_knife"):
    return 0
  if not ws.fire():
    return 0
  hits = 0
  for e in entities:
    if e.faction == Faction.PLAYER or not e.alive:
      continue
    if player.distance_to(e) < MELEE_RANGE:
      e.take_damage(ws.spec.damage)
      hits += 1
  return hits
