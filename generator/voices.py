# -*- coding: utf-8 -*-
"""人物声口：真正进入台词包装与 POV 旁白，禁止全员同一书面腔。"""

from __future__ import annotations

try:
    from .lore import (
        ANTONIOS,
        EARTH,
        EMPIRE,
        ENDFIELD,
        JUPITER,
        MCU,
        NORMA,
        PANGU,
        THUNDER,
    )
except ImportError:
    from lore import (
        ANTONIOS,
        EARTH,
        EMPIRE,
        ENDFIELD,
        JUPITER,
        MCU,
        NORMA,
        PANGU,
        THUNDER,
    )


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


ALIASES = {
    "托尼": MCU["tony"],
    "斯塔克": MCU["tony"],
    "Tony": MCU["tony"],
    "班纳": MCU["banner"],
    "布鲁斯": MCU["banner"],
    "Banner": MCU["banner"],
    "彼得": MCU["peter"],
    "帕克": MCU["peter"],
    "史蒂夫": MCU["steve"],
    "罗杰斯": MCU["steve"],
    "美国队长": MCU["steve"],
    "索尔": MCU["thor"],
    "火箭浣熊": MCU["rocket"],
    "星云": MCU["nebula"],
    "斯科特": MCU["scott"],
    "霍普": MCU["hope"],
    "罗迪": MCU["rhodey"],
    "罗德斯": MCU["rhodey"],
    "克林特": MCU["clint"],
    "佩珀": MCU["pepper"],
    "罗辑": EARTH["luo"],
    "老罗": EARTH["luo"],
    "史强": EARTH["shi"],
    "大史": EARTH["shi"],
    "萨伊": EARTH["say"],
    "伽尔宁": EARTH["garanin"],
    "丁仪": EARTH["ding"],
    "常伟思": EARTH["chang"],
    "章北海": EARTH["zhang"],
    "维德": EARTH["wade"],
    "托马斯·维德": EARTH["wade"],
    "汪淼": EARTH["wang"],
    "泰勒": EARTH["tyler"],
    "弗雷德里克·泰勒": EARTH["tyler"],
    "雷迪亚兹": EARTH["diaz"],
    "曼努尔·雷迪亚兹": EARTH["diaz"],
    "希恩斯": EARTH["hines"],
    "比尔·希恩斯": EARTH["hines"],
    "佩丽卡": ENDFIELD["perlica"],
    "管理员": ENDFIELD["admin"],
    "陈千语": ENDFIELD["chen"],
    "伊冯": ENDFIELD["yvonne"],
    "莱万汀": ENDFIELD["laev"],
    "菲奥娜": ENDFIELD["fiona"],
    "莱恩·凯": ANTONIOS["ceo"],
    "莱恩": ANTONIOS["ceo"],
    "玛尔塔·诺瓦克": NORMA["director"],
    "玛尔塔": NORMA["director"],
    "奥列格·贝洛": NORMA["fleet_master"],
    "纪若木": PANGU["engineer"],
    "霍炎": THUNDER["chief"],
    "赫尔曼·瓦格纳": JUPITER["chair"],
    "赫尔曼": JUPITER["chair"],
    "奥古斯丁·楚希罗": EMPIRE["emperor"],
    "奥古斯丁": EMPIRE["emperor"],
    "皇帝": EMPIRE["emperor"],
    "艾琳娜·沃斯": EMPIRE["envoy"],
    "艾琳娜": EMPIRE["envoy"],
    "伊根·霍尔": EMPIRE["academy_chief"],
    "马尔科·维克托": EMPIRE["admiral"],
    "维克托": EMPIRE["admiral"],
    "执政官": "三体执政官",
}


