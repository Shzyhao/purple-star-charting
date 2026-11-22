"""专题：姻缘、事业、财运、健康（自撰规则，不含原文；不涉寿命）。"""

from .consts import PALACES, to_simp
from .interpret import STAR_TEXT

MAIN = ("紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍")
SHA = ("擎羊", "陀羅", "火星", "鈴星", "地空", "地劫", "天刑")
LASHA = ("擎羊", "陀羅")


def _stars(ch, pname):
    return ch["palaces"][pname]["stars"]


def _main(ch, pname):
    return [s for s in _stars(ch, pname) if s in MAIN]


def _hua_of(ch, star):
    return ch["hua"].get(star, "")


def _palace_of(ch, star):
    for pname in PALACES:
        if star in _stars(ch, pname):
            return pname
    return None


def _side_palace(ch, pname, offset):
    order = PALACES
    i = order.index(pname)
    return order[(i + offset) % 12]


def marriage(ch, ln=None):
    out = []
    A = out.append
    A("## 姻缘专题")
    A("")
    q = _main(ch, "夫妻")
    A("- 夫妻宫主星：%s。" % ("、".join(to_simp(s) for s in q) or "空宫（借对宫看）"))
    for s in q:
        t = STAR_TEXT.get(s)
        if t:
            A("  - %s：%s" % (to_simp(s), t["xing"]))
    qs = _stars(ch, "夫妻")
    if any(s in qs for s in ("紅鸞", "天喜")):
        A("- 夫妻宫见红鸾或天喜，传统上主婚喜之兆，感情机会较多。")
    shas = [s for s in qs if s in SHA]
    if shas:
        A("- 夫妻宫见煞星（%s），感情易有波折、拖延或聚少离多，宜晚婚、重沟通。" % "、".join(to_simp(s) for s in shas))
    tri = set(_stars(ch, "夫妻")) | set(_stars(ch, "官祿")) | set(_stars(ch, "遷移")) | set(_stars(ch, "福德"))
    if "紅鸞" in tri or "天喜" in tri:
        A("- 夫妻宫三方四正见红鸾或天喜，婚喜信号更强。")
    for s in q:
        h = _hua_of(ch, s)
        if h in ("祿", "權", "科"):
            A("- 夫妻宫主星化%s：婚姻方面得助或有名声。" % h)
        if h == "忌":
            A("- 夫妻宫主星化忌：感情方面需多包容，易有牵挂与压力。")
    if ln:
        A("")
        A(
            "- 流年 %s：流年四化落夫妻宫：%s"
            % (
                ln["year_gz"],
                "、".join("%s化%s" % (x["star"], h) for h, x in ln["hua_loc"].items() if x["palace"] == "夫妻") or "无",
            )
        )
        qz = [x for h, x in ln["hua_loc"].items() if x["palace"] == "夫妻"]
        if qz:
            A("  - 流年有能量进入夫妻宫，感情主题活跃，但吉凶要看星曜与煞星。")
    A("")
    A("- 建议：看对象是否成熟、是否愿意沟通，比看年龄和命盘更重要；晚婚往往更稳。")
    A("")
    A("> 姻缘分析属传统术数倾向性描述，不构成婚配建议。")
    return "\n".join(out)


def career(ch, ln=None):
    out = []
    A = out.append
    A("## 事业专题")
    A("")
    ming = _main(ch, "命宮")
    A("- 命宫主星：%s。" % ("、".join(to_simp(s) for s in ming) or "空宫"))
    if any(s in ("天機", "太陰", "天同", "天梁") for s in ming) or "機月同梁" in "".join(to_simp(s) for s in ming):
        A('  - 偏"机月同梁"型：适合稳定体系、专业技术、文职、顾问、教育与研究类工作。')
    if any(s in ("七殺", "破軍", "貪狼") for s in ming):
        A('  - 偏"杀破狼"型：适合开创、业务、竞争性行业，宜有平台与团队支撑。')
    if any(s in ("天府", "天相") for s in ming):
        A('  - 偏"府相"型：稳健、善于管理与协调，适合体制内或大型组织。')
    if any(s in ("太陽", "紫微") for s in ming):
        A("  - 主星带贵气：适合公职、管理、品牌、需要名声的行业。")
    g = _main(ch, "官祿")
    A("- 官禄宫主星：%s。" % ("、".join(to_simp(s) for s in g) or "空宫（借对宫看）"))
    for s in g:
        h = _hua_of(ch, s)
        if h in ("祿", "權", "科", "忌"):
            A(
                "  - 官禄宫主星化%s，事业上%s。"
                % (h, {"祿": "多机会与资源", "權": "有主导权也有压力", "科": "重名声与文书", "忌": "多变动与阻碍"}[h])
            )
    if ch["daxian"]:
        A("- 大限：%s起限，每十年一宫，可对照事业阶段。" % ch["ju"])
    A("")
    A('- 建议：把命盘当"性格与节奏参考"，职业选择仍以能力、兴趣与市场为准。')
    A("")
    A("> 事业分析属传统术数倾向性描述，不构成职业建议。")
    return "\n".join(out)


