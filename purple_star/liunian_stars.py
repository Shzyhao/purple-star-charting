# -*- coding: utf-8 -*-
"""流年诸星：按流年干支起流禄、流羊、流陀、流马、流魁、流钺。

说明：流昌、流曲因流派差异较大（有以斗君起、有以年干起），暂不内置，见 docs/limitations.md。
"""
from .consts import LUCUN, KUIYUE, TIANMA, GAN_IDX, ZHI_IDX, GAN, ZHI


def add(zhi, n):
    return ZHI[(ZHI_IDX[zhi] + n) % 12]


def liunian_stars(year_gz):
    """流年六星落宫。"""
    yg, yz = year_gz[0], year_gz[1]
    lc = LUCUN[yg]
    kui, yue = KUIYUE[yg]
    return {
        "流祿": lc,
        "流羊": add(lc, 1),
        "流陀": add(lc, -1),
        "流馬": TIANMA[yz],
        "流魁": kui,
        "流鉞": yue,
    }


def place(ch, year_gz):
    """把流年诸星按宫位归组：{宫名: [流星...]}。"""
    stars = liunian_stars(year_gz)
    out = {}
    for name, zhi in stars.items():
        for pname, info in ch["palaces"].items():
            if info["zhi"] == zhi:
                out.setdefault(pname, []).append(name)
                break
    return out, stars
