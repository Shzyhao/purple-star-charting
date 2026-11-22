# -*- coding: utf-8 -*-
"""择时：按事件类型对流月流日打分（传统术数参考，不构成专业建议）。"""
from .consts import PALACES, to_simp
from . import liuyue, strength

EVENTS = {
    "contract": {"name": "签约/合同", "palaces": ("官祿", "田宅")},
    "interview": {"name": "面试/求职", "palaces": ("官祿", "父母")},
    "travel": {"name": "出行/远行", "palaces": ("遷移",)},
    "date": {"name": "相亲/约会", "palaces": ("夫妻", "福德")},
    "medical": {"name": "就医/检查", "palaces": ("疾厄",)},
    "opening": {"name": "开业/开张", "palaces": ("財帛", "官祿")},
}
JI = ("左輔", "右弼", "文昌", "文曲", "天魁", "天鉞", "祿存", "天喜", "紅鸞")
SHA = ("擎羊", "陀羅", "火星", "鈴星", "地空", "地劫", "天刑")


def score_day(ch, year, lunar_month, lunar_day, event):
    ev = EVENTS[event]
    d = liuyue.liuri(ch, year, lunar_month, lunar_day)
    stars = d["stars"]
    base_palace = [p for p, v in ch["palaces"].items() if v["zhi"] == d["day_zhi"]][0]
    score = 0.0
    reasons = []
    if any(s in stars for s in JI):
        score += 2.0
        reasons.append("吉星")
    if any(s in stars for s in SHA):
        score -= 2.0
        reasons.append("煞星")
    if base_palace in ev["palaces"]:
        score += 2.0
        reasons.append("落事件宫")
    # 流年四化落本命宫位（若在事件宫加分）
    for h, star in ch["hua"].items():
        if star in stars:
            if h in ("祿", "科"):
                score += 1.0
            elif h == "忌":
                score -= 1.0
    return {"day": lunar_day, "zhi": d["day_zhi"], "palace": base_palace,
            "stars": stars, "score": score, "reasons": reasons}


def timing_md(ch, year, lunar_month, event):
    ev = EVENTS[event]
    rows = [score_day(ch, year, lunar_month, d, event) for d in range(1, 31)]
    rows.sort(key=lambda r: (-r["score"], r["day"]))
    out = ["## 择时参考：%s（%d 年农历 %d 月）" % (ev["name"], year, lunar_month), "",
           "| 农历日 | 流日命宫 | 星曜 | 参考分 | 说明 |", "|---|---|---|---|---|"]
    for r in rows[:12]:
        out.append("| %d | %s（%s） | %s | %s | %s |" % (
            r["day"], to_simp(r["palace"]), r["zhi"],
            "、".join(to_simp(s) for s in r["stars"]) or "空宫",
            ("%+.1f" % r["score"]), "、".join(r["reasons"]) or "—"))
    out.append("")
    out.append("> 仅为传统术数参考，不构成签约、医疗、出行等任何专业建议；重大事项请以现实条件为准。")
    return "\n".join(out)