def wealth(ch, ln=None):
    out = []
    A = out.append
    A("## 财运专题")
    A("")
    cai = _stars(ch, "財帛")
    A("- 财帛宫星曜：%s。" % ("、".join(to_simp(s) for s in cai) or "空宫"))
    for s in _main(ch, "財帛"):
        h = _hua_of(ch, s)
        if h:
            A(
                "  - %s化%s：%s"
                % (
                    to_simp(s),
                    h,
                    {"祿": "财路顺、有进项", "權": "理财主导、压力大", "科": "靠名声文书得财", "忌": "易破耗或纠纷"}[h],
                )
            )
    if "祿存" in cai:
        A("- 财帛宫见禄存：主积蓄力，宜稳健理财。")
    if any(s in cai for s in ("擎羊", "陀羅", "地空", "地劫", "火星", "鈴星")):
        A("- 财帛宫见煞：钱财起伏较大，忌投机与担保，宜留现金流。")
    tz = _main(ch, "田宅")
    A("- 田宅宫主星：%s。" % ("、".join(to_simp(s) for s in tz) or "空宫"))
    A("- 建议：先看赚钱方式（专业/口才/投资），再看守财能力（禄存、田宅、化忌位置）。")
    A("")
    A("> 财运分析属传统术数倾向性描述，不构成投资建议。")
    return "\n".join(out)


HEALTH_MAP = {
    "紫微": "脾胃、头部",
    "天機": "肝胆、神经",
    "太陽": "眼目、心血管",
    "武曲": "呼吸、牙齿",
    "天同": "脾胃、消化",
    "廉貞": "血液、心血管、妇科",
    "天府": "脾胃、代谢",
    "太陰": "肾、泌尿、妇科",
    "貪狼": "肝胆、泌尿、内分泌",
    "巨門": "肠胃、口腔",
    "天相": "皮肤、泌尿",
    "天梁": "慢性病、脾胃",
    "七殺": "呼吸、外伤",
    "破軍": "肾、泌尿",
}


def health(ch, ln=None):
    out = []
    A = out.append
    A("## 健康专题（非医学建议）")
    A("")
    jie = _main(ch, "疾厄")
    A("- 疾厄宫主星：%s。" % ("、".join(to_simp(s) for s in jie) or "空宫"))
    for s in jie:
        if s in HEALTH_MAP:
            A("  - %s：传统上留意 %s。" % (to_simp(s), HEALTH_MAP[s]))
    if any(s in _stars(ch, "疾厄") for s in SHA):
        A("- 疾厄宫见煞：注意外伤、炎症或慢性问题，宜定期体检。")
    A("- 福德宫（情绪与精神）：%s。" % ("、".join(to_simp(s) for s in _stars(ch, "福德")) or "空宫"))
    A("- 建议：规律作息、体检、情绪管理；有症状看医生，不要用命盘代替医学判断。")
    A("")
    A("> 健康专题仅为传统术数文化描述，不构成诊断或医疗建议。")
    return "\n".join(out)


def study(ch, ln=None):
    out = []
    A = out.append
    A("## 学业专题（考试/进修）")
    A("")
    ming = _main(ch, "命宮")
    A("- 命宫主星：%s。" % ("、".join(to_simp(x) for x in ming) or "空宫"))
    stars_all = set()
    for pn in ("命宮", "官祿", "父母"):
        stars_all |= set(_stars(ch, pn))
    if {"文昌", "文曲"} & stars_all:
        A("- 命/官/父母宫见文昌或文曲：考运与文书方面有助力。")
    if "化科" in "".join(_hua_of(ch, s) for s in stars_all):
        A("- 见化科：考试、评审类事项有利。")
    if any(s in stars_all for s in ("擎羊", "陀羅", "地空", "地劫")):
        A("- 见煞星：考试易有临场波动，需多准备。")
    A("- 建议：把命盘当作息与心态参考，备考仍以计划与练习为主。")
    A("")
    A("> 学业分析属传统术数倾向性描述，不构成升学建议。")
    return "\n".join(out)


