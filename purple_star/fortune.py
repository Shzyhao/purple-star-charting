"""运势曲线：大限 + 流年综合评分（自撰规则，供参考）。"""

from . import strength
from .chart import ganzhi_index, gz_of_year, liunian
from .consts import to_simp

WEIGHT_PALACE = {"命宮": 1.0, "財帛": 0.8, "官祿": 0.8, "遷移": 0.6, "夫妻": 0.6, "福德": 0.5, "田宅": 0.5, "疾厄": 0.5}
HUA_SCORE = {"祿": 2.0, "權": 1.0, "科": 0.8, "忌": -2.0}


def _palace_of_zhi(ch, zhi):
    mapping = ch.get("palace_by_zhi")
    if mapping is not None:
        return mapping.get(zhi)
    for p, v in ch["palaces"].items():
        if v["zhi"] == zhi:
            return p
    return None


def daxian_score(ch, age):
    for z, d in ch["daxian"].items():
        if d["from"] <= age <= d["to"]:
            p = _palace_of_zhi(ch, z)
            st = strength.palace_strength(ch, p)
            base = st["avg"] if st["avg"] is not None else 0.0
            hua = ch.get("daxian_sihua", {}).get(z, {})
            bonus = 0.0
            for h, star in (hua.get("hua") or {}).items():
                for p2, info in ch["palaces"].items():
                    if star in info["stars"]:
                        bonus += HUA_SCORE[h] * WEIGHT_PALACE.get(p2, 0.3)
                        break
            return {
                "palace": p,
                "zhi": z,
                "from": d["from"],
                "to": d["to"],
                "base": round(base, 2),
                "hua": round(bonus, 2),
                "score": round(base * 0.6 + bonus * 0.4, 2),
            }
    return None


def liunian_score(ch, year):
    age = (ganzhi_index(gz_of_year(year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1
    ln = liunian(ch, gz_of_year(year), age)
    lp = _palace_of_zhi(ch, ln["ming"])
    st = strength.palace_strength(ch, lp)
    base = st["avg"] if st["avg"] is not None else 0.0
    bonus = 0.0
    for h, star in ln["hua"].items():
        for p2, info in ch["palaces"].items():
            if star in info["stars"]:
                bonus += HUA_SCORE[h] * WEIGHT_PALACE.get(p2, 0.3)
                break
    return {
        "age": age,
        "palace": lp,
        "zhi": ln["ming"],
        "hua": ln["hua"],
        "base": round(base, 2),
        "hua_score": round(bonus, 2),
        "score": round(base * 0.5 + bonus * 0.5, 2),
    }


def grade(score):
    if score >= 1.5:
        return "顺"
    if score >= 0.5:
        return "偏顺"
    if score > -0.5:
        return "平"
    if score > -1.5:
        return "偏弱"
    return "弱"


def curve_md(ch, start, end):
    lines = [
        "## 运势曲线（%d-%d）" % (start, end),
        "",
        "| 年份 | 虚岁 | 大限宫 | 大限分 | 流年命宫 | 流年分 | 综合 | 评级 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for y in range(start, end + 1):
        dx = daxian_score(ch, (ganzhi_index(gz_of_year(y)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1)
        ln = liunian_score(ch, y)
        total = round((dx["score"] + ln["score"]) / 2, 2) if dx else ln["score"]
        lines.append(
            "| %d | %d | %s | %+.2f | %s | %+.2f | %+.2f | %s |"
            % (
                y,
                ln["age"],
                to_simp(dx["palace"]) if dx else "—",
                dx["score"] if dx else 0.0,
                to_simp(ln["palace"]),
                ln["score"],
                total,
                grade(total),
            )
        )
    lines.append("")
    lines.append("> 评分基于强弱（五行生克）+ 四化落宫加权，为项目自撰规则，仅供趋势参考。")
    return "\n".join(lines)
