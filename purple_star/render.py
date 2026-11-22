"""命盘图：SVG 为主（无字体依赖），PNG 可选（需 Pillow 与中文字体）。"""

import os

FONT_FAMILY = "Noto Sans CJK SC, Source Han Sans SC, Microsoft JhengHei, sans-serif"
GRID = [
    ("巳", 0, 0),
    ("午", 0, 1),
    ("未", 0, 2),
    ("申", 0, 3),
    ("辰", 1, 0),
    ("酉", 1, 3),
    ("卯", 2, 0),
    ("戌", 2, 3),
    ("寅", 3, 0),
    ("丑", 3, 1),
    ("子", 3, 2),
    ("亥", 3, 3),
]
POS = {z: (r, c) for z, r, c in GRID}


def _cells(ch):
    cells = {}
    dx = {z: "%d-%d" % (d["from"], d["to"]) for z, d in ch["daxian"].items()}
    for z in POS:
        pname = ""
        stars = []
        for pn, info in ch["palaces"].items():
            if info["zhi"] == z:
                pname = pn
                stars = info["stars"]
                break
        cells[z] = {"palace": pname, "stars": stars, "daxian": dx.get(z, ""), "shen": pname == ch["shen_palace"]}
    return cells


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def draw_svg(ch, path, W=1100, H=1100):
    cells = _cells(ch)
    cw, chh = W / 4.0, H / 4.0
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    for z, r, c in GRID:
        x0, y0 = c * cw, r * chh
        parts.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#222" stroke-width="1.2"/>'
            % (x0, y0, cw, chh)
        )
        info = cells[z]
        label = (info["palace"] or "") + ("★" if info["shen"] else "")
        parts.append(
            '<text x="%.1f" y="%.1f" font-size="16" font-family="%s">%s</text>'
            % (x0 + 8, y0 + 20, FONT_FAMILY, _esc(label))
        )
        parts.append(
            '<text x="%.1f" y="%.1f" font-size="20" text-anchor="end" font-family="%s">%s</text>'
            % (x0 + cw - 8, y0 + 22, FONT_FAMILY, z)
        )
        lines, cur = [], ""
        for s in info["stars"]:
            h = ch["hua"].get(s, "")
            t = s + ("(" + h + ")" if h else "")
            if len(cur) + len(t) + 1 > 9:
                lines.append(cur)
                cur = t
            else:
                cur = (cur + " " + t).strip()
        if cur:
            lines.append(cur)
        y = y0 + 44
        for ln in lines[:6]:
            parts.append(
                '<text x="%.1f" y="%.1f" font-size="13" font-family="%s">%s</text>' % (x0 + 8, y, FONT_FAMILY, _esc(ln))
            )
            y += 17
        if info["daxian"]:
            parts.append(
                '<text x="%.1f" y="%.1f" font-size="12" fill="#777" font-family="%s">%s</text>'
                % (x0 + 8, y0 + chh - 10, FONT_FAMILY, info["daxian"])
            )
    x0, y0 = cw, chh
    parts.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#222" stroke-width="1.2"/>'
        % (x0, y0, 2 * cw, 2 * chh)
    )
    info_lines = [
        "紫微斗数命盘",
        "性别：%s（%s）" % ("男" if ch["male"] else "女", ch["yang_yin"]),
        "生年：%s  农历：%d月%d日 %s"
        % (ch["year_ganzhi"], ch["input"]["lunar_month"], ch["input"]["lunar_day"], ch["input"]["hour"]),
        "命宫：%s  身宫：%s" % (ch["ming_zhi"], ch["shen_zhi"]),
        "五行局：%s  紫微在%s" % (ch["ju"], ch["ziwei"]),
        "命主：%s  身主：%s" % (ch["mingzhu"], ch["shenzhu"]),
    ]
    y = y0 + 30
    for ln in info_lines:
        parts.append(
            '<text x="%.1f" y="%.1f" font-size="16" font-family="%s">%s</text>' % (x0 + 20, y, FONT_FAMILY, _esc(ln))
        )
        y += 28
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    return path


def _find_font():
    cands = [
        "C:/Windows/Fonts/NotoSansCJKsc-Regular.otf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msjh.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def draw_png(ch, path, W=1100, H=1100):
    """可选：需要 Pillow 与中文字体；找不到字体时退回默认字体（可能显示方块）。"""
    from PIL import Image, ImageDraw, ImageFont

    cells = _cells(ch)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    cw, chh = W / 4.0, H / 4.0
    fp = _find_font()

    def font(sz):
        if fp:
            return ImageFont.truetype(fp, sz)
        return ImageFont.load_default()

    f_small, f_mid, f_big = font(13), font(16), font(20)
    for z, r, c in GRID:
        x0, y0 = c * cw, r * chh
        d.rectangle([x0, y0, x0 + cw, y0 + chh], outline="#222", width=1)
        info = cells[z]
        d.text((x0 + 8, y0 + 4), (info["palace"] or "") + ("★" if info["shen"] else ""), fill="black", font=f_mid)
        d.text((x0 + cw - 30, y0 + 4), z, fill="black", font=f_big)
        lines, cur = [], ""
        for s in info["stars"]:
            h = ch["hua"].get(s, "")
            t = s + ("(" + h + ")" if h else "")
            if len(cur) + len(t) + 1 > 9:
                lines.append(cur)
                cur = t
            else:
                cur = (cur + " " + t).strip()
        if cur:
            lines.append(cur)
        y = y0 + 30
        for ln in lines[:6]:
            d.text((x0 + 8, y), ln, fill="black", font=f_small)
            y += 18
        if info["daxian"]:
            d.text((x0 + 8, y0 + chh - 22), info["daxian"], fill="gray", font=f_small)
    x0, y0 = cw, chh
    d.rectangle([x0, y0, 3 * cw, 3 * chh], outline="#222", width=1)
    info_lines = [
        "紫微斗数命盘",
        "性别：%s（%s）" % ("男" if ch["male"] else "女", ch["yang_yin"]),
        "生年：%s 农历%d月%d日 %s"
        % (ch["year_ganzhi"], ch["input"]["lunar_month"], ch["input"]["lunar_day"], ch["input"]["hour"]),
        "命宫：%s 身宫：%s" % (ch["ming_zhi"], ch["shen_zhi"]),
        "五行局：%s 紫微在%s" % (ch["ju"], ch["ziwei"]),
        "命主：%s 身主：%s" % (ch["mingzhu"], ch["shenzhu"]),
    ]
    y = y0 + 20
    for ln in info_lines:
        d.text((x0 + 16, y), ln, fill="black", font=f_mid)
        y += 26
    img.save(path)
    return path