def children(ch, ln=None):
    out = []
    A = out.append
    A("## 子女专题")
    A("")
    A("- 子女宫主星：%s。" % ("、".join(to_simp(x) for x in _main(ch, "子女")) or "空宫（借对宫）"))
    for s in _main(ch, "子女"):
        h = _hua_of(ch, s)
        if h:
            A("  - %s化%s" % (to_simp(s), h))
    A("- 建议：亲子关系重沟通与陪伴，命盘只作性格差异参考。")
    A("")
    A("> 子女分析属传统术数倾向性描述，不构成育儿建议。")
    return "\n".join(out)


def parents(ch, ln=None):
    out = []
    A = out.append
    A("## 父母/长辈专题")
    A("")
    A("- 父母宫主星：%s。" % ("、".join(to_simp(x) for x in _main(ch, "父母")) or "空宫（借对宫）"))
    for s in _main(ch, "父母"):
        h = _hua_of(ch, s)
        if h:
            A("  - %s化%s" % (to_simp(s), h))
    A("- 建议：与长辈的相处以界限与尊重为先。")
    A("")
    A("> 父母分析属传统术数倾向性描述，不构成家庭建议。")
    return "\n".join(out)


def travel(ch, ln=None):
    out = []
    A = out.append
    A("## 迁移/出国专题")
    A("")
    A("- 迁移宫星曜：%s。" % ("、".join(to_simp(x) for x in _stars(ch, "遷移")) or "空宫"))
    if "天馬" in _stars(ch, "遷移"):
        A("- 迁移宫见天马：外出、异地发展机会较多。")
    if any(s in _stars(ch, "遷移") for s in ("擎羊", "陀羅", "火星", "鈴星")):
        A("- 迁移宫见煞：出行注意安全与突发状况。")
    A("- 建议：出国/迁居以现实条件（签证、工作、家庭）为准。")
    A("")
    A("> 迁移分析属传统术数倾向性描述，不构成出行建议。")
    return "\n".join(out)


def partnership(ch, ln=None):
    out = []
    A = out.append
    A("## 合伙/合作专题")
    A("")
    A("- 兄弟宫（合伙）：%s。" % ("、".join(to_simp(x) for x in _stars(ch, "兄弟")) or "空宫"))
    A("- 奴仆宫（团队）：%s。" % ("、".join(to_simp(x) for x in _stars(ch, "奴僕")) or "空宫"))
    if any(s in _stars(ch, "兄弟") + _stars(ch, "奴僕") for s in ("擎羊", "陀羅", "火星", "鈴星", "地空", "地劫")):
        A("- 兄弟/奴仆宫见煞：合伙易有分歧，建议事先约定权责与退出机制。")
    A("- 建议：合作看契约与信任，命盘只作相处风格参考。")
    A("")
    A("> 合伙分析属传统术数倾向性描述，不构成商业建议。")
    return "\n".join(out)


def legal(ch, ln=None):
    out = []
    A = out.append
    A("## 官非/合同专题")
    A("")
    A("- 官禄宫星曜：%s。" % ("、".join(to_simp(x) for x in _stars(ch, "官祿")) or "空宫"))
    A("- 田宅宫（合同/房产）：%s。" % ("、".join(to_simp(x) for x in _stars(ch, "田宅")) or "空宫"))
    for s in _stars(ch, "官祿") + _stars(ch, "田宅"):
        if s in ("擎羊", "陀羅", "天刑", "地空", "地劫", "火星", "鈴星"):
            A("- 见%s：合同、文书、官非类事项宜谨慎。" % to_simp(s))
    A("- 建议：涉及签约、诉讼请咨询专业人士；命盘不作法律判断。")
    A("")
    A("> 官非分析属传统术数倾向性描述，不构成法律建议。")
    return "\n".join(out)


TOPICS = {
    "marriage": marriage,
    "career": career,
    "wealth": wealth,
    "health": health,
    "study": study,
    "children": children,
    "parents": parents,
    "travel": travel,
    "partnership": partnership,
    "legal": legal,
}


def analyze_topic(name, ch, ln=None):
    fn = TOPICS.get(name)
    if not fn:
        raise ValueError("unknown topic: " + name)
    return fn(ch, ln)
