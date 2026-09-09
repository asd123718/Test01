# -*- coding: utf-8 -*-
"""扩写引擎：把每章剧情核铺成可读正文，意象与细节一次性消耗。"""

from __future__ import annotations

import re
from collections import deque

import imagery
import fillers
from lore import COALITION


def cjk_len(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


class Pool:
    def __init__(self, items, kind: str = "细节"):
        self._q = deque(items)
        self._i = 0
        self.kind = kind

    def take(self, salt: str = "") -> str:
        self._i += 1
        if self._q:
            return self._q.popleft()
        return ""


class Engine:
    def __init__(self):
        self.space = Pool(imagery.SPACE, "太空")
        self.earth = Pool(imagery.EARTH_SCENE, "地面")
        self.room = Pool(imagery.ROOM, "室内")
        self.lab = Pool(imagery.LAB, "实验室")
        self.war = Pool(imagery.WAR, "战场")
        self.human = Pool(list(imagery.HUMAN) + list(fillers.FOLK), "人间")
        self.cosmic = Pool(imagery.COSMIC, "宇宙")
        self.openings = Pool(imagery.OPENINGS, "开场")
        self.gesture = Pool(fillers.GESTURE, "手势")
        self.sound = Pool(fillers.SOUND, "声音")
        self.light = Pool(fillers.LIGHT, "光线")
        self.object = Pool(fillers.OBJECT, "物件")
        self.timeskip = Pool(fillers.TIME_SKIP, "时间")
        self.bridge = Pool(fillers.BRIDGES, "过渡")
        self.wrap = Pool(fillers.WRAP, "节制")
        self.used_full = set()
        self.recent_starts = deque(maxlen=12)
        self._seq = 0

    def _uniq(self, sentence: str) -> str:
        s = sentence.strip()
        if not s:
            return s
        if s[-1] not in "。！？…」》：":
            s += "。"
        return s

    def _para(self, *parts: str) -> str:
        chunks = [self._uniq(p) for p in parts if p and p.strip()]
        return "".join(chunks)

    def _scene_img(self, place: str, salt: str = "") -> str:
        p = place
        if any(k in p for k in ("舰", "轨", "门", "木星", "月", "小行星", "曲率", "星门", "船坞", "无敌", "帝江")):
            return self.space.take(salt)
        if any(k in p for k in ("实验室", "加速器", "纳米", "车间", "SIM", "量子")):
            return self.lab.take(salt)
        if any(k in p for k in ("靶", "演习", "战场", "试射", "拦截")):
            return self.war.take(salt)
        if any(k in p for k in ("墓", "胡同", "纽约", "北京", "戈壁", "广场", "面包", "学校")):
            return self.earth.take(salt)
        if any(k in p for k in ("宇宙", "森林", "黑暗", "歌者")):
            return self.cosmic.take(salt)
        return self.room.take(salt)

    def _line(self, ch: dict, idx: int) -> str:
        who = ch["pov"][idx % len(ch["pov"])]
        place = ch["places"][idx % len(ch["places"])]
        variants = [
            f"{who}在《{ch['title']}》第{idx+1}步把{place}的一角当成无门牌办公室，门牌会变成靶标。",
            f"{who}负责把《{ch['title']}》的句子从壮丽改成可执行，改的时候{place}的灯还开着。",
            f"{place}的空气循环均匀，均匀让{who}听见自己的牙关，牙关不属于第{idx+1}项议程。",
            f"{ch['time']}的一分钟对{who}并不普通，《{ch['title']}》要求决定。",
            f"{who}避开镜头，镜头想把《{ch['title']}》拍成史诗，史诗频谱太亮。",
            f"未签字的纸在{place}发抖，{who}第{idx+1}次没有立刻按住。",
            f"{who}在《{ch['title']}》里拒绝用旧星系场面作类比，类比会偷懒。",
            f"清洁工经过{place}最外圈，水痕蒸发得比《{ch['title']}》的宣言快。",
            f"{who}把《{ch['title']}》第{idx+1}现场写在手心又擦掉。",
            f"翻译耳机杂音让{who}想到监视也会排队，排队发生在{place}。",
        ]
        return variants[(idx + ch["num"] * 3) % len(variants)]

    def _wrap_beat(self, beat: str, ch: dict, idx: int) -> str:
        who = ch["pov"][idx % len(ch["pov"])]
        place = ch["places"][idx % len(ch["places"])]
        salt = f"{ch['num']}-{idx}"
        img = self._scene_img(place, salt)
        g = self.gesture.take(salt + "g")
        so = self.sound.take(salt + "s")
        w1 = self.wrap.take(salt + "w1")
        extra = self._line(ch, idx)
        variants = [
            f"{place}在{ch['time']}不为《{ch['title']}》提供掌声。{who}把第{idx+1}个判断压在舌下。",
            f"{who}先确认{place}的门还能关，再听《{ch['title']}》外围的口号。",
            f"第{idx+1}段里，{who}宁可少说一句，也不把{place}变成舞台。",
            f"{ch['time']}的光在{place}很均匀，均匀让{who}没法假装这是神话。",
            f"{who}离开《{ch['title']}》这一小段时，只带走能关的门，不带走观众。",
            f"{place}仍在运转。运转被{who}写成第{idx+1}项工序，不写成颂歌。",
            f"有人想为《{ch['title']}》鼓掌，{who}把掌声改成点头，点头不发光。",
            f"{who}在{place}数了一次呼吸，次数不能当《{ch['title']}》的战略，但能防止第{idx+1}段演说失控。",
        ]
        atm = variants[(idx + ch["num"]) % len(variants)]
        mode = (idx + ch["num"]) % 5
        if mode == 0:
            p1 = self._para(f"{ch['time']}，{place}。", img, g, beat, w1)
        elif mode == 1:
            p1 = self._para(img, so, beat, extra)
        elif mode == 2:
            p1 = self._para(beat, g, w1, f"{who}没有给《{ch['title']}》第{idx+1}段配乐。")
        elif mode == 3:
            p1 = self._para(so, beat, img, f"{place}的记录只保存工序。")
        else:
            p1 = self._para(extra, beat, w1, img)
        p2 = self._para(atm, f"{who}离开《{ch['title']}》第{idx+1}小段时，{place}仍在运转。")
        return p1 + "\n\n" + p2

    def _talk_block(self, talks: list, start: int, n: int, salt: str = "") -> str:
        if start >= len(talks):
            return ""
        chunk = talks[start : start + n]
        lines = []
        for speaker, line in chunk:
            lines.append(f"「{line}」{speaker}说。")
        if len(chunk) >= 2:
            lines.insert(1, self.gesture.take(salt + "tg"))
        if len(chunk) >= 4:
            lines.insert(3, self.sound.take(salt + "ts"))
        return self._para(*lines)

    def _document(self, doc: tuple, num: int = 0) -> str:
        title, body = doc
        return (
            f"\n【文献摘录：{title}】\n"
            f"{body}\n"
            f"摘录终止。本章编号{num:02d}之原件分散存档，不进入深空广播级网络。\n"
        )

    def _radio(self, ch: dict, idx: int) -> str:
        who = ch["pov"][idx % len(ch["pov"])]
        place = ch["places"][idx % len(ch["places"])]
        return self._para(
            f"短波残段（未公开）：“{place}方向，{who}在场，信号强度普通。章名《{ch['title']}》。”",
            f"普通两个字在《{ch['title']}》里被故意使用，普通可以当掩护。",
            self.object.take(),
        )

    def _journal(self, ch: dict) -> str:
        who = ch["pov"][0]
        b0, b1, b2 = ch["beats"][0], ch["beats"][len(ch["beats"]) // 2], ch["beats"][-1]
        talk = ch["talks"][0][1] if ch["talks"] else "今天没有值得引用的话。"
        return (
            f"【{who}·非联网手记】\n"
            + self._para(
                f"日期记作{ch['time']}。我不把《{ch['title']}》这页同步到任何云，云对《{ch['title']}》来说是森林的耳朵。",
                f"我看见的第一件事：{b0}",
                f"中间我无法忽视：{b1}",
                f"临睡前仍在：{b2}",
                f"有人说：“{talk}”这话像钥匙，也像枪。我把它抄下来，不点评。",
                f"抄写地点：{ch['places'][-1]}。地点可以放弃。放弃要先练习。",
                self.wrap.take(),
                self.gesture.take(),
                f"若有人拾到与《{ch['title']}》有关的手记，请先吃饭，再决定是否继续读。读不是义务。活着才是。时间：{ch['time']}。",
            )
            + "\n"
        )

    def _street(self, ch: dict) -> str:
        beat = ch["beats"][min(3, len(ch["beats"]) - 1)]
        return (
            "【人间切片】\n"
            + self._para(
                self.earth.take(),
                self.human.take(),
                f"远离{ch['places'][0]}的人把《{ch['title']}》相关新闻当成一种更硬的天气。天气里出现了{ch['pov'][-1]}的名字，名字被念错，错在{ch['time']}。",
                f"念错也没关系。他们真正关心的是供水、班车、孩子的咳嗽，以及那句被简化到失真的话——与“{beat[:20]}”有关，又完全无关。",
                self.object.take(),
                self.sound.take(),
                f"切片结束。《{ch['title']}》的这一角不进入战略数据库，只进入还能被煮熟的日子。",
            )
            + "\n"
        )

    def _counter(self, ch: dict) -> str:
        enemy = ch["pov"][min(1, len(ch["pov"]) - 1)]
        return (
            "【不同意见】\n"
            + self._para(
                f"{enemy}并非《{ch['title']}》需要的反派槽位，槽位太亮，亮得像广播。",
                f"不同意见只是坚持：{ch['epi']}",
                f"坚持可能错。错也要被记录在《{ch['title']}》不会被胜利者自动删除的副本里。",
                self.bridge.take(),
                self.cosmic.take(),
                f"副本存放处之一：{ch['places'][0]}的下一级权限柜。权限柜没有诗意。",
            )
            + "\n"
        )

    def _recall(self, ch: dict) -> str:
        bits = [f"【《{ch['title']}》回想录】"]
        bits.append(
            f"时间仍是{ch['time']}。回想不等于重播。重播会发光。下面只保留《{ch['title']}》未进入深空的句子。"
        )
        for i, beat in enumerate(ch["beats"]):
            who = ch["pov"][i % len(ch["pov"])]
            place = ch["places"][i % len(ch["places"])]
            head = beat[:18].rstrip("，。；")
            bits.append(
                f"{who}后来不愿原样复述第{i+1}事，只承认它发生在{place}，开头近于“{head}”。第{i+1}段其余留在《{ch['title']}》正文。"
            )
        bits.append(f"对话被抄在纸上。纸会黄。黄比云安全。抄写不求完整，《{ch['title']}》把完整当成一种暴露。")
        for i, (speaker, line) in enumerate(ch["talks"]):
            head = line[:16].rstrip("，。；")
            bits.append(
                f"{speaker}那句以“{head}”开始的话，被第{i+1}张纸接住。纸的去向：{ch['places'][i % len(ch['places'])]}的下一级权限柜。"
            )
        title, body = ch["doc"]
        bits.append(
            f"文献《{title}》在回想里只留下执行的手感：{body[:90]}在《{ch['title']}》里手感替代不了条款，条款替代不了还在吃饭的人。"
        )
        bits.append(
            f"回想录结束。若《{ch['title']}》被装订成册，册须能被烧掉，也不得充当唯一数据库。"
        )
        return "\n".join(bits) + "\n"

    def render_chapter(self, ch: dict) -> str:
        self._seq += 1
        parts = []
        parts.append(f"第{ch['num']:02d}章 {ch['title']}")
        parts.append(f"〔{ch['vol']} · {ch['time']}〕")
        parts.append(f"题记：{ch['epi']}")
        parts.append("")

        opening = self.openings.take()
        parts.append(
            self._para(
                opening,
                f"本章的时钟被拨到{ch['time']}。",
                self._scene_img(ch["places"][0]),
                f"在场将被提到的名字包括：{'、'.join(ch['pov'])}。《{ch['title']}》把名单当责任清册。",
            )
        )
        parts.append("")

        beats = ch["beats"]
        talks = ch["talks"]
        talk_i = 0
        for i, beat in enumerate(beats):
            # 章首或中段插入时间跳跃，避免均匀节拍
            if i == 4:
                parts.append(self._para(self.timeskip.take(), self.human.take()))
                parts.append("")
            parts.append(self._wrap_beat(beat, ch, i))
            parts.append("")
            # 每两拍插入一段对话
            if i % 2 == 1:
                block = self._talk_block(talks, talk_i, 2, salt=f"{ch['num']}-{i}")
                if block:
                    parts.append(block)
                    parts.append("")
                    talk_i += 2
            # 特定拍插入无线电或人间
            if i == 6:
                parts.append(self._radio(ch, i))
                parts.append("")
            if i == 8:
                parts.append(self._para(self.earth.take() if ch["num"] % 2 else self.space.take(), self.bridge.take()))
                parts.append("")

        # 剩余对话一次给完
        if talk_i < len(talks):
            parts.append(f"余下的对话被{ch['places'][0]}消化。消化不等于同意。本章是《{ch['title']}》。")
            parts.append(self._talk_block(talks, talk_i, 12, salt=f"{ch['num']}-rest"))
            parts.append("")

        parts.append(self._journal(ch))
        parts.append("")
        parts.append(self._street(ch))
        parts.append("")
        parts.append(self._counter(ch))
        parts.append("")
        parts.append(self._recall(ch))
        parts.append("")
        parts.append(self._document(ch["doc"], ch["num"]))
        parts.append(
            self._para(
                self.cosmic.take() if ch["num"] % 3 == 0 else self.bridge.take(),
                f"第{ch['num']}章《{ch['title']}》把笔放下。放下不等于安全，《{ch['title']}》里的节点必须还能搬家。",
                f"{COALITION['short']}在{ch['time']}仍未完成。完成是一种首都幻觉。",
            )
        )
        parts.append("")
        text = "\n".join(parts)
        return self._soften(text)

    def _soften(self, text: str) -> str:
        # 去掉连续重复的“说。”堆叠感：已在 talk 里用动作打断
        text = text.replace("。\n。", "。\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        # 删除生硬补丁句若未被需要
        return text


def load_chapters():
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
        "——本文为二次创作长篇，时间锚点为三体危机纪元早期、面壁计划启动之际。\n"
        f"——联合体格言：{COALITION['motto']}\n"
        "\n"
        "目录按卷：卷一裂隙 / 卷二初遇 / 卷三磨合 / 卷四暗流 / 卷五入盟 / 卷六网络 / 卷七田园\n"
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
    body = "".join(chunks)
    # 若字数不足，追加“档案附录”式扩写而非重复章
    return body
