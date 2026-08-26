"""HUD, menus, and dialogue UI."""

from __future__ import annotations

import pygame

from game.settings import (
  COLOR_ACCENT,
  COLOR_DANGER,
  COLOR_SAFE,
  COLOR_TEXT,
  COLOR_UI_BG,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
)
from game.sprites import draw_gun_icon
from game.weapons import WEAPONS


class UI:
  def __init__(self):
    self.font = pygame.font.SysFont("microsoftyahei,simhei,arial", 18)
    self.font_small = pygame.font.SysFont("microsoftyahei,simhei,arial", 14)
    self.font_large = pygame.font.SysFont("microsoftyahei,simhei,arial", 28, bold=True)
    self.font_title = pygame.font.SysFont("microsoftyahei,simhei,arial", 42, bold=True)
    self.dialogue_text = ""
    self.dialogue_timer = 0.0
    self.show_weapon_wheel = False
    self.message = ""
    self.message_timer = 0.0
    self.show_help = True

  def show_dialogue(self, text: str, duration: float = 5.0):
    self.dialogue_text = text
    self.dialogue_timer = duration

  def show_message(self, text: str, duration: float = 3.0):
    self.message = text
    self.message_timer = duration

  def update(self, dt: float):
    if self.dialogue_timer > 0:
      self.dialogue_timer -= dt
    if self.message_timer > 0:
      self.message_timer -= dt

  def draw_hud(self, screen: pygame.Surface, player, disaster_status: str, fps: float):
    # Health bar
    self._bar(screen, 20, SCREEN_HEIGHT - 50, 200, 16, player.health / player.max_health, COLOR_DANGER, "生命")
    # Stamina
    self._bar(screen, 20, SCREEN_HEIGHT - 28, 200, 12, player.stamina / 100, COLOR_SAFE, "")

    # Weapon info
    ws = player.current_weapon
    spec = ws.spec
    ammo_text = "∞" if spec.magazine >= 999 else f"{ws.ammo}/{spec.magazine}"
    reload = " [换弹中...]" if ws.reloading else ""
    wtxt = self.font.render(f"🔫 {spec.name_cn} ({spec.name}) | 弹药: {ammo_text}{reload}", True, COLOR_TEXT)
    screen.blit(wtxt, (240, SCREEN_HEIGHT - 48))

  # Stats
    stats = self.font_small.render(
      f"击杀: {player.kills} | 武器: {len(player.weapons)}/{len(WEAPONS)} | 天数: {player.day}",
      True, (160, 170, 180),
    )
    screen.blit(stats, (240, SCREEN_HEIGHT - 28))

    # Disaster status
    dtxt = self.font.render(disaster_status, True, COLOR_ACCENT)
    screen.blit(dtxt, (20, 20))

    # Weapon slots
    for i, ws in enumerate(player.weapons[:8]):
      draw_gun_icon(screen, ws.spec.id, 20 + i * 58, SCREEN_HEIGHT - 100, i == player.weapon_index)

    if len(player.weapons) > 8:
      more = self.font_small.render(f"+{len(player.weapons) - 8}", True, COLOR_TEXT)
      screen.blit(more, (20 + 8 * 58, SCREEN_HEIGHT - 95))

    # Dialogue box
    if self.dialogue_timer > 0:
      self._draw_box(screen, self.dialogue_text, SCREEN_HEIGHT - 140)

    if self.message_timer > 0:
      msg = self.font.render(self.message, True, COLOR_ACCENT)
      screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 60))

    # Crosshair
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 255, 255), (mx, my), 8, 1)
    pygame.draw.line(screen, (255, 255, 255), (mx - 12, my), (mx - 4, my), 1)
    pygame.draw.line(screen, (255, 255, 255), (mx + 4, my), (mx + 12, my), 1)
    pygame.draw.line(screen, (255, 255, 255), (mx, my - 12), (mx, my - 4), 1)
    pygame.draw.line(screen, (255, 255, 255), (mx, my + 4), (mx, my + 12), 1)

    # Help hint
    if self.show_help:
      hints = [
        "WASD移动 | 鼠标瞄准射击 | R换弹 | 1-8切换武器 | Tab武器轮盘",
        "E与NPC对话 | Q拾取武器 | M地图 | H隐藏帮助 | ESC暂停",
      ]
      for i, h in enumerate(hints):
        t = self.font_small.render(h, True, (140, 150, 160))
        screen.blit(t, (SCREEN_WIDTH - t.get_width() - 10, SCREEN_HEIGHT - 50 + i * 18))

  def _bar(self, screen, x, y, w, h, ratio, color, label):
    pygame.draw.rect(screen, (40, 45, 55), (x, y, w, h), border_radius=4)
    pygame.draw.rect(screen, color, (x, y, int(w * max(0, min(1, ratio))), h), border_radius=4)
    if label:
      t = self.font_small.render(f"{label} {int(ratio * 100)}", True, COLOR_TEXT)
      screen.blit(t, (x + 4, y - 1))

  def _draw_box(self, screen, text, y):
    pad = 12
    lines = self._wrap(text, 70)
    h = len(lines) * 22 + pad * 2
    surf = pygame.Surface((SCREEN_WIDTH - 80, h), pygame.SRCALPHA)
    surf.fill((10, 12, 18, 220))
    pygame.draw.rect(surf, COLOR_ACCENT, (0, 0, SCREEN_WIDTH - 80, h), 2, border_radius=8)
    for i, line in enumerate(lines):
      t = self.font.render(line, True, COLOR_TEXT)
      surf.blit(t, (pad, pad + i * 22))
    screen.blit(surf, (40, y))

  def _wrap(self, text: str, width: int) -> list[str]:
    lines = []
    for paragraph in text.split("\n"):
      while len(paragraph) > width:
        lines.append(paragraph[:width])
        paragraph = paragraph[width:]
      if paragraph:
        lines.append(paragraph)
    return lines or [""]

  def draw_title_screen(self, screen: pygame.Surface, alpha: float = 1.0):
    screen.fill((12, 16, 24))
    title = self.font_title.render("无尽寒冬", True, (220, 230, 240))
    subtitle = self.font_large.render("ENDLESS WINTER", True, COLOR_ACCENT)
    story = self.font.render(
      "全球气候崩溃 · 灾难永不停歇 · 在废墟中求生",
      True, (160, 170, 185),
    )
    prompt = self.font.render("按 ENTER 或 点击 开始游戏", True, COLOR_SAFE)

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 240))
    screen.blit(story, (SCREEN_WIDTH // 2 - story.get_width() // 2, 310))

    lore_lines = [
      "灵感来源：《后天》《2012》—— 但假设灾难永远不会结束",
      "极寒风暴、连环地震、无尽洪涝、火山灰幕……轮番降临",
      "感染者与变异动物在废墟中游荡，拾取武器，活下去",
    ]
    for i, line in enumerate(lore_lines):
      t = self.font_small.render(line, True, (120, 130, 145))
      screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 380 + i * 24))

    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 520))

  def draw_pause(self, screen: pygame.Surface):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    title = self.font_large.render("暂停", True, COLOR_TEXT)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    t = self.font.render("按 ESC 继续 | 按 Q 退出", True, (180, 190, 200))
    screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT // 2))

  def draw_weapon_wheel(self, screen: pygame.Surface, player, mouse_pos):
    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    title = self.font_large.render("武器库", True, COLOR_ACCENT)
    screen.blit(title, (cx - title.get_width() // 2, 40))

    cols = 6
    for i, ws in enumerate(player.weapons):
      col = i % cols
      row = i // cols
      x = 80 + col * 190
      y = 100 + row * 70
      selected = i == player.weapon_index
      bg = (60, 70, 90) if selected else (30, 35, 45)
      pygame.draw.rect(screen, bg, (x, y, 180, 60), border_radius=6)
      if selected:
        pygame.draw.rect(screen, COLOR_ACCENT, (x, y, 180, 60), 2, border_radius=6)
      name = self.font.render(f"{i + 1}. {ws.spec.name_cn}", True, COLOR_TEXT)
      detail = self.font_small.render(
        f"{ws.spec.name} | 伤害{ws.spec.damage:.0f} | {ws.spec.category.name}",
        True, (150, 160, 170),
      )
      screen.blit(name, (x + 8, y + 8))
      screen.blit(detail, (x + 8, y + 32))

    hint = self.font_small.render("点击选择武器 | 松开Tab关闭", True, (140, 150, 160))
    screen.blit(hint, (cx - hint.get_width() // 2, SCREEN_HEIGHT - 40))

  def draw_minimap(self, screen: pygame.Surface, world, player, entities, size: int = 160):
    mm = pygame.Surface((size, size))
    mm.fill((20, 25, 30))
    scale = size / 600
    px = int(player.x * scale)
    py = int(player.y * scale)

    for e in entities:
      if not e.alive:
        continue
      ex = int(e.x * scale)
      ey = int(e.y * scale)
      if 0 <= ex < size and 0 <= ey < size:
        color = (80, 160, 255)
        if hasattr(e, "variant"):
          color = (200, 60, 60)
        elif hasattr(e, "animal_type"):
          color = (200, 140, 60)
        elif getattr(e, "hostile", False):
          color = (200, 80, 80)
        pygame.draw.circle(mm, color, (ex, ey), 2)

    pygame.draw.circle(mm, (255, 255, 255), (min(size - 2, px), min(size - 2, py)), 3)
    pygame.draw.rect(screen, (60, 70, 80), (SCREEN_WIDTH - size - 15, 15, size + 4, size + 4), border_radius=4)
    screen.blit(mm, (SCREEN_WIDTH - size - 13, 17))

  def draw_game_over(self, screen: pygame.Surface, player):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    title = self.font_title.render("你已陨落", True, COLOR_DANGER)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    stats = [
      f"存活天数: {player.day}",
      f"击杀数: {player.kills}",
      f"收集武器: {len(player.weapons)}",
      "灾难仍在继续……世界没有尽头",
    ]
    for i, s in enumerate(stats):
      t = self.font.render(s, True, COLOR_TEXT)
      screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 300 + i * 35))
    prompt = self.font.render("按 ENTER 重新开始", True, COLOR_SAFE)
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 500))
