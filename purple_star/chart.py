"""排盘核心：仅依据规则计算，不读取任何原书文本。"""

import json
import os

from .consts import (
    BOSHI_NAMES,
    CHANGSHENG_NAMES,
    CHANGSHENG_START,
    GAN,
    GAN_IDX,
    HUOLING,
    JU,
    JU_NAME,
    KUIYUE,
    LING,
    LUCUN,
    MINGZHU,
    NAYIN,
    PALACES,
    SHENZHU,
    SIHUA,
    SIHUA_TABLES,
    TIANFU_SERIES,
    TIANMA,
    WUHU,
    XIAOXIAN,
    ZHI,
    ZHI_IDX,
    ZIWEI_SERIES,
)

_DATA = os.path.join(os.path.dirname(__file__), "data", "ziwei_table.json")
with open(_DATA, encoding="utf-8") as f:
    ZIWEI_TABLE = json.load(f)
# 木三局初九在原传本中有缺，此处按通行补正（见 docs/limitations.md）
if "9" not in ZIWEI_TABLE.get("木三局", {}):
    ZIWEI_TABLE.setdefault("木三局", {})["9"] = "辰"


def add(zhi, n):
    return ZHI[(ZHI_IDX[zhi] + n) % 12]


def gz_of_year(year):
    """公历年 -> 干支（以农历年近似，仅用于展示；排盘请直接给年干支）。"""
    n = (year - 4) % 60
    return GAN[n % 10] + ZHI[n % 12]


def ganzhi_index(year_gz):
    g, z = GAN_IDX[year_gz[0]], ZHI_IDX[year_gz[1]]
    for i in range(60):
        if i % 10 == g and i % 12 == z:
            return i
    raise ValueError("invalid ganzhi: " + year_gz)