# 台词后的声口标签：同一角色多条轮换，结构互不相同。
TAGS = {
    MCU["tony"]: [
        "托尼把这句话扔出去，翻译耳机才开始追。",
        "托尼说。嘲讽在前，数据在后，中间没有给礼貌留座位。",
        "托尼用下巴点了点空气，像在给一个不存在的董事会散会。",
        "斯塔克先生的语速让记录员只记下关键词，关键词还带火星。",
    ],
    MCU["banner"]: [
        "班纳说，先把边界说完，才肯把结论轻轻放下。",
        "班纳补了一句限定条件，好像怕绝对化会在空气里结晶。",
        "布鲁斯把声音放得很慢，慢是为了让自己也不被肾上腺素签字。",
    ],
    MCU["peter"]: [
        "彼得说，句尾还挂着一个没来得及问出口的问题。",
        "彼得下意识叫了一声斯塔克先生，随即把称呼咽回去一半。",
        "帕克的语速比恐惧快，比答案更快。",
    ],
    MCU["steve"]: [
        "史蒂夫说。原则先落地，策略在门口排队。",
        "罗杰斯不多解释头衔，头衔在他句子里显得像多余勋章。",
        "史蒂夫把声音压平，平得像一条不肯弯的线。",
    ],
    MCU["thor"]: [
        "索尔说，句法仍带雷的余韵，却努力把雷收进房间。",
        "索尔直呼其事，像对待一场本该在旷野举行的宴会。",
    ],
    MCU["rocket"]: [
        "火箭说。脏话和公差挤在同一句里，谁也没资格先走。",
        "火箭骂完对方，又骂了一下螺丝的规格，螺丝没有顶嘴。",
    ],
    MCU["nebula"]: [
        "星云说。只有威胁被陈述，情绪不配进入情报。",
        "星云的句子短，短到只剩可以射击的部分。",
    ],
    MCU["scott"]: [
        "斯科特确认自己没听错，才把这句话放出牙缝。",
        "斯科特说，普通人的喘气声还挂在句首。",
    ],
    MCU["hope"]: [
        "霍普纠正了空气里刚冒头的烂比喻，然后才回答正题。",
        "霍普说。实验室纪律比安慰先到。",
    ],
    MCU["rhodey"]: [
        "罗德斯把托尼的笑话收回去，重新包装成简报。",
        "罗迪说。军人的翻译功能在这一秒比装甲更忙。",
    ],
    MCU["clint"]: [
        "克林特说。大词被他留在门外，像把弓卸了弦。",
        "克林特的句子短，短得像父亲在厨房里交代明天谁去接孩子。",
    ],
    MCU["pepper"]: [
        "佩珀说。公司与家庭同时在线，她先问托尼睡过没有。",
        "佩珀把日程和人心叠在同一句话里，谁也不许掉线。",
    ],
    EARTH["luo"]: [
        "罗辑说，轻得像在抱怨旅馆空调，重的部分藏在反问里。",
        "罗辑先把自己放进麻烦里，才允许文明大事靠过来。",
        "罗辑反问完，自己先皱眉，仿佛嫌这问题太像演说。",
        "罗辑把壮语拆成琐事：琐事才不容易被做成广播。",
    ],
    EARTH["shi"]: [
        "史强说。烟在句子中间断了一截。",
        "大史不喊头衔，外号比职务先到场。",
        "史强把话砸在桌上，像把一份口供按指纹。",
    ],
    EARTH["say"]: [
        "萨伊说。外交辞令里有钢，钢不敲杯子也会响。",
        "秘书长把句子铺得很完整，完整是为了不留可被割让的缝。",
        "萨伊的停顿经过训练，停顿本身也是主权。",
    ],
    EARTH["garanin"]: [
        "伽尔宁把发言权切成片段，片段才开得完会。",
        "伽尔宁说。主持是一种把火药分成小包的技术。",
    ],
    EARTH["ding"]: [
        "丁仪说，对定理客气，对活人刻薄，酒气在两者之间。",
        "丁仪把杯子当标点，标点比发言更诚实。",
    ],
    EARTH["chang"]: [
        "常伟思先报职务，再给判断，判断短得像命令的影子。",
        "常伟思说。军语不负责安慰。",
    ],
    EARTH["zhang"]: [
        "章北海问得平静，平静比吼更吓人。",
        "章北海说。政委的问句不给虚假的乐观留座位。",
    ],
    EARTH["wade"]: [
        "维德说。代价不解释，前进两个字自己带着血。",
        "托马斯·维德的句子短，短到只剩方向。",
    ],
    EARTH["wang"]: [
        "汪淼先报数量级，再肯让感情靠近材料。",
        "汪淼说。精度比口号更像他的母语。",
    ],
    EARTH["tyler"]: [
        "泰勒说。意志和幽灵仍在他的词汇里巡逻。",
        "泰勒把非常规战争说成唯一还没被偷看光的房间。",
    ],
    EARTH["diaz"]: [
        "雷迪亚兹说。民选的热度还在喉咙里燃烧。",
        "雷迪亚兹把同归于尽也说成一种谈判，谈判桌因此发烫。",
    ],
    EARTH["hines"]: [
        "希恩斯说得温柔，温柔里有把信念写成工程的牙。",
        "希恩斯把大脑说成可以施工的现场，现场让旁人脊背发凉。",
    ],
    ENDFIELD["perlica"]: [
        "佩丽卡先把流程说完，才把人情轻轻搁在附录。",
        "佩丽卡说。监督不是冷，是不肯让自动化自己当神。",
    ],
    ENDFIELD["admin"]: [
        "管理员说。指令句，很少自称。",
        "管理员的句子像开关：开、关、红线，没有抒情。",
    ],
    ENDFIELD["chen"]: [
        "陈千语说。剑和工业可以出现在同一句，热而直。",
        "陈千语不绕弯，弯会被当成延误。",
    ],
    ENDFIELD["yvonne"]: [
        "伊冯先报误差，冷幽默才被允许进门。",
        "伊冯说。笑话带着校准过的小数点。",
    ],
    ENDFIELD["laev"]: [
        "莱万汀说。少解释，多到位，熔火留在动作里。",
        "莱万汀的句子短，短到只剩抵达。",
    ],
    ENDFIELD["fiona"]: [
        "菲奥娜把频道、信号、可信度排成一行，然后才给结论。",
        "菲奥娜说。情报分析不负责鼓舞士气。",
    ],
    ANTONIOS["ceo"]: [
        "莱恩·凯说。先生们三个字把退路温和地切断。",
        "莱恩把赔付说得像礼貌，礼貌后面是清算。",
    ],
    NORMA["director"]: [
        "玛尔塔先问补给窗口，理想排在冗余之后。",
        "玛尔塔·诺瓦克说。航线比旗帜先被喂饱。",
    ],
    NORMA["fleet_master"]: [
        "奥列格报吨位、泊位、曲率窗口，像在念一张不会撒谎的表。",
        "舰队总监的句子里没有诗，诗装不进货柜。",
    ],
    PANGU["engineer"]: [
        "纪若木说。失修比击沉更致命，这句话他可以重复到船坞报废。",
        "纪若木把船坞的固执放进音节，音节叮当作响。",
    ],
    THUNDER["chief"]: [
        "霍炎说。可维护性不是漂亮，是还能再出击。",
        "霍炎把回收两个字咬得很死，死过一次的系统才配活。",
    ],
    JUPITER["chair"]: [
        "赫尔曼把接口与曲率认证说成船厂的祈祷。",
        "瓦格纳说。签字栏比演说区更大。",
    ],
    EMPIRE["emperor"]: [
        "奥古斯丁说，像把负担放在典礼的托盘上，托盘必须端稳。",
        "皇帝把人民两个字说得比臣民更重，重是他给自己上的锁。",
        "奥古斯丁的长句不是华丽，是不肯把责任说短。",
    ],
    EMPIRE["envoy"]: [
        "艾琳娜说。枢密院的平稳下面是联合，不是吞并。",
        "艾琳娜·沃斯把纹章留着，把征服从词典里拿开。",
    ],
    EMPIRE["academy_chief"]: [
        "伊根·霍尔把单点故障说成比敌人更近的羞辱。",
        "科学院首席要求分散，分散是信仰也是工程。",
    ],
    EMPIRE["admiral"]: [
        "维克托说。情感是变量，变量要进射表才会被承认。",
        "马尔科把舰队效率放在所有抒情前面。",
    ],
    "智子": [
        "智子说。没有停顿，也没有为人类准备的语气。",
        "智子把风险、监听、低熵体排列出来，排列本身就是思维。",
        "智子的句子平，平得像一张不肯起皱的膜。",
    ],
    "三体执政官": [
        "执政官说。集体决定，句子里不出现计谋一词。",
        "三体执政官把生存说成会议的唯一合法主语。",
        "思维海洋里的声音叠在一起，听上去仍像一个。",
    ],
}


