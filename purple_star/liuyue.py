"""流月与流日：以斗君起正月，顺行；流日从流月命宫起初一顺行。"""

from .chart import add, gz_of_year
from .consts import GAN, SIHUA, ZHI, ZHI_IDX, to_simp

MONTH_STAR = ("祿", "權", "科", "忌")


def month_gz(year_gan, month_no):
    yin = {"甲": 2, "己": 2, "乙": 4, "庚": 4, "丙": 6, "辛": 6, "丁": 8, "壬": 8, "戊": 0, "癸": 0}[year_gan]
    return GAN[(yin + (month_no - 1)) % 10] + ZHI[(2 + (month_no - 1)) % 12]


def doujun(ch):
    yz = ch["year_ganzhi"][1]
    return add(add(yz, -(ch["input"]["lunar_month"] - 1)), ZHI.index(ch["input"]["hour"][0]))


def liuyue_table(ch, year):
    """返回某流年 12 个农历月的流月命宫、月干支、四化落宫。"""
    year_gz = gz_of_year(year)
    dj = doujun(ch)
    rows = []
    for m in range(1, 13):
        z = ZHI[(ZHI_IDX[dj] + (m - 1)) % 12]
        mgz = month_gz(year_gz[0], m)
        hua = SIHUA.get(mgz[0], {})
        loc = {}
        for h, star in hua.items():
            for pname, info in ch["palaces"].items():
                if star in info["stars"]:
                    loc[h] = {"star": star, "palace": pname}
                    break
        pname = ch.get("palace_by_zhi", {}).get(z) or [k for k, v in ch["palaces"].items() if v["zhi"] == z][0]
        rows.append(
            {"month": m, "palace": pname, "zhi": z, "gz": mgz, "stars": ch["palaces"][pname]["stars"], "hua": loc}
        )
    return {"year": year, "year_gz": year_gz, "doujun": dj, "rows": rows}


def liuyue_md(ch, year):
    t = liuyue_table(ch, year)
    out = ["## 流月（%d %s）" % (year, t["year_gz"]), "", "斗君（正月）：%s宫" % t["doujun"], ""]
    out.append("| 农历月 | 月干支 | 流月命宫 | 星曜 | 月四化落宫 |")
    out.append("|---|---|---|---|---|")
    for r in t["rows"]:
        hua = "；".join("%s化%s→%s" % (r["gz"][0], h, to_simp(x["palace"])) for h, x in r["hua"].items())
        out.append(
            "| %d月 | %s | %s（%s） | %s | %s |"
            % (
                r["month"],
                r["gz"],
                to_simp(r["palace"]),
                r["zhi"],
                "、".join(to_simp(s) for s in r["stars"]) or "空宫",
                hua,
            )
        )
    out.append("")
    out.append("> 流月推法在古籍中较简略，可靠性有限，仅作时间窗口参考。")
    return "\n".join(out)


def liuri(ch, year, lunar_month, lunar_day):
    t = liuyue_table(ch, year)
    row = t["rows"][lunar_month - 1]
    z = ZHI[(ZHI_IDX[row["zhi"]] + (lunar_day - 1)) % 12]
    pname = [k for k, v in ch["palaces"].items() if v["zhi"] == z][0]
    return {
        "year": year,
        "year_gz": t["year_gz"],
        "month": row,
        "day_zhi": z,
        "day_palace": pname,
        "stars": ch["palaces"][pname]["stars"],
    }


def liuri_md(ch, year, lunar_month, lunar_day):
    d = liuri(ch, year, lunar_month, lunar_day)
    m = d["month"]
    out = [
        "## 流日（%d %s，农历%d月%d日）" % (year, d["year_gz"], lunar_month, lunar_day),
        "",
        "- 流月命宫：%s（%s），月干支 %s" % (to_simp(m["palace"]), m["zhi"], m["gz"]),
        "- 流日命宫：%s（%s）" % (to_simp(d["day_palace"]), d["day_zhi"]),
        "- 当日星曜：%s" % ("、".join(to_simp(s) for s in d["stars"]) or "空宫"),
        "",
        "> 流日推法可靠性最低，仅供日程安排参考，不宜用于重大决定。",
    ]
    return "\n".join(out)
