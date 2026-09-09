# -*- coding: utf-8 -*-
"""扩写引擎：剧情核 → 声口旁白 → 一次性意象。不加注水补记。"""

from __future__ import annotations

import re
from collections import deque

try:
    from . import fillers, frames, imagery, voices
    from .lore import COALITION
except ImportError:
    import fillers
    import frames
    import imagery
    import voices
    from lore import COALITION


def cjk_len(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


class Pool:
    def __init__(self, items, kind: str = "细节"):
        self._q = deque(items)
        self.kind = kind

    def take(self, _salt: str = "") -> str:
        if self._q:
            return self._q.popleft()
        return ""


class Engine:
    def __init__(self):
        self.space = Pool(list(imagery.SPACE), "太空")
        self.earth = Pool(list(imagery.EARTH_SCENE), "地面")
        self.room = Pool(list(imagery.ROOM), "室内")
        self.lab = Pool(list(imagery.LAB), "实验室")
        self.war = Pool(list(imagery.WAR), "战场")
        self.human = Pool(list(imagery.HUMAN), "人间")
        self.cosmic = Pool(list(imagery.COSMIC), "宇宙")
        self.openings = Pool(list(imagery.OPENINGS), "开场")
        self.gesture = Pool(list(fillers.GESTURE), "手势")
        self.sound = Pool(list(fillers.SOUND), "声音")
        self.light = Pool(list(fillers.LIGHT), "光线")
        self.object = Pool(list(fillers.OBJECT), "物件")
        self.timeskip = Pool(list(fillers.TIME_SKIP), "时间")
        self.bridge = Pool(list(fillers.BRIDGES), "过渡")
        self.wrap = Pool(list(fillers.WRAP), "节制")
        self.journals = Pool(list(frames.JOURNAL_FRAMES), "手记")
        self.streets = Pool(list(frames.STREET_FRAMES), "切片")
        self.counters = Pool(list(frames.COUNTER_FRAMES), "异议")
        self.radios = Pool(list(frames.RADIO_FRAMES), "短波")
        self.closers = Pool(list(frames.CLOSERS), "收束")
        self.synths = Pool(list(frames.SYNTH), "扩写")
        self._talk_i = 0
        self._beat_i = 0
        self._interior_pools = {
            name: Pool(list(lines), name) for name, lines in voices.INTERIORS.items()
        }
        self._aside_pools = {
            name: Pool(list(lines) if isinstance(lines, list) else [lines], name)
            for name, lines in voices.ASIDES.items()
        }
        self._lead_pools = {
            name: Pool(list(lines) if isinstance(lines, list) else [lines], name)
            for name, lines in voices.LEAD_INS.items()
        }
        self._tag_pools = {name: Pool(list(tags), name) for name, tags in voices.TAGS.items()}

    def _uniq(self, sentence: str) -> str:
        s = (sentence or "").strip()
        if not s:
            return s
        if s[-1] not in "。！？…」》：；":
            s += "。"
        return s

    def _para(self, *parts: str) -> str:
        return "".join(self._uniq(p) for p in parts if p and str(p).strip())

    def _scene_img(self, place: str) -> str:
        p = place
        if any(k in p for k in ("舰", "轨", "门", "木星", "月", "小行星", "曲率", "星门", "船坞", "无敌", "帝江", "同步")):
            return self.space.take()
        if any(k in p for k in ("实验室", "加速器", "纳米", "车间", "SIM", "量子", "材料")):
            return self.lab.take()
        if any(k in p for k in ("靶", "演习", "战场", "试射", "拦截")):
            return self.war.take()
        if any(k in p for k in ("墓", "胡同", "纽约", "北京", "戈壁", "广场", "面包", "学校", "早市", "地铁")):
            return self.earth.take()
        if any(k in p for k in ("宇宙", "森林", "黑暗", "歌者", "思维海洋")):
            return self.cosmic.take()
        return self.room.take()

    def _vars(self, ch: dict, **extra) -> dict:
        beats = ch["beats"]
        talks = ch["talks"]
        talk0 = talks[0][1] if talks else "今天没有值得引用的话。"
        who = extra.get("who", ch["pov"][0])
        place = extra.get("place", ch["places"][0])
        beat = extra.get("beat", beats[0])
        idx = extra.get("idx", 1)
        st = voices.style(who)
        data = {
            "who": who,
            "place": place,
            "title": ch["title"],
            "time": ch["time"],
            "epi": ch["epi"],
            "idx": str(idx),
            "head": str(beat)[:22].rstrip("，。；、"),
            "habit": st["habit"],
            "tone": st["tone"],
            "beat0": beats[0],
            "beat1": beats[len(beats) // 2],
            "beat2": beats[-1],
            "beat_head": beats[0][:18].rstrip("，。；"),
            "talk": talk0,
        }
        data.update(extra)
        return {k: v for k, v in data.items() if k in (
            "who", "place", "title", "time", "epi", "idx", "head", "habit",
            "tone", "beat0", "beat1", "beat2", "beat_head", "talk",
        )}

    def _fill(self, tmpl: str, ch: dict, **extra) -> str:
        return tmpl.format(**self._vars(ch, **extra))

    def _voice_take(self, pools: dict, name: str) -> str:
        key = voices.canon(name)
        pool = pools.get(key)
        return pool.take() if pool else ""

    def _slice_comment(self, beat: str, who: str, place: str, idx: int, salt: int) -> str:
        if not beat:
            return ""
        n = len(beat)
        head = beat[: min(18, n)].rstrip("，。；、")
        mid = beat[max(0, n // 3) : max(0, n // 3) + 16].rstrip("，。；、")
        tail = beat[max(0, n - 16) :].rstrip("，。；、")
        choices = [
            f"“{head}”被{who}按在{place}，后半截“{tail}”不配做口号。",
            f"“{tail}”更像工序。{who}把“{head}”从标题栏拿开。",
            f"“{mid}”若被配乐，{place}只记下“{tail}”。",
            f"{who}摘走“{tail}”，留下“{head}”当可以交班的半句。",
            f"人们记住的是“{head}”停住的那一下，不是“{mid}”的全段。",
            f"{place}把“{mid}”抄错一字，错字旁边仍是“{tail}”。",
        ]
        return choices[(idx + salt) % len(choices)]

    def _synth(self, ch: dict, who: str, place: str, beat: str, idx: int, salt: int) -> str:
        tmpl = frames.SYNTH[(ch["num"] * 13 + idx * 5 + salt * 17) % len(frames.SYNTH)]
        return self._fill(tmpl, ch, who=who, place=place, beat=beat, idx=idx + 1)

    def sides_for(self, ch: dict) -> list[str]:
        if "sides" in ch:
            return list(ch["sides"])
        # 每章最多一块附加，二十章完全不加，避免全套餐。
        return {0: [], 1: ["journal"], 2: ["street"], 3: ["counter"], 4: ["radio"]}[ch["num"] % 5]

    def _wrap_beat(self, beat: str, ch: dict, idx: int) -> str:
        who = ch["pov"][idx % len(ch["pov"])]
        place = ch["places"][idx % len(ch["places"])]
        img = self._scene_img(place)
        inn = self._voice_take(self._interior_pools, who)
        sid = self._voice_take(self._aside_pools, who) if idx == 0 else ""
        c1 = self._slice_comment(beat, who, place, idx, 0)
        c2 = self._slice_comment(beat, who, place, idx, 1)
        s1_tmpl = self.synths.take()
        s1 = self._fill(s1_tmpl, ch, who=who, place=place, beat=beat, idx=idx + 1) if s1_tmpl else ""
        extra = self.gesture.take() or self.sound.take() or ""
        self._beat_i += 1
        mode = (self._beat_i + ch["num"]) % 5
        if mode == 0:
            p1 = self._para(f"{ch['time']}，{place}。", beat, inn)
            p2 = self._para(c1, img)
            p3 = self._para(s1, c2, sid, extra)
        elif mode == 1:
            p1 = self._para(beat, extra)
            p2 = self._para(inn, c2)
            p3 = self._para(img, s1, c1)
        elif mode == 2:
            p1 = self._para(img, beat)
            p2 = self._para(c1, s1)
            p3 = self._para(c2, inn, extra)
        elif mode == 3:
            p1 = self._para(beat, c1)
            p2 = self._para(s1, inn)
            p3 = self._para(c2, img, sid, extra)
        else:
            p1 = self._para(f"{place}。", beat, extra)
            p2 = self._para(c2, inn)
            p3 = self._para(s1, c1)
        return "\n\n".join(p for p in (p1, p2, p3) if p)

    def _talk_block(self, talks: list, start: int, n: int) -> str:
        if start >= len(talks):
            return ""
        chunk = talks[start : start + n]
        lines = []
        for speaker, line in chunk:
            tag_pool = self._tag_pools.get(voices.canon(speaker))
            if tag_pool and tag_pool._q:
                tag = tag_pool.take()
                st = voices.style(speaker)
                if st["len"] in ("short", "careful", "grand"):
                    wrapped = f"{tag}「{line}」"
                else:
                    wrapped = f"「{line}」{tag}"
            else:
                wrapped = f"{speaker}把话放下：「{line}」"
            lines.append(wrapped)
            self._talk_i += 1
        if len(chunk) >= 2:
            lines.insert(1, self.gesture.take())
        if len(chunk) >= 3:
            lines.insert(3, self.sound.take())
        return self._para(*lines)

    def _dossier(self, ch: dict) -> str:
        bits = [f"【《{ch['title']}》现场备忘】"]
        bits.append(f"时间记作{ch['time']}。下面只抄原文，不配乐。")
        for i, beat in enumerate(ch["beats"]):
            bits.append(f"{i + 1}）{beat}")
        bits.append("对话原文留纸。")
        for speaker, line in ch["talks"]:
            bits.append(f"{speaker}：{line}")
        title, body = ch["doc"]
        bits.append(f"文献《{title}》：{body[:120]}")
        return "\n".join(bits) + "\n"

    def _document(self, doc: tuple, num: int = 0) -> str:
        title, body = doc
        return (
            f"\n【文献摘录：{title}】\n"
            f"{body}\n"
            f"摘录至此结束。《{title}》原件离开联网。\n"
        )
        title, body = doc
        return (
            f"\n【文献摘录：{title}】\n"
            f"{body}\n"
            f"摘录至此结束。《{title}》原件离开联网。\n"
        )

    def _journal(self, ch: dict) -> str:
        tmpl = self.journals.take()
        if not tmpl:
            return ""
        return self._fill(tmpl, ch) + "\n"

    def _street(self, ch: dict) -> str:
        tmpl = self.streets.take()
        if not tmpl:
            return ""
        extra = self._para(self.earth.take(), self.human.take(), self.object.take())
        return "【人间】\n" + self._para(self._fill(tmpl, ch), extra) + "\n"

    def _counter(self, ch: dict) -> str:
        tmpl = self.counters.take()
        if not tmpl:
            return ""
        who = ch["pov"][min(1, len(ch["pov"]) - 1)]
        return "【不同意见】\n" + self._para(
            self._fill(tmpl, ch, who=who),
            self.bridge.take(),
        ) + "\n"

    def _radio(self, ch: dict) -> str:
        tmpl = self.radios.take()
        if not tmpl:
            return ""
        return self._para(self._fill(tmpl, ch), self.object.take())

    def _close(self, ch: dict) -> str:
        if ch["num"] == 50:
            return self._para(
                "第五十章把笔停在发现，不写联盟，不写首都，不写田园。",
                "智子已经把其余势力点名。点名不是邀请函，也不是投降书。",
                "未央仍是未完成的草稿。草稿可以活，完成往往是一种会发光的幻觉。",
                f"{COALITION['motto']}",
            )
        tmpl = self.closers.take()
        if not tmpl:
            return self._para(self.bridge.take())
        return self._para(self._fill(tmpl, ch), self.bridge.take() if ch["num"] % 4 == 0 else "")

    def render_chapter(self, ch: dict) -> str:
        sides = set(self.sides_for(ch))
        parts = [
            f"第{ch['num']:02d}章 {ch['title']}",
            f"〔{ch['vol']} · {ch['time']}〕",
            f"题记：{ch['epi']}",
            "",
        ]
        opening = self.openings.take()
        lens_who = ch.get("lens") or ch["pov"][0]
        parts.append(
            self._para(
                opening,
                f"时钟被拨到{ch['time']}。",
                self._scene_img(ch["places"][0]),
                self._voice_take(self._lead_pools, lens_who),
                self._voice_take(self._interior_pools, lens_who),
            )
        )
        parts.append("")

        beats = ch["beats"]
        talks = ch["talks"]
        talk_i = 0
        for i, beat in enumerate(beats):
            if i == 4 and ch["num"] % 3 == 1:
                parts.append(self._para(self.timeskip.take(), self.human.take()))
                parts.append("")
            parts.append(self._wrap_beat(beat, ch, i))
            parts.append("")
            if i % 2 == 1:
                block = self._talk_block(talks, talk_i, 2)
                if block:
                    parts.append(block)
                    parts.append("")
                    talk_i += 2
            if i == 6 and "radio" in sides:
                parts.append(self._radio(ch))
                parts.append("")
                sides.discard("radio")

        if talk_i < len(talks):
            rest = self._talk_block(talks, talk_i, 12)
            if rest:
                parts.append(rest)
                parts.append("")

        if "journal" in sides:
            parts.append(self._journal(ch))
            parts.append("")
        if "street" in sides:
            parts.append(self._street(ch))
            parts.append("")
        if "counter" in sides:
            parts.append(self._counter(ch))
            parts.append("")
        if "radio" in sides:
            parts.append(self._radio(ch))
            parts.append("")

        parts.append(self._dossier(ch))
        parts.append("")
        parts.append(self._document(ch["doc"], ch["num"]))
        parts.append(self._close(ch))
        parts.append("")
        return self._soften("\n".join(parts))

    def _soften(self, text: str) -> str:
        text = text.replace("。\n。", "。\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text


def load_chapters():
    try:
        from .chapters_vol1 import CHAPTERS as a
        from .chapters_vol2 import CHAPTERS as b
        from .chapters_vol3 import CHAPTERS as c
        from .chapters_vol4 import CHAPTERS as d
        from .chapters_vol5 import CHAPTERS as e
        from .chapters_vol6 import CHAPTERS as f
    except ImportError:
        from chapters_vol1 import CHAPTERS as a
        from chapters_vol2 import CHAPTERS as b
        from chapters_vol3 import CHAPTERS as c
        from chapters_vol4 import CHAPTERS as d
        from chapters_vol5 import CHAPTERS as e
        from chapters_vol6 import CHAPTERS as f
    return a + b + c + d + e + f


def novel_header() -> str:
    return (
        "群星未央：黑暗森林联合体\n"
        "\n"
        "——跨文明合作并非简单相加，而可能是指数爆炸。\n"
        "——二次创作长篇。时间锚点：三体危机纪元早期、面壁计划启动之际。\n"
        "——本卷写到三体发现并点名其余势力为止，不写联盟完成，不写田园终局。\n"
        f"——联合体格言（草稿）：{COALITION['motto']}\n"
        "\n"
        "目录按卷：卷一裂隙 / 卷二初遇 / 卷三磨合 / 卷四暗流 / 卷五分类 / 卷六点名\n"
        "\n"
    )


def render_novel() -> str:
    eng = Engine()
    chapters = load_chapters()
    chunks = [novel_header()]
    current_vol = None
    for ch in chapters:
        if ch["vol"] != current_vol:
            current_vol = ch["vol"]
            chunks.append("\n" + "=" * 16 + f" {current_vol} " + "=" * 16 + "\n\n")
        chunks.append(eng.render_chapter(ch))
        chunks.append("\n")
    return "".join(chunks)
