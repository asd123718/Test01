# -*- coding: utf-8 -*-
"""生成《群星未央：黑暗森林联合体》并做重复/声口/独特词汇率质检。

字数是统计指标，不是硬门槛。禁止值班补记式注水。
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

try:
    from .engine import cjk_len, load_chapters, render_novel
    from . import voices
except ImportError:
    from engine import cjk_len, load_chapters, render_novel
    import voices


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "群星未央：黑暗森林联合体.txt"
QC = ROOT / "output" / "质检报告.txt"

MUST = [
    "神圣群星帝国",
    "安东尼奥斯",
    "诺玛运输",
    "木星工业",
    "雷火科技",
    "盘古",
    "帝江号",
    "佩丽卡",
    "管理员",
    "陈千语",
    "托尼",
    "班纳",
    "彼得",
    "罗辑",
    "智子",
    "黑暗森林",
    "其余势力",
    "未央",
]

FORBIDDEN_SUBSTRINGS = [
    "值班补记",
    "相关新闻当成一种更硬的天气",
    "他们真正关心的是供水、班车、孩子的咳嗽",
    "不进入战略数据库，只进入还能被煮熟的日子",
]

OLD_ENDINGS = [
    "田园立项",
    "光粒与网络",
    "第一滴小宇宙",
]


def ngrams(text: str, n: int = 18) -> Counter:
    body = re.sub(r"\s+", "", text)
    c = Counter()
    limit = max(0, len(body) - n + 1)
    for i in range(limit):
        gram = body[i : i + n]
        if sum(1 for ch in gram if "\u4e00" <= ch <= "\u9fff") < n - 2:
            continue
        c[gram] += 1
    return c


def sentence_dupes(text: str) -> list:
    sents = [s.strip() for s in re.split(r"[。！？]", text) if cjk_len(s.strip()) >= 12]
    cnt = Counter(sents)
    return [(s, n) for s, n in cnt.most_common(25) if n >= 3]


def _skeleton(sent: str) -> str:
    s = sent
    s = re.sub(r"《[^》]+》", "《T》", s)
    s = re.sub(r"第\d+章", "第N章", s)
    s = re.sub(r"第\d+个", "第N个", s)
    s = re.sub(r"第\d+段", "第N段", s)
    s = re.sub(r"\d+", "N", s)
    for name in list(voices.STYLES) + list(voices.ALIASES):
        if name:
            s = s.replace(name, "N")
    s = re.sub(r"[A-Za-z·．.]+", "N", s)
    return s


def isomorphic_paragraphs(text: str) -> list:
    sents = [s.strip() for s in re.split(r"[。！？]", text) if cjk_len(s.strip()) >= 16]
    cnt = Counter(_skeleton(s) for s in sents)
    return [(sk, n) for sk, n in cnt.most_common(20) if n >= 12]


def chapter_unique_ratios(text: str) -> list[tuple[str, float, int]]:
    chunks = re.split(r"\n第\d{2}章 ", text)
    rows = []
    for chunk in chunks[1:]:
        title = chunk.split("\n", 1)[0].strip()[:20]
        body = chunk
        chars = [ch for ch in body if "\u4e00" <= ch <= "\u9fff"]
        if len(chars) < 200:
            continue
        uniq = len(set(chars))
        rows.append((title, uniq / len(chars), len(chars)))
    return rows


def voice_consistency(text: str) -> dict:
    tony_old = len(re.findall(r"「[^」]{8,}」托尼说。", text))
    tony_new = text.count("托尼把这句话扔出去") + text.count("嘲讽在前") + text.count("语速让记录员")
    luo_new = text.count("轻得像在抱怨旅馆空调") + text.count("先把自己放进麻烦") + text.count("把壮语拆成琐事")
    shi_new = text.count("烟在句子中间断了一截") + text.count("外号比职务先到场")
    sophon_new = text.count("没有停顿，也没有为人类准备的语气") + text.count("平得像一张不肯起皱的膜")
    return {
        "托尼旧统一腔出现": tony_old,
        "托尼声口命中": tony_new,
        "罗辑声口命中": luo_new,
        "史强声口命中": shi_new,
        "智子声口命中": sophon_new,
    }


def split_chapters(text: str) -> list[str]:
    return re.findall(r"第\d{2}章 [\s\S]*?(?=第\d{2}章 |\Z)", text)


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    chapters = load_chapters()
    if len(chapters) != 50:
        print(f"ERROR: 章节数 {len(chapters)}，期望 50", file=sys.stderr)
        return 4
    nums = [c["num"] for c in chapters]
    if nums != list(range(1, 51)):
        print(f"ERROR: 章节编号不连续：{nums[:8]}...", file=sys.stderr)
        return 4
    if chapters[-1]["title"] != "其余势力":
        print("ERROR: 终章标题应为「其余势力」", file=sys.stderr)
        return 4
    if any(c["title"] in OLD_ENDINGS for c in chapters):
        print("ERROR: 仍包含旧终局卷章名", file=sys.stderr)
        return 4

    text = render_novel()
    if "值班补记" in text:
        print("ERROR: 正文出现值班补记注水", file=sys.stderr)
        return 5

    OUT.write_text(text, encoding="utf-8")
    total = cjk_len(text)
    chars = len(text)
    dupes = sentence_dupes(text)
    top_ng = [(g, n) for g, n in ngrams(text, 20).most_common(15) if n >= 8]
    missing = [k for k in MUST if k not in text]
    iso = isomorphic_paragraphs(text)
    ratios = chapter_unique_ratios(text)
    voice = voice_consistency(text)
    hot_ng = [(g, n) for g, n in top_ng if n >= 40]
    pad_hits = [s for s in FORBIDDEN_SUBSTRINGS if s in text]

    avg_unique = sum(r[1] for r in ratios) / len(ratios) if ratios else 0
    min_unique = min((r[1] for r in ratios), default=0)

    report = []
    report.append(f"输出文件：{OUT}")
    report.append(f"汉字字数（CJK，统计指标，非硬门槛）：{total}")
    report.append(f"全文字符数：{chars}")
    report.append(f"章节数：{len(chapters)}")
    report.append(f"叙事截止：{chapters[-1]['title']}（{chapters[-1]['time']}）")
    report.append(f"缺失关键词：{missing or '无'}")
    report.append(f"禁用注水模板命中：{pad_hits or '无'}")
    report.append("声口接入抽查：")
    for k, v in voice.items():
        report.append(f"  {k}：{v}")
    report.append(f"章节独特字种比：平均 {avg_unique:.3f}，最低 {min_unique:.3f}")
    report.append("独特字种比最低的五章：")
    for title, ratio, n in sorted(ratios, key=lambda x: x[1])[:5]:
        report.append(f"  {ratio:.3f}  {title}  ({n}字)")
    report.append("重复句子（出现>=3，最长15条）：")
    for s, n in dupes[:15]:
        report.append(f"  x{n}  {s[:80]}")
    report.append("高频20字片断（出现>=8）：")
    for g, n in top_ng:
        report.append(f"  x{n}  {g}")
    report.append("同构句子（骨架出现>=12）：")
    for sk, n in iso[:12]:
        report.append(f"  x{n}  {sk[:80]}")
    QC.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

    if pad_hits:
        print("ERROR: 旧模板残留", file=sys.stderr)
        return 5
    if hot_ng:
        print("ERROR: 存在接近每章一次的模板片断", file=sys.stderr)
        return 6
    if missing:
        print("WARN: 关键词缺失", file=sys.stderr)
        return 3
    if voice["托尼声口命中"] < 3 or voice["罗辑声口命中"] < 3:
        print("WARN: 声口命中偏低", file=sys.stderr)
        return 3
    if total < 90000:
        print("WARN: 汉字偏少，请检查扩写", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
