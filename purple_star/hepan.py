# -*- coding: utf-8 -*-
"""合盘：双盘互看（自撰规则，不含原文）。"""
from .consts import PALACES, to_simp, SIHUA, GAN, ZHI

MAIN_STARS = ("紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍")


def _palace_of_star(ch, star):
    for pname in PALACES:
        if star in ch["palaces"][pname]["stars"]:
            return pname
    return None


def _stars(ch, pname):
    return ch["palaces"][pname]["stars"]


def _main(ch, pname):
    return [s for s in _stars(ch, pname) if s in MAIN_STARS]


def _age(ch, target_year):
    from .chart import gz_of_year, ganzhi_index
    return (ganzhi_index(gz_of_year(target_year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1


def _daxian_at(ch, age):
    for z, d in ch["daxian"].items():
        if d["from"] <= age <= d["to"]:
            pname = [k for k, v in ch["palaces"].items() if v["zhi"] == z][0]
            return {"zhi": z, "palace": pname, "from": d["from"], "to": d["to"]}
    return None


def analyze_hepan(a, b, name_a="A", name_b="B", target_year=2026, year_a=None, year_b=None):
    """双盘合看：命宫、夫妻宫互看、四化互落、大限节奏、年龄差。"""
    out = []
    A = out.append
    A("# 合盘分析（%s × %s）" % (name_a, name_b))
    A("")
    A("> 本报告为传统术数体系下的倾向性分析，仅供文化学习参考，不作婚配决定依据。")
    A("")
    A("## 一、双方基本盘")
    A("")
    A("| 项目 | %s | %s |" % (name_a, name_b))
    A("|---|---|---|")
    A("| 性别 | %s | %s |" % ("男" if a["male"] else "女", "男" if b["male"] else "女"))
    A("| 生年 | %s | %s |" % (a["year_ganzhi"], b["year_ganzhi"]))
    A("| 命宫 | %s宫 | %s宫 |" % (a["ming_zhi"], b["ming_zhi"]))
    A("| 身宫 | %s宫 | %s宫 |" % (a["shen_zhi"], b["shen_zhi"]))
    A("| 五行局 | %s | %s |" % (a["ju"], b["ju"]))
    A("| 命宫主星 | %s | %s |" % ("、".join(to_simp(s) for s in _main(a, "命宮")) or "空宫",
                                  "、".join(to_simp(s) for s in _main(b, "命宮")) or "空宫"))
    A("| 夫妻宫主星 | %s | %s |" % ("、".join(to_simp(s) for s in _main(a, "夫妻")) or "空宫",
                                    "、".join(to_simp(s) for s in _main(b, "夫妻")) or "空宫"))
    A("")
    A("## 二、命宫对命宫")
    A("")
    am = _main(a, "命宮")
    bm = _main(b, "命宮")
    common = [s for s in am if s in bm]
    if common:
        A("- 双方命宫同见：%s，性格有相似之处，容易理解彼此，但也容易在同类问题上互不相让。" % "、".join(to_simp(s) for s in common))
    else:
        A("- 双方命宫主星不同（%s / %s），性格互补，需要更多磨合与解释。" % (
            "、".join(to_simp(s) for s in am) or "空宫", "、".join(to_simp(s) for s in bm) or "空宫"))
    A("- %s 命宫在 %s（%s）；%s 命宫在 %s（%s）。" % (name_a, a["ming_zhi"], a["ju"], name_b, b["ming_zhi"], b["ju"]))
    A("")
    A("## 三、夫妻宫互看")
    A("")
    qa = _main(a, "夫妻")
    qb = _main(b, "夫妻")
    A("- %s 夫妻宫主星：%s；%s 命宫主星：%s。" % (name_a, "、".join(to_simp(s) for s in qa) or "空宫", name_b, "、".join(to_simp(s) for s in bm) or "空宫"))
    inter = [s for s in qa if s in bm]
    if inter:
        A("  - 双方在对方夫妻宫的主星（%s）上重合，说明 %s 的婚配倾向与 %s 的气质相近，容易看对眼。" % ("、".join(to_simp(s) for s in inter), name_a, name_b))
    A("- %s 夫妻宫主星：%s；%s 命宫主星：%s。" % (name_b, "、".join(to_simp(s) for s in qb) or "空宫", name_a, "、".join(to_simp(s) for s in am) or "空宫"))
    inter2 = [s for s in qb if s in am]
    if inter2:
        A("  - %s 的婚配倾向与 %s 的气质在 %s 上重合。" % (name_b, name_a, "、".join(to_simp(s) for s in inter2)))
    qa_stars = _stars(a, "夫妻")
    qb_stars = _stars(b, "夫妻")
    for nm, stars in ((name_a, qa_stars), (name_b, qb_stars)):
        shas = [s for s in stars if s in ("擎羊", "陀羅", "火星", "鈴星", "地空", "地劫", "天刑")]
        if shas:
            A("- %s 夫妻宫见煞：%s，感情上易有摩擦、拖延或聚少离多，需多沟通。" % (nm, "、".join(to_simp(s) for s in shas)))
    A("")
    A("## 四、四化互落")
    A("")
    for nm, src, dst in ((name_a, a, b), (name_b, b, a)):
        gan = src["year_ganzhi"][0]
        hua = SIHUA.get(gan, {})
        A("- %s 生年四化（%s干）：" % (nm, gan))
        for h in "祿權科忌":
            star = hua.get(h)
            if not star:
                continue
            pal = _palace_of_star(dst, star)
            MEAN = {"祿": "机会与资源", "權": "主导与压力", "科": "名声与文书贵人", "忌": "压力与牵挂"}
            if pal:
                A("  - 化%s（%s）落对方 %s 宫：把%s带到对方此宫。" % (h, to_simp(star), to_simp(pal), MEAN[h]))
            else:
                A("  - 化%s（%s）：对方盘中未见此星。" % (h, to_simp(star)))
    A("")
    A("## 五、大限节奏")
    A("")
    for nm, ch in ((name_a, a), (name_b, b)):
        age = _age(ch, target_year)
        dx = _daxian_at(ch, age)
        if dx:
            stars = _main(ch, dx["palace"])
            A("- %s：%d 年虚岁 %d，大限在%s宫（%d-%d岁），主星：%s。" % (
                nm, target_year, age, to_simp(dx["palace"]), dx["from"], dx["to"],
                "、".join(to_simp(s) for s in stars) or "空宫"))
    A("- 若一方在婚限、一方在事业限，节奏容易错位，宜提前沟通共同规划。")
    A("")
    A("## 六、年龄差与角色")
    A("")
    diff = (year_b - year_a) if (year_a and year_b) else _year_diff(a, b)
    A("- 两人相差 %d 岁（按出生年计）。" % abs(diff))
    A("- 传统经验里，夫妻宫见天同、天梁者，伴侣偏年长或性格老成；见太阳、巨门者，伴侣个性较强。年龄本身不是问题，\"谁更成熟、谁更让\"才是关键。")
    A("")
    A("## 七、姻缘窗口交集（2026-2031）")
    A("")
    A("| 年份 | %s 信号 | %s 信号 | 交集 |" % (name_a, name_b))
    A("|---|---|---|---|")
    for row in marriage_windows(a, b, target_year or 2026, 6):
        A("| %d | %s | %s | %s |" % (row["year"], row["a"]["score"], row["b"]["score"], row["both"]))
    A("")
    A("> 交集为双方同年信号的较小值，值越高说明双方在该年都更可能有感情主题。")
    A("")
    sync = daxian_sync(a, b, target_year or 2026)
    A("## 八、大限同步度")
    A("")
    if sync["a"]:
        A("- %s：虚岁 %d，大限在%s宫（%s）。" % (name_a, sync["a"]["age"], to_simp(sync["a"]["palace"]), sync["a"]["cat"]))
    if sync["b"]:
        A("- %s：虚岁 %d，大限在%s宫（%s）。" % (name_b, sync["b"]["age"], to_simp(sync["b"]["palace"]), sync["b"]["cat"]))
    A("- 结论：%s。" % ("双方大限主题相近，节奏较同步" if sync["same"] else "双方大限主题不同，节奏容易错位，宜提前沟通共同规划"))
    A("")
    A("## 九、相处建议")
    A("")
    tips = [
        "把\"主导权\"说清楚：一方强、一方慢时，容易积累怨气，定期对齐节奏。",
        "遇煞多的夫妻宫，忌冷战与翻旧账，宜当天说清。",
        "若一方大限在婚限、另一方在事业限，给对方留出各自的时间，而不是强行同步。",
        "不以命盘给关系下结论，现实相处与沟通永远优先。",
    ]
    for t in tips:
        A("- " + t)
    A("")
    A("---")
    A("说明：本报告为项目自撰分析，不含古籍原文；命理内容仅供传统术数文化学习参考，不构成婚姻、法律等任何建议。")
    return "\n".join(out)


def _year_diff(a, b):
    from .chart import ganzhi_index
    return ganzhi_index(b["year_ganzhi"]) - ganzhi_index(a["year_ganzhi"])


def _marriage_score(ch, year):
    """某年该盘的姻缘信号分（自撰规则）。"""
    from .chart import gz_of_year, ganzhi_index, liunian
    age = (ganzhi_index(gz_of_year(year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1
    ln = liunian(ch, gz_of_year(year), age)
    score = 0.0
    notes = []
    for h, x in ln.get("hua_loc", {}).items():
        if x["palace"] == "夫妻":
            if h in ("祿", "科"):
                score += 2.0
            elif h == "忌":
                score -= 2.0
            else:
                score += 1.0
            notes.append("%s化%s入夫妻" % (x["star"], h))
    qz = add = None
    yz = gz_of_year(year)[1]
    qz_zhi = [z for z in "子丑寅卯辰巳午未申酉戌亥"]
    from .consts import ZHI_IDX, ZHI
    qzi = ZHI[(ZHI_IDX[yz] - 2) % 12]
    qpal = [p for p, v in ch["palaces"].items() if v["zhi"] == qzi][0]
    qstars = ch["palaces"][qpal]["stars"]
    if "紅鸞" in qstars or "天喜" in qstars:
        score += 1.0
        notes.append("流年夫妻宫见红鸾天喜")
    for z, d in ch["daxian"].items():
        if d["from"] <= age <= d["to"]:
            dxp = [p for p, v in ch["palaces"].items() if v["zhi"] == z][0]
            if "紅鸞" in ch["palaces"][dxp]["stars"] or "天喜" in ch["palaces"][dxp]["stars"]:
                score += 1.0
                notes.append("大限宫见红鸾天喜")
            break
    return {"year": year, "age": age, "score": round(score, 1), "notes": notes}


def marriage_windows(a, b, start=2026, years=6):
    rows = []
    for y in range(start, start + years):
        sa = _marriage_score(a, y)
        sb = _marriage_score(b, y)
        rows.append({"year": y, "a": sa, "b": sb, "both": round(min(sa["score"], sb["score"]), 1)})
    return rows


def daxian_sync(a, b, year):
    from .chart import gz_of_year, ganzhi_index
    def cat(ch):
        age = (ganzhi_index(gz_of_year(year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1
        for z, d in ch["daxian"].items():
            if d["from"] <= age <= d["to"]:
                p = [k for k, v in ch["palaces"].items() if v["zhi"] == z][0]
                mapping = {"夫妻": "婚限", "子女": "家庭/婚限", "福德": "婚限",
                           "官祿": "事业限", "遷移": "事业限", "財帛": "事业限",
                           "田宅": "家庭限", "父母": "家庭限"}
                return {"age": age, "palace": p, "cat": mapping.get(p, "其他")}
        return None
    ca = cat(a)
    cb = cat(b)
    return {"a": ca, "b": cb, "same": bool(ca and cb and ca["cat"] == cb["cat"])}
