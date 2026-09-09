# -*- coding: utf-8 -*-
"""设定检索库：专有名词、机构、舰船、人物与技术。小说生成器只从此处取名，避免写飘。"""

EMPIRE = {
    "name": "神圣群星帝国",
    "capital_system": "星空皇冠星系",
    "capital": "圣凯旋城",
    "old_names": ("南冕座Ω星系", "新卢泰西亚城"),
    "slogan": "向着永恒的群星前进",
    "founder": "安德鲁·楚希罗",
    "first_consul": "库恩·楚希罗",
    "emperor": "奥古斯丁·楚希罗",
    "privy": "皇家枢密院",
    "academy": "帝国皇家科学院",
    "mil_academy": "帝国皇家军事科学院",
    "academy_chief": "伊根·霍尔",
    "college": "圣家族学院",
    "military_school": "圣凯旋军事学院",
    "guard": "楚国皇家禁卫军",
    "eros": "埃罗斯卫队",
    "victor": "维克托军团",
    "legions": [
        "第一凯旋军团",
        "第十装甲军团",
        "第一海王星军团",
        "第二十二初创军团",
        "第一星序军团",
        "第二星序兵团",
        "第十七星序兵团",
        "幸运者军团",
        "第十三合组军团",
    ],
    "ships": {
        "invincible": "无敌号",
        "invincible_class": "无敌级战列舰",
        "trafalgar": "特拉法加级旗舰",
        "rock": "磐石级帝国要塞舰",
        "warspite": "止战级攻坚战列舰",
        "boreas": "凛冽级防御驱逐舰",
        "pallas": "帕拉斯元帅",
        "eros_court": "埃罗斯王庭",
    },
    "tech": [
        "拉格朗日星门",
        "空间种子",
        "空间振荡器",
        "曲率航行",
        "曲率蛙跳",
        "第四代智能控制核心",
        "分散集群智能微芯片",
    ],
    "houses": ["楚西罗家族", "庞氏家族", "崔顿家族", "杜布瓦家族", "第十三家族"],
    "envoy": "艾琳娜·沃斯",
    "admiral": "马尔科·维克托",
}

ANTONIOS = {
    "name": "安东尼奥斯财团",
    "hq": "安东塔斯城",
    "planet": "花园星",
    "system": "花园星系",
    "ceo": "莱恩·凯",
    "marshal": "巴利达·克拉克斯",
    "economist": "凯恩斯·陈",
    "captain": "帕尔默·劳埃德",
    "axis": "安东尼奥斯巨轴",
    "subs": ["罗安与卡利莱恩太空机械公司", "安氏精密科技公司"],
    "ships": ["南十字星元帅级武装航空母舰", "新君士坦丁大帝级综合战列巡洋舰", "圣安德鲁号"],
}

NORMA = {
    "name": "诺玛运输集团",
    "hq": "贝洛伯格城",
    "system": "科雷戈星系",
    "director": "玛尔塔·诺瓦克",
    "fleet_master": "奥列格·贝洛",
    "ships": [
        "太阳鲸级武装战略航空母舰",
        "乌拉诺斯之矛级重型战列巡洋舰",
        "普鲁图斯之盾级防护战列巡洋舰",
        "奇美拉级重型巡洋舰",
    ],
}

JUPITER = {
    "name": "木星工业",
    "origin": "木星舰船制作厂与金乌能源集团",
    "chair": "赫尔曼·瓦格纳",
    "ships": ["ST59级防御战列巡洋舰", "艾奥级高速离子炮巡洋舰", "CV3000级快速航空母舰"],
}

THUNDER = {
    "name": "雷火科技",
    "chief": "霍炎",
    "ships": ["雷火之辉无人机航空母舰", "雷火之星综合武库舰", "灼热级重炮突击舰"],
    "system": "辉光回收维修系统",
}

PANGU = {
    "name": "盘古重工",
    "group": "盘古拓展与开发",
    "hq": "特提斯城",
    "system": "比邻星系",
    "engineer": "纪若木",
    "ships": ["玉衡级维修巡洋舰", "天枢级支援航空母舰", "天权级战列巡洋舰"],
    "plan": "补天计划",
    "ammo": "溶解弹",
    "armor": "一次性维修装甲",
}

ENDFIELD = {
    "org": "终末地工业",
    "dept": "协议回收部门",
    "ship": "帝江号",
    "aic": "自动化集成工业系统",
    "pac": "协议锚点核心",
    "admin": "管理员",
    "perlica": "佩丽卡",
    "chen": "陈千语",
    "yvonne": "伊冯",
    "laev": "莱万汀",
    "fiona": "菲奥娜",
    "andrei": "安德烈",
    "m3": "M3",
    "lifeng": "黎风",
    "estella": "埃特拉",
    "xaihi": "赛希",
    "avw": "艾维文娜",
    "zhuang": "庄方宜",
    "dapan": "大潘",
    "qiuli": "秋栗",
    "world": "塔卫二",
    "valley": "四号谷地",
    "tech": ["协议源石", "协议传送", "源石可控分布", "息壤", "超域"],
}

MCU = {
    "tony": "托尼·斯塔克",
    "banner": "布鲁斯·班纳",
    "peter": "彼得·帕克",
    "steve": "史蒂夫·罗杰斯",
    "thor": "索尔",
    "clint": "克林特·巴顿",
    "rhodey": "詹姆斯·罗德斯",
    "rocket": "火箭",
    "nebula": "星云",
    "scott": "斯科特·朗",
    "hope": "霍普·凡·戴因",
    "pepper": "佩珀·波茨",
    "happy": "快乐·霍根",
    "armor": "马克85",
    "ai": "星期五",
    "tech": ["纳米机械", "方舟反应堆", "量子领域", "皮姆粒子", "时间导航"],
}

EARTH = {
    "pdc": "行星防御理事会",
    "un": "联合国",
    "say": "萨伊",
    "garanin": "伽尔宁",
    "luo": "罗辑",
    "shi": "史强",
    "chang": "常伟思",
    "ding": "丁仪",
    "wang": "汪淼",
    "ye": "叶文洁",
    "yang": "杨冬",
    "zhang": "章北海",
    "wu": "吴岳",
    "wade": "托马斯·维德",
    "zhuangyan": "庄颜",
    "tyler": "弗雷德里克·泰勒",
    "diaz": "曼努尔·雷迪亚兹",
    "hines": "比尔·希恩斯",
    "eto": "地球三体组织",
    "pia": "PIA",
}

TRISOLARIS = {
    "name": "三体文明",
    "sophon": "智子",
    "droplet": "水滴",
    "fleet": "三体第一舰队",
    "listener": "监听员",
    "sim": "强相互作用力材料",
    "foil": "二向箔",
    "photoid": "光粒",
    "singer": "歌者",
}

COALITION = {
    "full": "未央—太阳系文明联合体",
    "short": "联合体",
    "parliament": "文明联合议会",
    "council": "文明存续委员会",
    "institute": "基础宇宙结构研究院",
    "motto": "文明不应因被看见而获罪，宇宙也不应因文明的恐惧而死去。",
    "garden": "田园时代工程",
    "seed": "星际工业种子",
    "evac": "维度灾难撤离协议",
}

ALL_FACTIONS = [
    EMPIRE["name"],
    ANTONIOS["name"],
    NORMA["name"],
    JUPITER["name"],
    THUNDER["name"],
    PANGU["name"],
    ENDFIELD["org"],
    "地球人类文明",
    TRISOLARIS["name"],
    "复仇者及相关技术团队",
]
