# -*- coding: utf-8 -*-
"""把 Markdown 报告转成自包含 HTML（无外部依赖）。"""
import html as _html
import re


def _esc(s):
    return _html.escape(s, quote=False)


def _inline(s):
    s = _esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = s.replace(chr(96), "")
    return s


def md_to_html(md, title="紫微斗数命盘解析"):
    lines = md.split("\n")
    out = []
    i = 0
    in_ul = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join("<th>%s</th>" % _inline(c) for c in header) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        if line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<h3>%s</h3>" % _inline(line[4:]))
        elif line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<h2>%s</h2>" % _inline(line[3:]))
        elif line.startswith("# "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<h1>%s</h1>" % _inline(line[2:]))
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>%s</li>" % _inline(line[2:]))
        elif line.strip() == "---":
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<hr>")
        elif line.strip() == "":
            if in_ul:
                out.append("</ul>")
                in_ul = False
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<p>%s</p>" % _inline(line))
        i += 1
    if in_ul:
        out.append("</ul>")
    body = "\n".join(out)
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>%s</title>
<style>
body{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;max-width:960px;margin:2em auto;padding:0 1em;line-height:1.7;color:#222}
h1{border-bottom:2px solid #333;padding-bottom:.3em}
h2{border-bottom:1px solid #999;padding-bottom:.2em;margin-top:1.6em}
table{border-collapse:collapse;width:100%%;margin:1em 0}
th,td{border:1px solid #bbb;padding:.4em .6em;text-align:left;font-size:.95em}
th{background:#f2f2f2}
blockquote{border-left:4px solid #ccc;margin:1em 0;padding:.2em 1em;color:#555;background:#fafafa}
hr{border:none;border-top:1px solid #ddd;margin:2em 0}
ul{padding-left:1.4em}
</style></head><body>
%s
</body></html>""" % (_esc(title), body)


def write_html(md_path, html_path, title="紫微斗数命盘解析"):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(md_to_html(md, title))
    return html_path
