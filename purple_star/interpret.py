# -*- coding: utf-8 -*-
"""解读层：全部为项目自撰的白话说明，不含任何原文；仅给出页码级引用。"""
from .consts import PALACES, ZHI, PALACES_SIMPLE, to_simp
from . import strength

STAR_TEXT = {
    "紫微": {"hua": "土，帝座，官禄主", "xing": "尊贵、稳重、要强、好面子，有领导欲",
             "ming": "坐命者厚重端庄、志向高远；得辅弼昌曲夹拱则贵，孤君无辅则孤高易受制",
             "xi": "喜左辅右弼、文昌文曲、天魁天钺；忌空劫、羊陀火铃冲破", "page": 18},
    "天機": {"hua": "木，化善，兄弟主", "xing": "机敏、善谋、好动、多变，思虑细密",
             "ming": "坐命者心思灵巧、善策划；庙旺则智谋出众，陷地则多思多虑、进退不定",
             "xi": "喜文昌文曲、天梁；忌羊陀空劫，主奔波劳碌", "page": 20},
    "太陽": {"hua": "火，化贵，官禄主", "xing": "光明、博爱、外向、好施，重名声",
             "ming": "坐命者光明磊落、乐于助人；庙旺则贵显，陷地则劳碌而名大于利",
             "xi": "喜吉星会照；忌空劫羊陀，陷地尤忌", "page": 23},
    "武曲": {"hua": "金，化财，财帛主", "xing": "刚毅、果决、重财、执行力强",
             "ming": "坐命者刚强果决、理财有方；庙旺主财，陷地则辛劳寡合",
             "xi": "喜禄存、天魁天钺；忌擎羊陀罗，主孤克", "page": 24},
    "天同": {"hua": "水金，化福，福德主", "xing": "温和、随和、享受、福气，行动力偏弱",
             "ming": "坐命者温良和顺、有福气；庙旺主安乐，陷地则懒散多劳",
             "xi": "喜吉星扶；忌羊陀空劫，福薄劳碌", "page": 26},
    "廉貞": {"hua": "火，化杀囚，官禄主，次桃花", "xing": "刚烈、才艺、多情、好胜，能吏亦能祸",
             "ming": "坐命者精明强悍、有才艺而多情；庙旺主贵，陷地加煞主刑伤",
             "xi": "喜紫微天府昌曲；忌羊陀火铃，主官非刑伤", "page": 25},
    "天府": {"hua": "土，南斗令星，财帛田宅主", "xing": "稳重、保守、善守、有库藏之象",
             "ming": "坐命者厚重稳健、善守成；庙旺主富足，陷地则平常",
             "xi": "喜禄存昌曲左右；忌空劫羊陀", "page": 22},
    "太陰": {"hua": "水，化富，财帛田宅主", "xing": "温柔、细腻、内敛、重家庭",
             "ming": "坐命者清秀温和、重感情；庙旺主富，陷地则劳心",
             "xi": "喜禄存昌曲；忌火铃空劫，主孤独劳碌", "page": 26},
    "貪狼": {"hua": "水木，化桃花杀，主祸福", "xing": "多才多艺、欲望强、交际广，好动好奇",
             "ming": "坐命者机巧多才、善交际；庙旺主富贵，陷地加煞主淫佚破败",
             "xi": "喜火星铃星、禄存；忌羊陀空劫", "page": 27},
    "巨門": {"hua": "水，化暗，主是非", "xing": "口才、多疑、善辩、好研究，易生是非",
             "ming": "坐命者多思善辩、口才出众；庙旺主富贵，陷地则口舌是非多",
             "xi": "喜太阳禄存；忌羊陀空劫，主刑克", "page": 28},
    "天相": {"hua": "水，化印，官禄主", "xing": "忠厚、谨慎、重服务、善协调",
             "ming": "坐命者忠厚谨慎、有服务心；庙旺主贵，陷地则平凡",
             "xi": "喜紫微天府左右；忌羊陀空劫", "page": 29},
    "天梁": {"hua": "土，化荫，寿星，父母主", "xing": "老成、稳重、有原则、荫庇，喜清高",
             "ming": "坐命者稳重有原则、逢凶化吉；庙旺主寿贵，陷地则孤高",
             "xi": "喜天同昌曲；忌羊陀空劫", "page": 30},
    "七殺": {"hua": "火金，南斗将星，遇帝为权", "xing": "刚猛、果决、独立、冲劲足",
             "ming": "坐命者刚强果断、有开创力；庙旺主权贵，陷地则辛劳刑伤",
             "xi": "喜紫微禄存；忌羊陀火铃空劫", "page": 31},
    "破軍": {"hua": "水，化耗，主夫妻子女", "xing": "破旧立新、敢冲、多变、耗散",
             "ming": "坐命者果敢善变、开创力强；庙旺主富贵，陷地则劳碌破耗",
             "xi": "喜紫微禄存昌曲；忌羊陀空劫", "page": 33},
}
OTHER_TEXT = {
    "左輔": "辅佐贵人，主助力、稳重", "右弼": "辅佐贵人，主助力、圆融",
    "文昌": "文星，主科甲文书", "文曲": "文星，主才艺口才",
    "天魁": "贵人星，主男性长辈助力", "天鉞": "贵人星，主女性长辈助力",
    "祿存": "财禄之星，主积蓄、稳重", "天馬": "驿马，主迁移奔波",
    "擎羊": "刑煞，主刑伤刚烈", "陀羅": "刑煞，主拖延纠缠",
    "火星": "煞星，主急躁突发", "鈴星": "煞星，主暗损急躁",
    "地空": "空亡，主虚耗空想", "地劫": "劫耗，主破耗起伏",
    "紅鸞": "主婚姻喜庆", "天喜": "主喜庆", "天刑": "主刑克自律",
    "天姚": "主桃花风流", "三台": "主贵显助力", "八座": "主贵显",
    "台輔": "主辅弼之贵", "封誥": "主封赠荣典", "天哭": "主忧愁孝服",
    "天虛": "主虚耗", "龍池": "主文雅聪慧", "鳳閣": "主雅致才艺",
}
PALACE_TEXT = {
    "命宮": "本人禀赋、性格、格局与一生大势", "兄弟": "兄弟姊妹、同辈平辈、合伙关系",
    "夫妻": "配偶、婚姻、感情", "子女": "子女、晚辈、学生、下属",
    "財帛": "钱财、收入、理财能力", "疾厄": "健康、疾病、体质",
    "遷移": "外出、远行、在外际遇", "奴僕": "朋友、下属、部属、交友",
    "官祿": "事业、工作、学业、职位", "田宅": "不动产、家宅、家庭环境",
    "福德": "福报、享受、精神生活、兴趣", "父母": "父母、长辈、上级、公家",
}
HUA_TEXT = {"祿": "顺遂、增益、财禄与机会（入何宫，何宫得利）",
            "權": "掌控、主导、压力与责任（入何宫，何宫有力）",
            "科": "名声、文书、贵人、声誉（入何宫，何宫有名）",
            "忌": "阻碍、牵挂、破耗与压力（入何宫，何宫需留意）"}