INTERIORS = {
    MCU["tony"]: [
        "他在心里给这场面起了个不该公开的外号，外号比战略简报先完成。",
        "装甲不在身上时，嘲讽就是他唯一还合身的外壳。",
        "他计算了一下谁会先破产：自己的耐心，还是翻译的词汇表。",
    ],
    MCU["banner"]: [
        "他先在内部划出不可逆的边界，边界比勇气更先被需要。",
        "绝对化的句子在他舌尖发苦，他把它改成概率。",
    ],
    MCU["peter"]: [
        "他想问的问题比房间里的军官还多，他只放出了最不像小孩的一个。",
        "尺度在他眼睛里同时变大变小，像纽约和宇宙抢同一副眼镜。",
    ],
    MCU["steve"]: [
        "他不喜欢把人当成棋子，棋盘却已经铺到轨道上。",
        "原则在他胸口发沉，沉是因为它还没被策略稀释。",
    ],
    EARTH["luo"]: [
        "他把这件事先说成自己今晚睡不着，睡不着才有资格想文明。",
        "反问在舌尖转了一圈，他咽回去，怕问句也是一种广播。",
        "壮丽的词让他恶心，恶心有时是理智还活着的证据。",
        "他觉得自己仍像走错门的人，走错门的人反而能看见门框。",
    ],
    EARTH["shi"]: [
        "他在人群里找手和包，不找象征。象征不会在胡同里安炸弹。",
        "头衔越响，他越想去看下水道。",
        "他给这局面起了个难听的外号，外号不进会议纪要，进他的烟。",
    ],
    EARTH["say"]: [
        "她把主权想象成一张还没被抽走的桌子，桌子必须留在地球。",
        "她在选词，选词是为了让后人无法说：那天我们把签字权卖了。",
    ],
    EARTH["ding"]: [
        "他刻薄不是为了出风头，是为了不让年轻人把未知当酒。",
        "公式不在了，酒还在。他讨厌这种替代。",
    ],
    EARTH["wang"]: [
        "数量级先于恐惧到达。恐惧没有单位，他偏要给它找一个。",
        "材料比宣言听话，也比宣言容易裂。",
    ],
    EARTH["zhang"]: [
        "失败主义在他心里不是情绪，是一种仓储算法：蛋要分篮。",
        "他问自己的问题不给别人听，别人的乐观太亮。",
    ],
    EARTH["chang"]: [
        "职务是他的护栏。护栏之外，他允许自己短暂地怕。",
    ],
    EARTH["wade"]: [
        "前进在他字典里没有反义词。反义词会被当成投降。",
    ],
    ENDFIELD["perlica"]: [
        "她把伦理开关想象成必须被多人同时看见的红灯，红灯不是装饰。",
        "自动化一旦被跪拜，就会变成另一种侵蚀。",
    ],
    ENDFIELD["admin"]: [
        "指令在内部排列。排列完成前，不需要自我。",
    ],
    ENDFIELD["chen"]: [
        "热意往前冲，冲到红线才停。红线不是怕，是还想让人住在后面。",
    ],
    ANTONIOS["ceo"]: [
        "他在估违约金。违约金能让某些人比道德更快学会停火。",
    ],
    NORMA["director"]: [
        "肚子会先于意识形态造反。她先喂航线。",
    ],
    PANGU["engineer"]: [
        "他听见的不是史诗，是螺栓的疲劳。疲劳比敌人诚实。",
    ],
    THUNDER["chief"]: [
        "不能修的胜利在他看来等于失败提前到场。",
    ],
    EMPIRE["emperor"]: [
        "典礼是外壳。外壳下面是他必须把流亡说成仍对人民负责。",
        "三条旋臂不在了，负担还在。负担不认星图。",
    ],
    EMPIRE["envoy"]: [
        "她把联合放在吞并前面，像把刀放回鞘，鞘仍是武器的一部分。",
    ],
    EMPIRE["admiral"]: [
        "情感若不能进射表，就不配指挥他的分钟。",
    ],
    "智子": [
        "思维是透明的。不透明的变量像镜子，镜子让光第一次排队。",
        "低熵体增加。模型需要新的项。项尚未命名，于是恐惧有了形状。",
        "监视出现延迟。延迟对质子计算机是一种接近羞辱的天气。",
    ],
    "三体执政官": [
        "生存仍是唯一合法的主语。主语下面开始长出无法合并的从句。",
        "计谋这个词被禁止，于是他们把犹豫叫作会议。",
    ],
}


