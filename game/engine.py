"""Main game engine."""

from __future__ import annotations

import math
import random

import pygame

from game.disasters import DisasterManager
from game.entities import (
  Bullet,
  Faction,
  Infected,
  InfectedAnimal,
  NPC,
  NPCRole,
  Player,
  fire_weapon,
  melee_attack,
  spawn_entities,
)
from game.settings import (
  COLOR_BG,
  FPS,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
  TILE_SIZE,
  TITLE,
  WORLD_HEIGHT,
  WORLD_WIDTH,
)
from game.ui import UI
from game.weapons import WEAPON_LIST, WEAPONS
from game.world import World


class GameState:
  TITLE = "title"
  PLAYING = "playing"
  PAUSED = "paused"
  GAME_OVER = "game_over"


class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption(TITLE)
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.state = GameState.TITLE
    self.ui = UI()
    self.reset()

  def reset(self):
    self.world = World()
    sx, sy = self.world.find_spawn_point()
    self.player = Player(sx, sy)
    self.npcs: list[NPC] = []
    self.infected: list[Infected] = []
    self.animals: list[InfectedAnimal] = []
    self.bullets: list[Bullet] = []
    self.disasters = DisasterManager()
    self.camera_x = 0.0
    self.camera_y = 0.0
    self.day_timer = 0.0
    self.fire_held = False
    self.show_minimap = False
    self.pickup_cooldown = 0.0
    self.interact_cooldown = 0.0
    self._give_starter_loot()

  def _give_starter_loot(self):
    # Give player access to more weapons over time - start with extras nearby
    bonus = random.sample(
      [w for w in WEAPON_LIST if w not in [ws.spec.id for ws in self.player.weapons]],
      min(15, len(WEAPON_LIST) - len(self.player.weapons)),
    )
    for wid in bonus:
      self.player.add_weapon(wid)

  def run(self):
    running = True
    while running:
      dt = self.clock.tick(FPS) / 1000.0
      dt = min(dt, 0.05)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        self._handle_event(event)

      if self.state == GameState.TITLE:
        self.ui.draw_title_screen(self.screen)
      elif self.state == GameState.PLAYING:
        self._update(dt)
        self._draw()
      elif self.state == GameState.PAUSED:
        self._draw()
        self.ui.draw_pause(self.screen)
      elif self.state == GameState.GAME_OVER:
        self._draw()
        self.ui.draw_game_over(self.screen, self.player)

      pygame.display.flip()

    pygame.quit()

  def _handle_event(self, event):
    if event.type == pygame.KEYDOWN:
      if self.state == GameState.TITLE:
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
          self.state = GameState.PLAYING
          self.ui.show_dialogue(self.disasters.get_current_story(), 6.0)
      elif self.state == GameState.GAME_OVER:
        if event.key == pygame.K_RETURN:
          self.reset()
          self.state = GameState.PLAYING
      elif self.state == GameState.PLAYING:
        if event.key == pygame.K_ESCAPE:
          self.state = GameState.PAUSED
        elif event.key == pygame.K_r:
          self.player.current_weapon.start_reload()
        elif event.key == pygame.K_e:
          self._interact_npc()
        elif event.key == pygame.K_q:
          self._pickup_weapon()
        elif event.key == pygame.K_m:
          self.show_minimap = not self.show_minimap
        elif event.key == pygame.K_h:
          self.ui.show_help = not self.ui.show_help
        elif event.key == pygame.K_TAB:
          self.ui.show_weapon_wheel = True
        elif pygame.K_1 <= event.key <= pygame.K_9:
          self.player.switch_weapon(event.key - pygame.K_1)
      elif self.state == GameState.PAUSED:
        if event.key == pygame.K_ESCAPE:
          self.state = GameState.PLAYING
        elif event.key == pygame.K_q:
          self.state = GameState.TITLE

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_TAB:
        self.ui.show_weapon_wheel = False

    if event.type == pygame.MOUSEBUTTONDOWN and self.state == GameState.TITLE:
      self.state = GameState.PLAYING
      self.ui.show_dialogue(self.disasters.get_current_story(), 6.0)

    if event.type == pygame.MOUSEBUTTONDOWN and self.ui.show_weapon_wheel:
      self._weapon_wheel_click(event.pos)

  def _weapon_wheel_click(self, pos):
    cols = 6
    for i, ws in enumerate(self.player.weapons):
      col = i % cols
      row = i // cols
      x = 80 + col * 190
      y = 100 + row * 70
      if x <= pos[0] <= x + 180 and y <= pos[1] <= y + 60:
        self.player.switch_weapon(i)
        break

  def _interact_npc(self):
    if self.interact_cooldown > 0:
      return
    nearest = None
    best_dist = 80
    for npc in self.npcs:
      if not npc.alive:
        continue
      d = self.player.distance_to(npc)
      if d < best_dist:
        best_dist = d
        nearest = npc
    if nearest:
      self.ui.show_dialogue(f"[{nearest.name}] {nearest.dialogue}", 5.0)
      self.interact_cooldown = 1.0
      if nearest.hostile:
        self.ui.show_message("警告：此人是敌对单位！", 2.0)

  def _pickup_weapon(self):
    if self.pickup_cooldown > 0:
      return
    # Random weapon drop simulation
    available = [w for w in WEAPON_LIST if w not in [ws.spec.id for ws in self.player.weapons]]
    if available:
      wid = random.choice(available)
      self.player.add_weapon(wid)
      spec = WEAPONS[wid]
      self.ui.show_message(f"获得武器: {spec.name_cn} ({spec.name})", 3.0)
    else:
      self.ui.show_message("已收集全部枪械型号！", 2.0)
    self.pickup_cooldown = 2.0

  def _update(self, dt: float):
    keys = pygame.key.get_pressed()
    move = (
      (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]),
      (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]),
    )

    disaster_mult = self.disasters.get_move_multiplier()
    self.player.update(dt, self.world, move, disaster_mult)

    # Disaster damage
    dmg = self.disasters.get_damage() * dt
    meteor_dmg = self.disasters.check_meteor_hit(self.player.x, self.player.y)
    self.player.take_damage(dmg + meteor_dmg * dt)

    if self.player.health <= 0:
      self.state = GameState.GAME_OVER
      return

    self.disasters.update(dt, (self.player.x, self.player.y), (0, 0, WORLD_WIDTH * TILE_SIZE, WORLD_HEIGHT * TILE_SIZE))

    spawn_entities(self.world, self.player, self.npcs, self.infected, self.animals)

    all_entities = self.npcs + self.infected + self.animals
    for e in all_entities:
      e.update(dt, self.world, self.player)

    # Shooting
    mouse_world_x = pygame.mouse.get_pos()[0] + self.camera_x
    mouse_world_y = pygame.mouse.get_pos()[1] + self.camera_y
    if pygame.mouse.get_pressed()[0]:
      ws = self.player.current_weapon
      if ws.spec.id in ("machete", "combat_knife"):
        hits = melee_attack(self.player, all_entities)
        if hits:
          self.player.kills += hits
      else:
        new_bullets = fire_weapon(self.player, mouse_world_x, mouse_world_y)
        self.bullets.extend(new_bullets)

    # Update bullets
    for b in self.bullets[:]:
      if not b.update(dt):
        self.bullets.remove(b)
        continue
      for e in all_entities:
        if not e.alive:
          continue
        if math.hypot(b.x - e.x, b.y - e.y) < e.radius + 4:
          e.take_damage(b.damage)
          if not e.alive:
            self.player.kills += 1
            self.player.experience += 10
          if b in self.bullets:
            self.bullets.remove(b)
          break

    # Camera follow
    self.camera_x = self.player.x - SCREEN_WIDTH // 2
    self.camera_y = self.player.y - SCREEN_HEIGHT // 2
    self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH))
    self.camera_y = max(0, min(self.camera_y, WORLD_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))

    shake = self.disasters.get_shake_offset()
    self.camera_x += shake[0]
    self.camera_y += shake[1]

    # Day cycle
    self.day_timer += dt
    if self.day_timer > 120:
      self.day_timer = 0
      self.player.day += 1
      self.ui.show_dialogue(f"第 {self.player.day} 天 — 灾难仍在继续……", 4.0)

    self.ui.update(dt)
    if self.pickup_cooldown > 0:
      self.pickup_cooldown -= dt
    if self.interact_cooldown > 0:
      self.interact_cooldown -= dt

    # Aim angle
    dx = mouse_world_x - self.player.x
    dy = mouse_world_y - self.player.y
    if dx or dy:
      self.player.angle = math.atan2(dy, dx)

  def _draw(self):
    self.screen.fill(COLOR_BG)
    self.world.draw(self.screen, self.camera_x, self.camera_y, SCREEN_WIDTH, SCREEN_HEIGHT)

    all_draw = self.npcs + self.infected + self.animals
    all_draw.sort(key=lambda e: e.y)

    for e in all_draw:
      if not e.alive:
        continue
      sx = int(e.x - self.camera_x)
      sy = int(e.y - self.camera_y)
      if -50 < sx < SCREEN_WIDTH + 50 and -50 < sy < SCREEN_HEIGHT + 50:
        if e.sprite:
          rect = e.sprite.get_rect(center=(sx, sy))
          if e.damage_flash > 0:
            flash = pygame.Surface(e.sprite.get_size(), pygame.SRCALPHA)
            flash.fill((255, 100, 100, 120))
            self.screen.blit(e.sprite, rect)
            self.screen.blit(flash, rect)
          else:
            self.screen.blit(e.sprite, rect)
        # Name tag for NPCs
        if isinstance(e, NPC) and not e.hostile:
          font = self.ui.font_small
          tag = font.render(e.name, True, (180, 190, 200))
          self.screen.blit(tag, (sx - tag.get_width() // 2, sy - 28))

    # Bullets
    for b in self.bullets:
      sx = int(b.x - self.camera_x)
      sy = int(b.y - self.camera_y)
      self.screen.blit(b.sprite, (sx - 3, sy - 3))

    # Player
    psx = int(self.player.x - self.camera_x)
    psy = int(self.player.y - self.camera_y)
    if self.player.sprite:
      rotated = pygame.transform.rotate(
        self.player.sprite,
        -math.degrees(self.player.angle) - 90,
      )
      rect = rotated.get_rect(center=(psx, psy))
      self.screen.blit(rotated, rect)

    self.disasters.draw_overlay(self.screen, (self.camera_x, self.camera_y))

    if self.show_minimap:
      self.ui.draw_minimap(self.screen, self.world, self.player, all_draw)

    fps = self.clock.get_fps()
    self.ui.draw_hud(self.screen, self.player, self.disasters.get_status_text(), fps)

    if self.ui.show_weapon_wheel:
      self.ui.draw_weapon_wheel(self.screen, self.player, pygame.mouse.get_pos())