GEJU = [
    ("君臣慶會", "紫微坐命，左辅右弼文昌文曲天魁天钺会照三方"),
    ("府相朝垣", "天府天相会照命宫三方"),
    ("日月照璧", "太阳太阴分居旺地、会照命宫"),
    ("日月夾命", "太阳太阴夹命宫"),
    ("左右夾命", "左辅右弼夹命宫"),
    ("昌曲夾命", "文昌文曲夹命宫"),
    ("羊陀夾命", "擎羊陀罗夹命宫（凶格）"),
    ("空劫夾命", "地空地劫夹命宫（凶格）"),
    ("火貪格", "贪狼与火星同宫或会照"),
    ("鈴貪格", "贪狼与铃星同宫或会照"),
    ("馬頭帶箭", "命宫在午，擎羊同宫"),
    ("科權祿拱", "化禄化权化科会照命宫三方"),
    ("殺破狼", "七杀破军贪狼会照命宫三方"),
    ("紫府同宮", "紫微天府同宫"),
    ("紫府朝垣", "紫微天府会照命宫三方"),
    ("武貪同行", "武曲贪狼同宫"),
    ("雙祿交流", "禄存与化禄星同会三方"),
    ("祿馬交馳", "禄存与天马同会三方"),
    ("巨日同宮", "巨门太阳同宫"),
    ("陽梁昌祿", "太阳天梁文昌禄存会照三方"),
    ("文星暗拱", "文昌文曲在命宫两侧相夹"),
    ("紫殺同宮", "紫微七杀同宫"),
    ("紫破同宮", "紫微破军同宫"),
    ("廉殺同宮", "廉贞七杀同宫"),
    ("武相同宮", "武曲天相同宫"),
    ("命裡逢空", "地空地劫入命"),
    ("天羅地網", "命宫在辰或戌"),
    ("機月同梁", "天机太阴天同天梁会照三方"),
    ("極向離明", "紫微坐命于午"),
]

