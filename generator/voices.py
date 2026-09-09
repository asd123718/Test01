# -*- coding: utf-8 -*-
"""人物声口。对话组织必须按角色差异，禁止全员同一书面腔。"""

from lore import EARTH, MCU, ENDFIELD, EMPIRE, ANTONIOS, NORMA, PANGU, THUNDER, JUPITER


STYLES = {
    EARTH["luo"]: {"len": "medium", "tone": "先轻后重，爱反问，厌壮语", "habit": "把文明大事说成个人麻烦"},
    EARTH["shi"]: {"len": "short", "tone": "市井刑侦", "habit": "外号，不喊头衔"},
    EARTH["say"]: {"len": "long", "tone": "外交辞令藏钢", "habit": "秘书长腔"},
    EARTH["garanin"]: {"len": "medium", "tone": "会议主持", "habit": "把发言权切成片段"},
    EARTH["ding"]: {"len": "medium", "tone": "酒与公式", "habit": "对年轻人刻薄，对定理客气"},
    EARTH["chang"]: {"len": "short", "tone": "军语", "habit": "先职务后判断"},
    EARTH["zhang"]: {"len": "medium", "tone": "平静得吓人", "habit": "政委问句"},
    EARTH["wade"]: {"len": "short", "tone": "命令", "habit": "不解释代价"},
    EARTH["wang"]: {"len": "medium", "tone": "材料精度", "habit": "先数量级"},
    EARTH["tyler"]: {"len": "medium", "tone": "非常规战争", "habit": "幽灵、意志"},
    EARTH["diaz"]: {"len": "medium", "tone": "燃烧的民选腔", "habit": "同归于尽也是谈判"},
    EARTH["hines"]: {"len": "long", "tone": "温柔的脑科学", "habit": "信念可工程化"},
    MCU["tony"]: {"len": "fast", "tone": "嘲讽作装甲", "habit": "外号，语速超过翻译"},
    MCU["banner"]: {"len": "careful", "tone": "先边界后结论", "habit": "避免绝对化"},
    MCU["peter"]: {"len": "fast", "tone": "问题比答案多", "habit": "斯塔克先生"},
    MCU["steve"]: {"len": "short", "tone": "原则先于策略", "habit": "少头衔崇拜"},
    MCU["thor"]: {"len": "grand", "tone": "神话句法", "habit": "直呼或称王"},
    MCU["rocket"]: {"len": "short", "tone": "脏话并列公差", "habit": "谁都可能被骂"},
    MCU["nebula"]: {"len": "short", "tone": "情报", "habit": "只陈述威胁"},
    MCU["scott"]: {"len": "medium", "tone": "普通人喘气", "habit": "先确认没听错"},
    MCU["hope"]: {"len": "medium", "tone": "实验室纪律", "habit": "纠正烂比喻"},
    MCU["rhodey"]: {"len": "medium", "tone": "把笑话收回成简报", "habit": "军人翻译托尼"},
    MCU["clint"]: {"len": "short", "tone": "父亲与射手", "habit": "少大词"},
    MCU["pepper"]: {"len": "medium", "tone": "公司与家庭同时在线", "habit": "先问托尼睡没睡"},
    ENDFIELD["perlica"]: {"len": "medium", "tone": "监督", "habit": "流程后人情"},
    ENDFIELD["admin"]: {"len": "short", "tone": "指令句", "habit": "很少自称"},
    ENDFIELD["chen"]: {"len": "fast", "tone": "热而直", "habit": "剑和工业可以同句"},
    ENDFIELD["yvonne"]: {"len": "medium", "tone": "冷幽默", "habit": "先报误差"},
    ENDFIELD["laev"]: {"len": "short", "tone": "熔火", "habit": "少解释，多到位"},
    ENDFIELD["fiona"]: {"len": "medium", "tone": "情报分析", "habit": "频道、信号、可信度"},
    ANTONIOS["ceo"]: {"len": "medium", "tone": "温和切断退路", "habit": "先生们"},
    NORMA["director"]: {"len": "medium", "tone": "窗口与冗余", "habit": "先补给后理想"},
    NORMA["fleet_master"]: {"len": "short", "tone": "航线", "habit": "吨位、泊位、曲率窗口"},
    PANGU["engineer"]: {"len": "medium", "tone": "船坞固执", "habit": "失修比击沉更致命"},
    THUNDER["chief"]: {"len": "short", "tone": "可维护性", "habit": "回收再出击"},
    JUPITER["chair"]: {"len": "medium", "tone": "船厂认证", "habit": "接口与曲率"},
    EMPIRE["emperor"]: {"len": "long", "tone": "典礼与负担", "habit": "人民，而非臣民"},
    EMPIRE["envoy"]: {"len": "medium", "tone": "枢密院平稳", "habit": "联合而非吞并"},
    EMPIRE["academy_chief"]: {"len": "medium", "tone": "反单点故障", "habit": "分散集群"},
    EMPIRE["admiral"]: {"len": "short", "tone": "舰队效率", "habit": "情感是变量"},
    "智子": {"len": "flat", "tone": "透明思维", "habit": "风险、监听、低熵体"},
    "三体执政官": {"len": "flat", "tone": "集体决定", "habit": "不使用计谋一词"},
}


def style(name: str) -> dict:
    return STYLES.get(name, {"len": "medium", "tone": "中性", "habit": "职务"})
