"""星曜强弱：五行生克法（自撰规则，不依赖任何版本庙旺表）。

说明：传统庙旺落陷表因版本与整理成果差异，本项目不内置该表；
这里用公开的五行生克关系推得生 / 比和 / 耗 / 泄 / 受制五级强弱，
属于本项目的规则实现，可解释、可复现，也不涉及任何原文。
用户如自带庙旺表，可通过 load_miaowang() 以 JSON 方式加载（见 docs/data/miaowang-schema.md）。
"""

import json

# 十四主星与常用辅星的五行（依据传统星曜五行，属事实性规则）
STAR_ELEMENT = {
    "紫微": ("土",),
    "天機": ("木",),
    "太陽": ("火",),
    "武曲": ("金",),
    "天同": ("水", "金"),
    "廉貞": ("火",),
    "天府": ("土",),
    "太陰": ("水",),
    "貪狼": ("水", "木"),
    "巨門": ("水",),
    "天相": ("水",),
    "天梁": ("土",),
    "七殺": ("火", "金"),
    "破軍": ("水",),
    "文昌": ("金",),
    "文曲": ("水",),
    "左輔": ("土",),
    "右弼": ("水",),
    "天魁": ("火",),
    "天鉞": ("火",),
    "祿存": ("土",),
    "天馬": ("火",),
    "擎羊": ("金",),
    "陀羅": ("金",),
    "火星": ("火",),
    "鈴星": ("火",),
    "地空": ("火",),
    "地劫": ("火",),
}
# 十二地支五行
PALACE_ELEMENT = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
REL_SCORE = {"宮生星": 2.0, "比和": 1.0, "星克宮": 0.0, "星生宮": -1.0, "宮克星": -2.0}

MAIN_STARS = (
    "紫微",
    "天機",
    "太陽",
    "武曲",
    "天同",
    "廉貞",
    "天府",
    "太陰",
    "貪狼",
    "巨門",
    "天相",
    "天梁",
    "七殺",
    "破軍",
)
JI_STARS = ("文昌", "文曲", "左輔", "右弼", "天魁", "天鉞", "祿存", "天馬")
SHA_STARS = ("擎羊", "陀羅", "火星", "鈴星", "地空", "地劫")

MIAOWANG_GRADE_SCORE = {"廟": 3.0, "旺": 2.0, "得地": 1.0, "利盆": 0.5, "平和": 0.0, "不得地": -1.0, "陷": -2.0}


def relation(star_el, palace_el):
    if star_el == palace_el:
        return "比和"
    if SHENG[palace_el] == star_el:
        return "宮生星"
    if SHENG[star_el] == palace_el:
        return "星生宮"
    if KE[star_el] == palace_el:
        return "星克宮"
    if KE[palace_el] == star_el:
        return "宮克星"
    return "比和"


def star_score(star, palace_zhi):
    """单星在某地支宫位的五行强弱分（多五行取平均）。"""
    els = STAR_ELEMENT.get(star)
    if not els:
        return None
    pel = PALACE_ELEMENT.get(palace_zhi)
    if not pel:
        return None
    scores = [REL_SCORE[relation(e, pel)] for e in els]
    return sum(scores) / len(scores)


def level_of(score):
    if score is None:
        return ""
    if score >= 1.5:
        return "强"
    if score >= 0.5:
        return "偏强"
    if score > -0.5:
        return "平"
    if score > -1.5:
        return "偏弱"
    return "弱"


def palace_strength(ch, palace_name):
    info = ch["palaces"][palace_name]
    zhi = info["zhi"]
    rows = []
    main_scores = []
    for s in info["stars"]:
        sc = star_score(s, zhi)
        if sc is None:
            continue
        rows.append(
            {"star": s, "score": sc, "level": level_of(sc), "rel": relation(STAR_ELEMENT[s][0], PALACE_ELEMENT[zhi])}
        )
        if s in MAIN_STARS:
            main_scores.append(sc)
    avg = round(sum(main_scores) / len(main_scores), 2) if main_scores else None
    return {
        "palace": palace_name,
        "zhi": zhi,
        "rows": rows,
        "avg": avg,
        "level": level_of(avg),
        "has_main": bool(main_scores),
    }


def sanfang(ch):
    """三方四正（命、财帛、官禄、迁移）强弱与吉煞统计。"""
    names = ("命宮", "財帛", "官祿", "遷移")
    stats = [palace_strength(ch, n) for n in names]
    vals = [s["avg"] for s in stats if s["avg"] is not None]
    avg = round(sum(vals) / len(vals), 2) if vals else None
    ji = set()
    sha = set()
    for n in names:
        for s in ch["palaces"][n]["stars"]:
            if s in JI_STARS:
                ji.add(s)
            if s in SHA_STARS:
                sha.add(s)
    return {"stats": stats, "avg": avg, "level": level_of(avg), "ji": sorted(ji), "sha": sorted(sha)}


def load_miaowang(path):
    """加载用户自备的传统庙旺表（可选）。

    格式：{"星曜": {"子": "廟", "丑": "旺", ...}, ...}
    返回 dict；文件不存在或格式异常时返回 {}。
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def miaowang_grade(table, star, zhi):
    if not table:
        return None
    val = table.get(star, {}).get(zhi)
    if val is None:
        return None
    return val if val in MIAOWANG_GRADE_SCORE else None