MAIN_STARS = ("紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府", "太陰",
              "貪狼", "巨門", "天相", "天梁", "七殺", "破軍")


def _palace_with(ch, *stars):
    for pname in PALACES:
        s = set(_stars(ch, pname))
        if all(x in s for x in stars):
            return pname
    return None


def detect_geju(ch):
    ming = set(_stars(ch, "命宮"))
    tri = _tri(ch)
    flank = _flank(ch)
    res = []
    def pair(a, b):
        return _palace_with(ch, a, b) is not None
    if "紫微" in ming and len({"左輔", "右弼", "文昌", "文曲", "天魁", "天鉞"} & tri) >= 3:
        res.append("君臣慶會")
    if {"天府", "天相"} & ming and len({"天府", "天相"} & tri) >= 2:
        res.append("府相朝垣")
    if {"太陽", "太陰"} <= tri:
        res.append("日月照璧")
    if {"太陽", "太陰"} <= flank:
        res.append("日月夾命")
    if {"左輔", "右弼"} <= flank:
        res.append("左右夾命")
    if {"文昌", "文曲"} <= flank:
        res.append("昌曲夾命")
    if {"擎羊", "陀羅"} <= flank:
        res.append("羊陀夾命")
    if {"地空", "地劫"} <= flank:
        res.append("空劫夾命")
    if "貪狼" in tri and "火星" in tri:
        res.append("火貪格")
    if "貪狼" in tri and "鈴星" in tri:
        res.append("鈴貪格")
    if ch["ming_zhi"] == "午" and "擎羊" in ming:
        res.append("馬頭帶箭")
    if len([x for x in ch["hua"] if x in tri]) >= 3:
        res.append("科權祿拱")
    if {"七殺", "破軍", "貪狼"} <= tri:
        res.append("殺破狼")
    if pair("紫微", "天府"):
        res.append("紫府同宮")
    if {"紫微", "天府"} <= tri and "紫微" not in ming:
        res.append("紫府朝垣")
    if pair("武曲", "貪狼"):
        res.append("武貪同行")
    if "祿存" in tri and any(v in tri for v in ch["hua"].values()):
        res.append("雙祿交流")
    if "祿存" in tri and "天馬" in tri:
        res.append("祿馬交馳")
    if pair("巨門", "太陽"):
        res.append("巨日同宮")
    if {"太陽", "天梁", "文昌", "祿存"} <= tri:
        res.append("陽梁昌祿")
    if {"文昌", "文曲"} <= flank:
        res.append("文星暗拱")
    if pair("紫微", "七殺"):
        res.append("紫殺同宮")
    if pair("紫微", "破軍"):
        res.append("紫破同宮")
    if pair("廉貞", "七殺"):
        res.append("廉殺同宮")
    if pair("武曲", "天相"):
        res.append("武相同宮")
    if {"地空", "地劫"} & ming:
        res.append("命裡逢空")
    if ch["ming_zhi"] in ("辰", "戌"):
        res.append("天羅地網")
    if {"天機", "太陰", "天同", "天梁"} <= tri:
        res.append("機月同梁")
    if "紫微" in ming and ch["ming_zhi"] == "午":
        res.append("極向離明")
    return res


ORDER = ["命宮", "兄弟", "夫妻", "子女", "財帛", "疾厄", "遷移", "奴僕", "官祿", "田宅", "福德", "父母"]


def _stars(ch, pname):
    return ch["palaces"][pname]["stars"]


def _tri(ch):
    out = set()
    for p in ("命宮", "財帛", "官祿", "遷移"):
        out |= set(_stars(ch, p))
    return out


def _flank(ch):
    i = ORDER.index("命宮")
    return set(_stars(ch, ORDER[(i - 1) % 12])) | set(_stars(ch, ORDER[(i + 1) % 12]))


