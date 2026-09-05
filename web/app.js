const snow = document.getElementById("snow");
const sctx = snow.getContext("2d");
const flakes = Array.from({ length: 90 }, () => ({
  x: Math.random(),
  y: Math.random(),
  r: Math.random() * 1.8 + 0.4,
  v: Math.random() * 0.35 + 0.12,
}));

function resizeSnow() {
  snow.width = innerWidth;
  snow.height = innerHeight;
}

function drawSnow() {
  sctx.clearRect(0, 0, snow.width, snow.height);
  sctx.fillStyle = "rgba(220, 235, 255, 0.7)";
  for (const f of flakes) {
    f.y += f.v / 120;
    f.x += Math.sin(f.y * 8) * 0.0004;
    if (f.y > 1) f.y = 0;
    sctx.beginPath();
    sctx.arc(f.x * snow.width, f.y * snow.height, f.r, 0, Math.PI * 2);
    sctx.fill();
  }
  requestAnimationFrame(drawSnow);
}

resizeSnow();
addEventListener("resize", resizeSnow);
drawSnow();

const DISASTERS = [
  ["超级暴风雪", "#9ecbff"],
  ["连环地震", "#c9a27a"],
  ["无尽洪涝", "#4d8cff"],
  ["火山灰幕", "#8a8a8f"],
  ["极寒冻结", "#b9e7ff"],
  ["陨石雨", "#ffb36a"],
  ["剧毒迷雾", "#86d18a"],
  ["太阳风暴", "#ff6b4a"],
];

const canvas = document.getElementById("arena");
const ctx = canvas.getContext("2d");
const hpEl = document.getElementById("hp");
const scoreEl = document.getElementById("score");
const eventEl = document.getElementById("event");
const overlay = document.getElementById("overlay");
const stick = document.getElementById("stick");
const knob = stick.querySelector(".knob");
const fireBtn = document.getElementById("fire");

let running = false;
let move = { x: 0, y: 0 };
let firing = false;
let keys = {};
const state = {
  t: 0,
  hp: 100,
  player: { x: 360, y: 240 },
  bullets: [],
  foes: [],
  disaster: 0,
  nextDisaster: 8,
};

function spawnFoe() {
  const edge = Math.floor(Math.random() * 4);
  const p = { x: 0, y: 0, s: 28 + Math.random() * 22 };
  if (edge === 0) { p.x = Math.random() * canvas.width; p.y = -10; }
  if (edge === 1) { p.x = canvas.width + 10; p.y = Math.random() * canvas.height; }
  if (edge === 2) { p.x = Math.random() * canvas.width; p.y = canvas.height + 10; }
  if (edge === 3) { p.x = -10; p.y = Math.random() * canvas.height; }
  state.foes.push(p);
}

function reset() {
  state.t = 0;
  state.hp = 100;
  state.player = { x: canvas.width / 2, y: canvas.height / 2 };
  state.bullets = [];
  state.foes = [];
  state.disaster = 0;
  state.nextDisaster = 6;
  for (let i = 0; i < 6; i++) spawnFoe();
}

function startGame() {
  reset();
  running = true;
  overlay.hidden = true;
  stick.hidden = false;
  fireBtn.hidden = false;
}

document.getElementById("start").addEventListener("click", startGame);

addEventListener("keydown", (e) => {
  keys[e.key.toLowerCase()] = true;
  if (e.code === "Space") firing = true;
});
addEventListener("keyup", (e) => {
  keys[e.key.toLowerCase()] = false;
  if (e.code === "Space") firing = false;
});

function setStick(clientX, clientY) {
  const rect = stick.getBoundingClientRect();
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  let dx = clientX - cx;
  let dy = clientY - cy;
  const max = 28;
  const mag = Math.hypot(dx, dy) || 1;
  dx = (dx / mag) * Math.min(mag, max);
  dy = (dy / mag) * Math.min(mag, max);
  knob.style.transform = `translate(${dx}px, ${dy}px)`;
  move.x = dx / max;
  move.y = dy / max;
}

function clearStick() {
  knob.style.transform = "translate(0, 0)";
  move.x = 0;
  move.y = 0;
}

stick.addEventListener("pointerdown", (e) => {
  stick.setPointerCapture(e.pointerId);
  setStick(e.clientX, e.clientY);
});
stick.addEventListener("pointermove", (e) => {
  if (e.pressure || (e.buttons & 1)) setStick(e.clientX, e.clientY);
});
stick.addEventListener("pointerup", clearStick);
stick.addEventListener("pointercancel", clearStick);