def chart(gender, year_gz, month, day, hour_idx, leap_month=False, late_zi="same", school=None):
    """排盘。

    gender: "男" / "女"
    year_gz: 农历年干支，如 "己卯"
    month: 农历月 1-12
    day: 农历日 1-30
    hour_idx: 0=子 .. 11=亥
    leap_month: 是否闰月（闰月按次月起命身）
    late_zi: "same"/"next" 晚子时归属
    """
    school = school or {}
    sihua_table = SIHUA_TABLES.get(school.get("sihua", "ben"), SIHUA)
    notes = []
    if leap_month:
        month = month % 12 + 1
        notes.append("闰月按次月起命身")
    if late_zi == "next" and hour_idx == 0:
        day = min(30, day + 1)
        notes.append("晚子时按次日计")
    yg, yz = year_gz[0], year_gz[1]
    g, z = GAN_IDX[yg], ZHI_IDX[yz]
    yin_gan = WUHU[g]
    ming_z = ZHI[(2 + (month - 1) - hour_idx) % 12]
    shen_z = ZHI[(2 + (month - 1) + hour_idx) % 12]
    ming_gan = GAN[(yin_gan + (ZHI_IDX[ming_z] - 2)) % 10]
    nayin = NAYIN.get(ming_gan + ming_z, "")
    ju_char = None
    for k in JU:
        if nayin.endswith(k):
            ju_char = k
            break
    if ju_char is None:
        raise ValueError("无法由命宫干支推五行局: " + ming_gan + ming_z)
    ju_name = JU_NAME[ju_char]
    ju_num = JU[ju_char]
    zw = ZIWEI_TABLE[ju_name][str(day)]
    tf = ZHI[(4 - ZHI_IDX[zw]) % 12]
    stars = {zi: [] for zi in ZHI}

    def put(star, pos):
        stars[pos].append(star)

    for name, off in ZIWEI_SERIES:
        put(name, add(zw, off))
    for name, off in TIANFU_SERIES:
        put(name, add(tf, off))
    put("文昌", add("戌", -hour_idx))
    put("文曲", add("辰", hour_idx))
    put("左輔", add("辰", month - 1))
    put("右弼", add("戌", -(month - 1)))
    kui, yue = KUIYUE[yg]
    put("天魁", kui)
    put("天鉞", yue)
    lc = LUCUN[yg]
    put("祿存", lc)
    put("擎羊", add(lc, 1))
    put("陀羅", add(lc, -1))
    put("天馬", TIANMA[yz])
    if school.get("huoling") == "hour":
        put("火星", add(HUOLING[yz], hour_idx))
        put("鈴星", add(LING[yz], hour_idx))
    else:
        put("火星", HUOLING[yz])
        put("鈴星", LING[yz])
    put("地劫", add("亥", hour_idx))
    put("地空", add("亥", -hour_idx))
    put("紅鸞", add("卯", -z))
    put("天喜", add(add("卯", -z), 6))
    put("天刑", add("酉", month - 1))
    put("天姚", add("丑", month - 1))
    put("三台", add("辰", month - 1 + day - 1))
    put("八座", add("戌", -(month - 1) - (day - 1)))
    put("台輔", add("午", hour_idx))
    put("封誥", add("寅", hour_idx))
    put("天哭", add("午", -z))
    put("天虛", add("午", z))
    put("龍池", add("辰", z))
    put("鳳閣", add("戌", -z))
    hua = {star: h for h, star in sihua_table[yg].items()}
    for h, star in sihua_table[yg].items():
        hua[star] = h
    palaces = {}
    for i, pname in enumerate(PALACES):
        pos = add(ming_z, -i)
        palaces[pname] = {"zhi": pos, "stars": sorted(stars[pos])}
    palace_by_zhi = {info["zhi"]: pname for pname, info in palaces.items()}
    star_palace = {star: pname for pname, info in palaces.items() for star in info["stars"]}
    shen_palace = palace_by_zhi.get(shen_z)
    yang_gan = g % 2 == 0
    male = gender == "男"
    forward = (yang_gan and male) or ((not yang_gan) and (not male))
    if school.get("daxian") == "ming":
        start_off = 0
    else:
        start_off = -11 if forward else -1
    daxian = {}
    for k in range(12):
        pos = add(ming_z, start_off + (k if forward else -k))
        age_from = ju_num + 10 * k
        daxian[pos] = {"from": age_from, "to": age_from + 9, "order": k + 1}
    daxian_sihua = {}
    for dz, _d in daxian.items():
        gan = GAN[(yin_gan + (ZHI_IDX[dz] - 2)) % 10]
        daxian_sihua[dz] = {"gan": gan, "hua": sihua_table.get(gan, {})}
        try:
            from .liunian_stars import layer_stars

            daxian_sihua[dz]["stars"] = layer_stars(gan, yz)
        except Exception:
            pass
    xx_start = XIAOXIAN[yz]
    xiaoxian = {}
    for age in range(1, 121):
        step = (age - 1) if male else -(age - 1)
        xiaoxian[age] = add(xx_start, step)
    return {
        "input": {
            "gender": gender,
            "year_gz": year_gz,
            "lunar_month": month,
            "lunar_day": day,
            "hour": ZHI[hour_idx] + "時",
        },
        "notes": notes,
        "year_ganzhi": year_gz,
        "yin_gan": GAN[yin_gan],
        "ming_zhi": ming_z,
        "ming_gan": ming_gan,
        "shen_zhi": shen_z,
        "nayin": nayin,
        "ju": ju_name,
        "ju_number": ju_num,
        "ziwei": zw,
        "tianfu": tf,
        "palaces": palaces,
        "palace_by_zhi": palace_by_zhi,
        "star_palace": star_palace,
        "shen_palace": shen_palace,
        "hua": hua,
        "daxian": daxian,
        "daxian_sihua": daxian_sihua,
        "xiaoxian": xiaoxian,
        "mingzhu": MINGZHU[ming_z],
        "shenzhu": SHENZHU[yz],
        "yang_yin": "陽" if yang_gan else "陰",
        "male": male,
        "forward": forward,
        "chang_sheng": {add(CHANGSHENG_START[ju_num], k if forward else -k): CHANGSHENG_NAMES[k] for k in range(12)},
        "bo_shi": {add(lc, (k if forward else -k)): BOSHI_NAMES[k] for k in range(12)},
    }


def doujun(year_zhi, birth_month, birth_hour_idx):
    start = add(year_zhi, -(birth_month - 1))
    return add(start, birth_hour_idx)


def liunian(ch, year_gz, age=None):
    """流年：流年命宫、流年四化落宫、大限/小限叠加。"""
    yg, yz = year_gz[0], year_gz[1]
    from .liunian_stars import liunian_stars
    from .liunian_stars import place as _place

    sihua_table = ch.get("sihua_table", SIHUA)
    res = {"year_gz": year_gz, "ming": yz, "hua": sihua_table.get(yg, {})}
    res["stars"] = liunian_stars(year_gz)
    res["star_palaces"], _ = _place(ch, year_gz)
    ln_palaces = []
    for i, pname in enumerate(PALACES):
        zpos = add(yz, -i)
        base_palace = [k for k, v in ch["palaces"].items() if v["zhi"] == zpos][0]
        ln_palaces.append(
            {"palace": pname, "zhi": zpos, "base": base_palace, "stars": ch["palaces"][base_palace]["stars"]}
        )
    res["palaces"] = ln_palaces
    loc = {}
    for h, star in sihua_table.get(yg, {}).items():
        for pname, info in ch["palaces"].items():
            if star in info["stars"]:
                loc[h] = {"star": star, "palace": pname, "zhi": info["zhi"]}
    res["hua_loc"] = loc
    if age:
        for dz, d in ch["daxian"].items():
            if d["from"] <= age <= d["to"]:
                res["daxian"] = {"zhi": dz, "from": d["from"], "to": d["to"]}
                res["daxian_sihua"] = ch["daxian_sihua"].get(dz, {})
                break
        res["xiaoxian"] = ch["xiaoxian"].get(age)
    return res