def analyze(ch, ln=None, miaowang=None):
    L = []
    A = L.append
    A("# 紫微斗数命盘解析")
    A("")
    A("> 本报告为紫微斗数排盘与白话解读，属传统术数文化学习用途，不构成任何决策依据。")
    A("")
    A("## 一、基本资料")
    A("")
    A("| 项目 | 内容 |")
    A("|---|---|")
    A("| 性别 | %s（%s） |" % ("男" if ch["male"] else "女", ch["yang_yin"]))
    A("| 生年干支 | %s |" % ch["year_ganzhi"])
    A("| 农历 | %d月%d日 %s |" % (ch["input"]["lunar_month"], ch["input"]["lunar_day"], ch["input"]["hour"]))
    A("| 命宫 | %s宫（%s） |" % (ch["ming_zhi"], ch["ming_gan"]))
    A("| 身宫 | %s宫 |" % ch["shen_zhi"])
    A("| 五行局 | %s |" % ch["ju"])
    A("| 命主 / 身主 | %s / %s |" % (ch["mingzhu"], ch["shenzhu"]))
    A("| 紫微 / 天府 | %s / %s |" % (ch["ziwei"], ch["tianfu"]))
    for n in ch.get("notes", []):
        A("| 备注 | %s |" % n)
    A("")
    A("## 二、十二宫")
    A("")
    A("| 宫位 | 地支 | 星曜 | 强弱(五行) | 身宫 |")
    A("|---|---|---|---|---|")
    for pname in ORDER:
        info = ch["palaces"][pname]
        stars = []
        for s in info["stars"]:
            h = ch["hua"].get(s, "")
            stars.append(s + ("(化" + h + ")" if h else ""))
        ps = strength.palace_strength(ch, pname)
        sl = ("%s(%s)" % (ps["level"], ps["avg"])) if ps["avg"] is not None else "空宫"
        A("| %s | %s | %s | %s | %s |" % (PALACES_SIMPLE.get(pname, pname), info["zhi"], "、".join(to_simp(s) for s in stars) if stars else "（空宫）", sl, "★" if pname == ch["shen_palace"] else ""))
    A("")
    A("## 三、命宫")
    A("")
    ming_stars = _stars(ch, "命宮")
    mains = [s for s in ming_stars if s in STAR_TEXT]
    A("命宫星曜：%s" % ("、".join(to_simp(s) for s in ming_stars) if ming_stars else "（空宫，借对宫看）"))
    A("")
    for s in mains:
        t = STAR_TEXT[s]
        h = ch["hua"].get(s, "")
        A("### %s%s" % (s, "（化" + h + "）" if h else ""))
        A("")
        A("- 星性：%s；%s" % (t["hua"], t["xing"]))
        A("- 坐命：%s" % t["ming"])
        if h:
            A("- 四化：%s 化%s，%s" % (s, h, HUA_TEXT[h]))
        A("- 参见：卷一星曜问答（原书第 %d 页）" % t["page"])
        A("")
    A("身宫在%s：%s。" % (ch["shen_palace"], PALACE_TEXT.get(ch["shen_palace"], "")))
    A("")
    sf = strength.sanfang(ch)
    A("## 四、强弱与三方四正（五行生克法）")
    A("")
    A("> 说明：本工具不内置任何版本的庙旺表；强弱按星曜五行与宫位五行的生克关系推算：宫生星=得生(强)、比和=旺、星克宫=耗、星生宫=泄、宫克星=受制(弱)。")
    A("")
    for st_ in sf["stats"]:
        if st_["avg"] is None:
            A("- %s（%s）：空宫，借对宫看。" % (to_simp(st_["palace"]), st_["zhi"]))
        else:
            A("- %s（%s）：%s（均分 %s），主星：%s" % (
                to_simp(st_["palace"]), st_["zhi"], st_["level"], st_["avg"],
                "、".join("%s%s" % (to_simp(r["star"]), r["level"]) for r in st_["rows"] if r["star"] in strength.MAIN_STARS)))
    A("")
    A("- 三方四正综合：%s（均分 %s）；吉星：%s；煞星：%s。" % (
        sf["level"] or "—", sf["avg"] if sf["avg"] is not None else "—",
        "、".join(to_simp(x) for x in sf["ji"]) or "无",
        "、".join(to_simp(x) for x in sf["sha"]) or "无"))
    if miaowang:
        A("- 已加载用户自备庙旺表：报告中附星曜庙旺等级（仅供参考，不同版本差异较大）。")
    A("")
    A("## 五、十二宫概览")
    A("")
    for pname in ORDER:
        info = ch["palaces"][pname]
        stars = info["stars"]
        ps = strength.palace_strength(ch, pname)
        extra = ("（强弱：%s %s）" % (ps["level"], ps["avg"])) if ps["avg"] is not None else "（空宫）"
        A("- **%s（%s）**：%s —— %s%s" % (pname, info["zhi"], "、".join(to_simp(s) for s in stars) if stars else "空宫", PALACE_TEXT[pname], extra))
        if miaowang:
            grades = []
            for x in stars:
                g = strength.miaowang_grade(miaowang, x, info["zhi"])
                if g:
                    grades.append("%s:%s" % (to_simp(x), g))
            if grades:
                A("  - 庙旺（自备表）：%s" % "、".join(grades))
        for s in stars:
            if s in STAR_TEXT:
                A("  - %s：%s" % (s, STAR_TEXT[s]["xing"]))
    A("")
    A("## 六、格局识别")
    A("")
    gjs = detect_geju(ch)
    if gjs:
        for g in gjs:
            A("- **%s**：%s" % (g, next(x[1] for x in GEJU if x[0] == g)))
    else:
        A("未命中常见吉格/凶格（仅按常见格初筛，非定论）。")
    A("")
    A("## 七、本命四化")
    A("")
    A("生年干（%s）四化：" % ch["year_ganzhi"][0])
    for h in "祿權科忌":
        star = None
        for k, v in ch["hua"].items():
            if v == h:
                star = k
        if not star:
            continue
        loc = [pn for pn in ORDER if star in _stars(ch, pn)]
        A("- 化%s：%s —— %s%s" % (h, star, HUA_TEXT[h], ("；落" + (loc[0] if loc else "?")) if loc else ""))
    A("")
    A("## 八、飞星（宫干四化）")
    A("")
    from . import fly as _fly
    A(_fly.feixing_md(ch, ch.get("sihua_table")))
    A("")
    A("## 九、大限")
    A("")
    A("起运：%s，%s起限。" % (ch["ju"], "顺行" if ch["forward"] else "逆行"))
    A("")
    for z, d in sorted(ch["daxian"].items(), key=lambda kv: kv[1]["from"]):
        pname = [k for k, v in ch["palaces"].items() if v["zhi"] == z][0]
        A("- 第%d限 %d-%d岁：%s（%s宫）" % (d["order"], d["from"], d["to"], pname, z))
    A("")
    if ln:
        A("## 十、流年（%s）" % ln["year_gz"])
        A("")
        A("- 流年命宫：%s宫" % ln["ming"])
        A("- 流年四化：")
        for h in "祿權科忌":
            if h in ln["hua_loc"]:
                x = ln["hua_loc"][h]
                A("  - %s化%s，落本命%s" % (x["star"], h, x["palace"]))
        if "daxian" in ln:
            d = ln["daxian"]
            A("- 当前大限：%d-%d岁（%s宫）" % (d["from"], d["to"], d["zhi"]))
        if "daxian_sihua" in ln and ln["daxian_sihua"].get("hua"):
            A("- 大限四化（%s干）：%s" % (ln["daxian_sihua"]["gan"], "；".join("%s化%s" % (v, k) for k, v in ln["daxian_sihua"]["hua"].items())))
        if "daxian_sihua" in ln and ln["daxian_sihua"].get("stars"):
            ys = ln["daxian_sihua"]["stars"]
            A("- 大限运曜：%s" % "、".join("%s在%s" % (k, v) for k, v in ys.items() if v))
        if "xiaoxian" in ln:
            A("- 小限：%s宫" % ln["xiaoxian"])
        if ln.get("stars"):
            A("- 流年诸星：" + "、".join("%s在%s" % (to_simp(k), v) for k, v in ln["stars"].items()))
        if ln.get("palaces"):
            A("")
            A("### 流年十二宫")
            A("")
            A("| 流年宫位 | 地支 | 本命宫位 | 星曜 |")
            A("|---|---|---|---|")
            for row in ln["palaces"]:
                A("| %s | %s | %s | %s |" % (to_simp(row["palace"]), row["zhi"], to_simp(row["base"]),
                                             "、".join(to_simp(x) for x in row["stars"]) or "空宫"))
        A("")
    A("---")
    A("")
    A("说明：本报告所有解释均为项目自撰白话，不包含古籍原文；页码仅作查考指引。")
    A("命理内容属传统术数文化，仅供学习参考，不构成医疗、投资、法律、婚姻等任何建议。")
    return to_simp("\n".join(L))