fireBtn.addEventListener("pointerdown", (e) => {
  e.preventDefault();
  firing = true;
});
fireBtn.addEventListener("pointerup", () => { firing = false; });
fireBtn.addEventListener("pointercancel", () => { firing = false; });

let cooldown = 0;
function shoot() {
  if (cooldown > 0) return;
  cooldown = 0.16;
  const aim = nearestFoe();
  const dx = aim ? aim.x - state.player.x : 1;
  const dy = aim ? aim.y - state.player.y : 0;
  const mag = Math.hypot(dx, dy) || 1;
  state.bullets.push({
    x: state.player.x,
    y: state.player.y,
    vx: (dx / mag) * 380,
    vy: (dy / mag) * 380,
    life: 0.9,
  });
}

function nearestFoe() {
  let best = null;
  let dist = Infinity;
  for (const f of state.foes) {
    const d = Math.hypot(f.x - state.player.x, f.y - state.player.y);
    if (d < dist) {
      dist = d;
      best = f;
    }
  }
  return best;
}

function tick(dt) {
  if (!running) return;
  state.t += dt;
  state.nextDisaster -= dt;
  cooldown = Math.max(0, cooldown - dt);
  if (state.nextDisaster <= 0) {
    state.disaster = (state.disaster + 1) % DISASTERS.length;
    state.nextDisaster = 7 + Math.random() * 4;
  }

  let mx = move.x;
  let my = move.y;
  if (keys.w || keys.arrowup) my -= 1;
  if (keys.s || keys.arrowdown) my += 1;
  if (keys.a || keys.arrowleft) mx -= 1;
  if (keys.d || keys.arrowright) mx += 1;
  const mag = Math.hypot(mx, my);
  if (mag > 1) {
    mx /= mag;
    my /= mag;
  }
  const speed = 150;
  state.player.x = Math.max(12, Math.min(canvas.width - 12, state.player.x + mx * speed * dt));
  state.player.y = Math.max(12, Math.min(canvas.height - 12, state.player.y + my * speed * dt));

  if (firing) shoot();

  if (state.foes.length < 8 + Math.floor(state.t / 12)) spawnFoe();

  for (const f of state.foes) {
    const dx = state.player.x - f.x;
    const dy = state.player.y - f.y;
    const d = Math.hypot(dx, dy) || 1;
    f.x += (dx / d) * f.s * dt;
    f.y += (dy / d) * f.s * dt;
    if (d < 18) state.hp -= 18 * dt;
  }

  for (const b of state.bullets) {
    b.x += b.vx * dt;
    b.y += b.vy * dt;
    b.life -= dt;
  }
  state.bullets = state.bullets.filter((b) => b.life > 0);
  state.foes = state.foes.filter((f) => {
    const hit = state.bullets.some((b) => Math.hypot(b.x - f.x, b.y - f.y) < 14);
    return !hit;
  });

  const disasterDmg = 1.2 + state.disaster * 0.15;
  state.hp -= disasterDmg * dt;
  hpEl.style.width = `${Math.max(0, state.hp)}%`;
  scoreEl.textContent = `${state.t.toFixed(0)}s`;
  eventEl.textContent = DISASTERS[state.disaster][0];

  if (state.hp <= 0) {
    running = false;
    overlay.hidden = false;
    overlay.querySelector("h3").textContent = `你撑过了 ${state.t.toFixed(0)} 秒`;
    overlay.querySelector("p").textContent = "寒冬仍在继续。再试一次。";
    overlay.querySelector("button").textContent = "再次进入";
  }
}

function draw() {
  ctx.fillStyle = "#071018";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = DISASTERS[state.disaster][1] + "22";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(126,200,255,0.08)";
  for (let x = 0; x < canvas.width; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }

  ctx.fillStyle = "#6ad07a";
  for (const f of state.foes) {
    ctx.beginPath();
    ctx.arc(f.x, f.y, 8, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.fillStyle = "#ffd27a";
  for (const b of state.bullets) {
    ctx.fillRect(b.x - 2, b.y - 2, 4, 4);
  }

  ctx.fillStyle = "#ff8a3a";
  ctx.beginPath();
  ctx.arc(state.player.x, state.player.y, 9, 0, Math.PI * 2);
  ctx.fill();
}

let last = performance.now();
function loop(now) {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;
  tick(dt);
  draw();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
