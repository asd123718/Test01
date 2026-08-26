"""Weapon definitions - extensive firearm catalog."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class WeaponCategory(Enum):
    PISTOL = auto()
    SMG = auto()
    RIFLE = auto()
    SHOTGUN = auto()
    SNIPER = auto()
    LMG = auto()
    SPECIAL = auto()


@dataclass(frozen=True)
class WeaponSpec:
    id: str
    name: str
    name_cn: str
    category: WeaponCategory
    damage: float
    fire_rate: float  # shots per second
    magazine: int
    reload_time: float
    bullet_speed: float
    spread: float  # radians
    pellets: int = 1
    range_px: float = 700
    automatic: bool = True
    description: str = ""


WEAPONS: dict[str, WeaponSpec] = {}

def _add(spec: WeaponSpec) -> WeaponSpec:
    WEAPONS[spec.id] = spec
    return spec


# --- Pistols ---
_add(WeaponSpec("glock17", "Glock 17", "格洛克17", WeaponCategory.PISTOL, 22, 4.5, 17, 1.4, 620, 0.04))
_add(WeaponSpec("m1911", "M1911", "M1911", WeaponCategory.PISTOL, 28, 3.5, 8, 1.6, 600, 0.035, automatic=False))
_add(WeaponSpec("deagle", "Desert Eagle", "沙漠之鹰", WeaponCategory.PISTOL, 45, 2.2, 7, 1.8, 650, 0.06, automatic=False))
_add(WeaponSpec("makarov", "Makarov PM", "马卡洛夫", WeaponCategory.PISTOL, 20, 3.8, 8, 1.5, 580, 0.045, automatic=False))
_add(WeaponSpec("usp", "HK USP", "USP", WeaponCategory.PISTOL, 24, 4.0, 12, 1.5, 610, 0.038))
_add(WeaponSpec("p226", "SIG P226", "P226", WeaponCategory.PISTOL, 23, 4.2, 15, 1.45, 605, 0.04))
_add(WeaponSpec("five_seven", "FN Five-seveN", "FN57", WeaponCategory.PISTOL, 26, 4.8, 20, 1.5, 640, 0.035))
_add(WeaponSpec("cz75", "CZ 75", "CZ75", WeaponCategory.PISTOL, 24, 4.0, 16, 1.5, 600, 0.04))
_add(WeaponSpec("revolver_357", "Colt Python", "蟒蛇左轮", WeaponCategory.PISTOL, 42, 1.8, 6, 2.2, 580, 0.05, automatic=False))
_add(WeaponSpec("glock18", "Glock 18", "格洛克18", WeaponCategory.PISTOL, 20, 12.0, 33, 1.6, 600, 0.08))

# --- SMGs ---
_add(WeaponSpec("mp5", "HK MP5", "MP5", WeaponCategory.SMG, 18, 9.0, 30, 1.8, 680, 0.06))
_add(WeaponSpec("uzi", "Uzi", "乌兹", WeaponCategory.SMG, 16, 10.0, 32, 1.7, 650, 0.08))
_add(WeaponSpec("vector", "KRISS Vector", "维克托", WeaponCategory.SMG, 17, 11.0, 25, 1.6, 700, 0.05))
_add(WeaponSpec("p90", "FN P90", "P90", WeaponCategory.SMG, 16, 10.5, 50, 2.0, 720, 0.055))
_add(WeaponSpec("mp7", "HK MP7", "MP7", WeaponCategory.SMG, 15, 11.5, 40, 1.7, 710, 0.05))
_add(WeaponSpec("ump45", "HK UMP45", "UMP45", WeaponCategory.SMG, 22, 7.5, 25, 1.8, 660, 0.065))
_add(WeaponSpec("pp19", "PP-19 Bizon", "野牛", WeaponCategory.SMG, 17, 8.5, 64, 2.2, 670, 0.07))
_add(WeaponSpec("thompson", "Thompson M1A1", "汤普森", WeaponCategory.SMG, 20, 8.0, 30, 2.0, 640, 0.07))
_add(WeaponSpec("mp40", "MP40", "MP40", WeaponCategory.SMG, 18, 8.5, 32, 1.9, 630, 0.07))
_add(WeaponSpec("scorpion", "CZ Scorpion EVO", "蝎式", WeaponCategory.SMG, 17, 10.0, 30, 1.7, 690, 0.06))

# --- Assault Rifles ---
_add(WeaponSpec("ak47", "AK-47", "AK-47", WeaponCategory.RIFLE, 32, 6.5, 30, 2.2, 750, 0.05))
_add(WeaponSpec("m4a1", "M4A1", "M4A1", WeaponCategory.RIFLE, 28, 8.5, 30, 2.0, 780, 0.04))
_add(WeaponSpec("scar_h", "FN SCAR-H", "SCAR-H", WeaponCategory.RIFLE, 38, 5.5, 20, 2.3, 760, 0.045))
_add(WeaponSpec("aug", "Steyr AUG", "AUG", WeaponCategory.RIFLE, 27, 8.0, 30, 2.1, 770, 0.04))
_add(WeaponSpec("famas", "FAMAS", "法玛斯", WeaponCategory.RIFLE, 26, 9.5, 25, 2.0, 760, 0.045))
_add(WeaponSpec("g36", "HK G36", "G36", WeaponCategory.RIFLE, 27, 8.5, 30, 2.0, 775, 0.04))
_add(WeaponSpec("galil", "IMI Galil", "加利尔", WeaponCategory.RIFLE, 30, 7.0, 35, 2.2, 740, 0.05))
_add(WeaponSpec("hk416", "HK416", "HK416", WeaponCategory.RIFLE, 29, 8.0, 30, 2.0, 780, 0.038))
_add(WeaponSpec("an94", "AN-94", "AN-94", WeaponCategory.RIFLE, 31, 7.5, 30, 2.3, 750, 0.042))
_add(WeaponSpec("qbz95", "QBZ-95", "95式", WeaponCategory.RIFLE, 28, 7.5, 30, 2.1, 760, 0.045))
_add(WeaponSpec("tar21", "TAR-21", "TAR-21", WeaponCategory.RIFLE, 29, 7.8, 30, 2.1, 770, 0.043))
_add(WeaponSpec("as_val", "AS VAL", "AS VAL", WeaponCategory.RIFLE, 30, 7.0, 20, 2.2, 720, 0.04, range_px=550))

# --- Shotguns ---
_add(WeaponSpec("rem870", "Remington 870", "雷明顿870", WeaponCategory.SHOTGUN, 12, 1.2, 6, 2.5, 500, 0.25, pellets=8, automatic=False))
_add(WeaponSpec("spas12", "SPAS-12", "SPAS-12", WeaponCategory.SHOTGUN, 11, 1.8, 8, 2.4, 520, 0.22, pellets=8))
_add(WeaponSpec("aa12", "AA-12", "AA-12", WeaponCategory.SHOTGUN, 10, 4.0, 20, 2.8, 480, 0.2, pellets=6))
_add(WeaponSpec("m1014", "Benelli M4", "M1014", WeaponCategory.SHOTGUN, 12, 2.5, 7, 2.3, 510, 0.2, pellets=7))
_add(WeaponSpec("ksg", "Kel-Tec KSG", "KSG", WeaponCategory.SHOTGUN, 13, 1.0, 14, 2.6, 490, 0.24, pellets=9, automatic=False))
_add(WeaponSpec("saiga12", "Saiga-12", "Saiga-12", WeaponCategory.SHOTGUN, 11, 3.5, 10, 2.5, 500, 0.22, pellets=7))
_add(WeaponSpec("mossberg500", "Mossberg 500", "莫斯伯格500", WeaponCategory.SHOTGUN, 12, 1.1, 8, 2.4, 495, 0.23, pellets=8, automatic=False))
_add(WeaponSpec("double_barrel", "Double Barrel", "双管猎枪", WeaponCategory.SHOTGUN, 14, 0.8, 2, 1.8, 480, 0.28, pellets=10, automatic=False))

# --- Snipers ---
_add(WeaponSpec("awm", "AWM", "AWM", WeaponCategory.SNIPER, 95, 0.8, 5, 3.0, 950, 0.01, automatic=False, range_px=1200))
_add(WeaponSpec("m82", "Barrett M82", "巴雷特M82", WeaponCategory.SNIPER, 120, 0.6, 10, 3.5, 980, 0.015, automatic=False, range_px=1400))
_add(WeaponSpec("dragunov", "SVD Dragunov", "德拉古诺夫", WeaponCategory.SNIPER, 75, 1.2, 10, 2.8, 920, 0.02, automatic=False, range_px=1100))
_add(WeaponSpec("m24", "M24 SWS", "M24", WeaponCategory.SNIPER, 88, 0.9, 5, 2.9, 940, 0.012, automatic=False, range_px=1150))
_add(WeaponSpec("l96", "L96A1", "L96", WeaponCategory.SNIPER, 90, 0.85, 5, 2.9, 935, 0.012, automatic=False, range_px=1180))
_add(WeaponSpec("vss", "VSS Vintorez", "VSS", WeaponCategory.SNIPER, 55, 2.0, 10, 2.5, 800, 0.025, range_px=800))
_add(WeaponSpec("m200", "CheyTac M200", "M200", WeaponCategory.SNIPER, 110, 0.5, 7, 3.8, 1000, 0.008, automatic=False, range_px=1500))
_add(WeaponSpec("kar98k", "Kar98k", "Kar98k", WeaponCategory.SNIPER, 80, 0.7, 5, 2.5, 900, 0.015, automatic=False, range_px=1000))

# --- LMGs ---
_add(WeaponSpec("m249", "M249 SAW", "M249", WeaponCategory.LMG, 26, 10.0, 100, 4.0, 780, 0.06))
_add(WeaponSpec("rpk", "RPK", "RPK", WeaponCategory.LMG, 28, 8.0, 75, 3.5, 760, 0.055))
_add(WeaponSpec("pkp", "PKP Pecheneg", "PKP", WeaponCategory.LMG, 32, 7.5, 100, 4.2, 770, 0.058))
_add(WeaponSpec("mg42", "MG42", "MG42", WeaponCategory.LMG, 30, 12.0, 100, 4.5, 790, 0.07))
_add(WeaponSpec("m60", "M60", "M60", WeaponCategory.LMG, 30, 7.0, 100, 4.0, 750, 0.06))
_add(WeaponSpec("negev", "IWI Negev", "内盖夫", WeaponCategory.LMG, 27, 9.5, 150, 4.5, 785, 0.055))

# --- Special ---
_add(WeaponSpec("crossbow", "Crossbow", "十字弩", WeaponCategory.SPECIAL, 65, 0.9, 1, 2.0, 700, 0.0, automatic=False, range_px=600))
_add(WeaponSpec("flamethrower", "Flamethrower", "火焰喷射器", WeaponCategory.SPECIAL, 8, 15.0, 100, 3.0, 350, 0.3, pellets=3, range_px=200))
_add(WeaponSpec("rpg7", "RPG-7", "RPG-7", WeaponCategory.SPECIAL, 200, 0.5, 1, 3.5, 500, 0.02, automatic=False, range_px=800))
_add(WeaponSpec("m79", "M79 Grenade Launcher", "M79榴弹", WeaponCategory.SPECIAL, 150, 0.7, 6, 2.8, 450, 0.05, automatic=False, range_px=500))
_add(WeaponSpec("bow", "Compound Bow", "复合弓", WeaponCategory.SPECIAL, 50, 1.5, 1, 1.5, 680, 0.02, automatic=False, range_px=650))
_add(WeaponSpec("taser", "Taser X26", "泰瑟枪", WeaponCategory.SPECIAL, 5, 1.0, 1, 1.2, 200, 0.0, automatic=False, range_px=120))
_add(WeaponSpec("machete", "Machete", "砍刀", WeaponCategory.SPECIAL, 35, 2.5, 999, 0.0, 0, 0.0, automatic=False, range_px=50))
_add(WeaponSpec("combat_knife", "Combat Knife", "格斗刀", WeaponCategory.SPECIAL, 30, 3.0, 999, 0.0, 0, 0.0, automatic=False, range_px=45))

# --- DMR / Battle Rifles ---
_add(WeaponSpec("m14", "M14 EBR", "M14", WeaponCategory.RIFLE, 42, 3.5, 20, 2.5, 800, 0.03, automatic=False))
_add(WeaponSpec("mk14", "Mk 14 EBR", "Mk14", WeaponCategory.RIFLE, 40, 4.0, 20, 2.4, 810, 0.03))
_add(WeaponSpec("svd", "SVD", "SVD", WeaponCategory.SNIPER, 70, 1.5, 10, 2.6, 900, 0.02, automatic=False))
_add(WeaponSpec("fal", "FN FAL", "FAL", WeaponCategory.RIFLE, 36, 5.0, 20, 2.4, 770, 0.04))
_add(WeaponSpec("g3", "HK G3", "G3", WeaponCategory.RIFLE, 35, 5.5, 20, 2.5, 760, 0.045))
_add(WeaponSpec("m16a4", "M16A4", "M16A4", WeaponCategory.RIFLE, 30, 7.0, 30, 2.2, 790, 0.035, automatic=False))
_add(WeaponSpec("type56", "Type 56", "56式", WeaponCategory.RIFLE, 31, 6.0, 30, 2.2, 740, 0.05))
_add(WeaponSpec("stg44", "StG 44", "StG44", WeaponCategory.RIFLE, 28, 5.5, 30, 2.5, 720, 0.05))
_add(WeaponSpec("mcx", "SIG MCX", "MCX", WeaponCategory.RIFLE, 29, 8.0, 30, 2.0, 780, 0.038))
_add(WeaponSpec("acr", "Remington ACR", "ACR", WeaponCategory.RIFLE, 28, 8.0, 30, 2.1, 775, 0.04))

# --- More Pistols & Revolvers ---
_add(WeaponSpec("beretta92", "Beretta 92FS", "伯莱塔92", WeaponCategory.PISTOL, 23, 4.0, 15, 1.5, 600, 0.04))
_add(WeaponSpec("walther_ppk", "Walther PPK", "PPK", WeaponCategory.PISTOL, 20, 3.5, 7, 1.4, 560, 0.045, automatic=False))
_add(WeaponSpec("ruger_mk4", "Ruger Mk IV", "鲁格Mk4", WeaponCategory.PISTOL, 19, 5.0, 10, 1.3, 590, 0.035))
_add(WeaponSpec("sw500", "S&W 500", "史密斯500", WeaponCategory.PISTOL, 55, 1.2, 5, 2.5, 550, 0.06, automatic=False))

# --- More SMGs ---
_add(WeaponSpec("mac10", "MAC-10", "MAC-10", WeaponCategory.SMG, 15, 11.0, 32, 1.6, 640, 0.09))
_add(WeaponSpec("sten", "Sten Mk II", "斯登", WeaponCategory.SMG, 17, 7.0, 32, 1.9, 620, 0.08))

# --- More Shotguns ---
_add(WeaponSpec("ithaca37", "Ithaca 37", "伊萨卡37", WeaponCategory.SHOTGUN, 12, 1.0, 5, 2.3, 490, 0.24, pellets=8, automatic=False))
_add(WeaponSpec("usas12", "USAS-12", "USAS-12", WeaponCategory.SHOTGUN, 10, 3.0, 20, 2.6, 490, 0.22, pellets=6))

# --- More Snipers ---
_add(WeaponSpec("tac50", "McMillan TAC-50", "TAC-50", WeaponCategory.SNIPER, 130, 0.45, 5, 4.0, 1000, 0.008, automatic=False, range_px=1500))
_add(WeaponSpec("psg1", "HK PSG-1", "PSG-1", WeaponCategory.SNIPER, 85, 1.0, 5, 3.2, 930, 0.01, automatic=False, range_px=1100))
_add(WeaponSpec("mosin", "Mosin-Nagant", "莫辛纳甘", WeaponCategory.SNIPER, 78, 0.75, 5, 2.6, 880, 0.015, automatic=False, range_px=1000))

# --- More Special ---
_add(WeaponSpec("minigun", "M134 Minigun", "加特林", WeaponCategory.LMG, 22, 20.0, 500, 6.0, 800, 0.1))
_add(WeaponSpec("m320", "M320 GLM", "M320榴弹", WeaponCategory.SPECIAL, 140, 0.6, 5, 3.0, 420, 0.04, automatic=False, range_px=450))
_add(WeaponSpec("spear", "Spear", "长矛", WeaponCategory.SPECIAL, 40, 1.5, 999, 0.0, 0, 0.0, automatic=False, range_px=55))


STARTER_WEAPONS = ["glock17", "m4a1", "rem870", "ak47", "mp5", "crossbow", "machete"]

WEAPON_LIST = list(WEAPONS.keys())


def get_weapon(weapon_id: str) -> WeaponSpec:
    return WEAPONS[weapon_id]


def weapons_by_category(category: WeaponCategory) -> list[WeaponSpec]:
    return [w for w in WEAPONS.values() if w.category == category]