LEAD_INS = {
    MCU["tony"]: "托尼用一句不该出现在正式记录里的比喻给现场测温。",
    MCU["banner"]: "班纳先确认这件事还没有越过不可逆的线。",
    MCU["peter"]: "彼得把眼睛睁大，尺度在瞳孔里对撞。",
    MCU["steve"]: "史蒂夫站得像一条原则，原则暂时还没有座位。",
    EARTH["luo"]: "罗辑把场面降级成私人麻烦，降级之后才敢看它。",
    EARTH["shi"]: "史强不看旗，看手。",
    EARTH["say"]: "萨伊把桌子当成还没被征用的地球。",
    EARTH["ding"]: "丁仪用酒杯的重量核对这句话配不配进物理。",
    EARTH["wang"]: "汪淼先找单位，找不到单位的恐惧让他更烦。",
    EARTH["zhang"]: "章北海把乐观从句子里摘掉，再听剩下的事实。",
    ENDFIELD["perlica"]: "佩丽卡先找开关，再听理想。",
    ENDFIELD["admin"]: "管理员把现场折叠成可执行的指令序列。",
    ANTONIOS["ceo"]: "莱恩·凯在心里先开了一张违约金的草稿。",
    NORMA["director"]: "玛尔塔先数窗口，窗口比演讲短。",
    PANGU["engineer"]: "纪若木听螺栓，不听号角。",
    EMPIRE["emperor"]: "奥古斯丁把负担端正，像端正一顶没有国土的冠。",
    EMPIRE["envoy"]: "艾琳娜把纹章留在可见处，把征服留在不可见处。",
    "智子": "智子的观察没有镜头感，只有覆盖与覆盖失败。",
    "三体执政官": "执政官们的思维叠浪，浪尖上只准出现生存。",
}


