# -*- coding: utf-8 -*-
"""章节数据结构。剧情核产出 Chapter，引擎只负责渲染。"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Chapter:
    num: int
    title: str
    vol: str
    time: str
    epi: str
    pov: list[str]
    places: list[str]
    beats: list[str]
    talks: list
    doc: tuple
    sides: Optional[list[str]] = None
    lens: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        if not d.get("sides"):
            d.pop("sides", None)
        if not d.get("lens"):
            d.pop("lens", None)
        return d
