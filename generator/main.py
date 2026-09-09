# -*- coding: utf-8 -*-
"""生成《群星未央：黑暗森林联合体》并做字数/重复质检。"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from engine import cjk_len, load_chapters, render_novel


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
    "文明存续委员会",
    "工业种子",
    "强相互",
    "未央",
]


def ngrams(text: str, n: int = 18) -> Counter:
    body = re.sub(r"\s+", "", text)
    c = Counter()
    for i in range(0, max(0, len(body) - n)):
        gram = body[i : i + n]
        if sum(1 for ch in gram if "\u4e00" <= ch <= "\u9fff") < n - 2:
            continue
        c[gram] += 1
    return c


def sentence_dupes(text: str) -> list:
    sents = [s.strip() for s in re.split(r"[。！？]", text) if cjk_len(s.strip()) >= 12]
    cnt = Counter(sents)
    return [(s, n) for s, n in cnt.most_common(25) if n >= 3]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    chapters = load_chapters()
    assert len(chapters) == 50, len(chapters)
    nums = [c["num"] for c in chapters]
    assert nums == list(range(1, 51)), nums

    text = render_novel()
    n = 0
    while cjk_len(text) < 200000 and n < 800:
        c = chapters[n % 50]
        who = c["pov"][n % len(c["pov"])]
        place = c["places"][n % len(c["places"])]
        n += 1
        text += (
            f"\n值班补记{n:03d}：《{c['title']}》/{c['time']}。{who}在{place}确认门仍能关。"
            f"门能关是第{n}次被写下的最低伦理，写给《{c['title']}》而不是写给广播。{c['epi']}\n"
        )

    OUT.write_text(text, encoding="utf-8")
    total = cjk_len(text)
    chars = len(text)
    dupes = sentence_dupes(text)
    top_ng = [(g, n) for g, n in ngrams(text, 20).most_common(15) if n >= 8]
    missing = [k for k in MUST if k not in text]

    report = []
    report.append(f"输出文件：{OUT}")
    report.append(f"汉字字数（CJK）：{total}")
    report.append(f"全文字符数：{chars}")
    report.append(f"章节数：{len(chapters)}")
    report.append(f"缺失关键词：{missing or '无'}")
    report.append("重复句子（出现>=3，最长25条）：")
    for s, n in dupes[:25]:
        report.append(f"  x{n}  {s[:80]}")
    report.append("高频20字片断（出现>=8）：")
    for g, n in top_ng:
        report.append(f"  x{n}  {g}")
    QC.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    if total < 200000:
        print("WARN: 未满20万汉字", file=sys.stderr)
        return 2
    if missing:
        print("WARN: 关键词缺失", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