ASIDES = {
    MCU["tony"]: "他在心里说：这要是电影，剪辑师已经该喊卡；可惜宇宙没有卡。",
    MCU["banner"]: "他在心里加了一条脚注：以上判断在新数据到来前失效。",
    MCU["peter"]: "他在心里把斯塔克先生换成自己，又立刻觉得太狂。",
    MCU["steve"]: "他在心里把勋章翻到背面，背面没有口号。",
    EARTH["luo"]: "他在心里说：别把这句写进会发光的地方。",
    EARTH["shi"]: "他在心里给每个人起外号，外号比档案难伪造。",
    EARTH["say"]: "她在心里核对：这句话会不会在明天变成割让。",
    EARTH["ding"]: "他在心里骂了一句年轻人和宇宙，骂完对定理道歉。",
    ENDFIELD["perlica"]: "她在心里把掌声改成检查清单。",
    "智子": "延迟被记录。记录本身成为新的风险项。",
    "三体执政官": "会议没有计谋，只有尚未合并的生存定义。",
    EMPIRE["emperor"]: "他在心里把人民二字又读了一遍，读给没有三条旋臂的自己。",
}


def canon(name: str) -> str:
    if name in STYLES:
        return name
    if name in ALIASES:
        return ALIASES[name]
    for key in STYLES:
        if name and (name in key or key.endswith(name) or name.endswith(key)):
            return key
    return name


def style(name: str) -> dict:
    return STYLES.get(canon(name), {"len": "medium", "tone": "中性", "habit": "职务"})


def tags_for(name: str) -> list[str]:
    return TAGS.get(canon(name), [])


def interior(name: str, idx: int = 0) -> str:
    pool = INTERIORS.get(canon(name), [])
    if not pool:
        st = style(name)
        return f"{name}以{st['tone']}把这件事按自己的习惯按住：{st['habit']}。"
    return pool[idx % len(pool)]


def lead_in(name: str) -> str:
    return LEAD_INS.get(canon(name), f"{name}把注意力放到还能执行的那一层。")


def aside(name: str) -> str:
    return ASIDES.get(canon(name), f"{name}把未说出口的部分留在权限柜外。")


def speech_tag(name: str, idx: int = 0) -> str:
    pool = tags_for(name)
    if pool:
        return pool[idx % len(pool)]
    st = style(name)
    return f"{name}说。口吻偏{st['tone']}，习惯仍是{st['habit']}。"


def wrap_line(name: str, line: str, idx: int = 0) -> str:
    """把一句台词接上该角色的声口，而不是统一写成「」X说。"""
    tag = speech_tag(name, idx)
    st = style(name)
    kind = st["len"]
    if kind == "flat":
        return f"「{line}」{tag}"
    if kind == "fast":
        return f"「{line}」{tag}"
    if kind == "short":
        return f"{tag}「{line}」"
    if kind == "grand":
        return f"{tag}「{line}」"
    if kind == "careful":
        return f"{tag}「{line}」"
    return f"「{line}」{tag}"
