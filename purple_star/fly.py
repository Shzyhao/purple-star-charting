"""宫干四化（飞星）：十二宫宫干各自起四化，看化禄权科忌飞入何宫。"""

from .consts import GAN, GAN_IDX, PALACES, SIHUA, WUHU, ZHI_IDX, to_simp


def palace_gans(ch):
    """按五虎遁推十二宫天干。"""
    yin_gan = WUHU[GAN_IDX[ch["year_ganzhi"][0]]]
    gans = {}
    for pname in PALACES:
        zhi = ch["palaces"][pname]["zhi"]
        gans[pname] = GAN[(yin_gan + (ZHI_IDX[zhi] - 2)) % 10]
    return gans


def feixing(ch, sihua_table=None):
    """每宫宫干四化飞入的宫位。返回 {宫: {干, hua: {禄: (星, 宫), ...}}}"""
    table = sihua_table or SIHUA
    gans = palace_gans(ch)
    out = {}
    for pname in PALACES:
        gan = gans[pname]
        hua = table.get(gan, {})
        targets = {}
        for h, star in hua.items():
            for p2 in PALACES:
                if star in ch["palaces"][p2]["stars"]:
                    targets[h] = (star, p2)
                    break
        out[pname] = {"gan": gan, "hua": targets}
    return out


def feixing_md(ch, sihua_table=None):
    fx = feixing(ch, sihua_table)
    lines = ["## 宫干四化（飞星）", "", "| 宫位 | 宫干 | 化禄→ | 化权→ | 化科→ | 化忌→ |", "|---|---|---|---|---|---|"]
    for pname in PALACES:
        d = fx[pname]
        cells = []
        for h in "祿權科忌":
            t = d["hua"].get(h)
            cells.append(("%s→%s" % (to_simp(t[0]), to_simp(t[1]))) if t else "—")
        lines.append(
            "| %s | %s | %s | %s | %s | %s |" % (to_simp(pname), d["gan"], cells[0], cells[1], cells[2], cells[3])
        )
    lines.append("")
    lines.append("> 飞星派用法：看某宫宫干化忌飞入何宫，即该宫对此宫的影响；不同流派取用不同，此处仅列映射。")
    return "\n".join(lines)
