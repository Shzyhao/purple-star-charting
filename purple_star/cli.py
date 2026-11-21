# -*- coding: utf-8 -*-
"""命令行入口：排盘、专题、合盘、流月流日。"""
import argparse
import os
import sys

from .chart import chart, gz_of_year, ganzhi_index, liunian
from . import interpret, render, hepan, topics, liuyue
from .consts import ZHI

GAN = "甲乙丙丁戊己庚辛壬癸"


def hour_index(hh):
    if hh >= 23 or hh < 1:
        return 0
    return (hh + 1) // 2 % 12


def solar_to_lunar(y, m, d):
    try:
        from lunardate import LunarDate
    except ImportError:
        raise SystemExit("需要 lunardate：pip install lunardate")
    ld = LunarDate.fromSolarDate(y, m, d)
    return ld.year, ld.month, ld.day, getattr(ld, "isLeapMonth", False)


def build_chart(args, prefix=""):
    if prefix:
        solar = getattr(args, "solar2")
        time_s = getattr(args, "time2") or "12:00"
        lunar_gz = getattr(args, "lunar_gz2")
        month = getattr(args, "month2")
        day = getattr(args, "day2")
        hour = getattr(args, "hour2")
        gender = getattr(args, "gender2")
        leap = getattr(args, "leap2")
        late = getattr(args, "late_zi")
    else:
        solar = args.solar
        time_s = args.time
        lunar_gz = args.lunar_gz
        month = args.month
        day = args.day
        hour = args.hour
        gender = args.gender
        leap = args.leap
        late = args.late_zi
    if solar:
        y, m, d = [int(x) for x in solar.split("-")]
        ly, lm, lday, leap = solar_to_lunar(y, m, d)
        hh, mm = [int(x) for x in time_s.split(":")]
        hidx = hour_index(hh)
        ygz = gz_of_year(ly)
        year = y
    else:
        if not (lunar_gz and month and day and hour):
            raise SystemExit("请提供公历生日，或农历年干支/月/日/时辰")
        lm, lday = month, day
        hidx = ZHI.index(hour)
        ygz = lunar_gz
        leap = bool(leap)
        year = None
    ch = chart(gender, ygz, lm, lday, hidx, leap_month=leap, late_zi=late)
    ch["birth_year"] = year
    return ch


def main(argv=None):
    ap = argparse.ArgumentParser(description="紫微斗数排盘与解读（传统术数文化学习工具）")
    ap.add_argument("--name", default="命主")
    ap.add_argument("--gender", choices=["男", "女"], required=True)
    ap.add_argument("--solar", help="公历生日 YYYY-MM-DD")
    ap.add_argument("--time", default="12:00")
    ap.add_argument("--lunar-gz", dest="lunar_gz")
    ap.add_argument("--month", type=int)
    ap.add_argument("--day", type=int)
    ap.add_argument("--hour")
    ap.add_argument("--leap", action="store_true")
    ap.add_argument("--late-zi", dest="late_zi", choices=["same", "next"], default="same")
    ap.add_argument("--year", type=int, help="分析流年的公历年")
    ap.add_argument("--topic", choices=["marriage", "career", "wealth", "health", "all"], help="专题")
    ap.add_argument("--liuyue", type=int, help="输出某年的流月表")
    ap.add_argument("--date", help="输出某公历日的流月流日 YYYY-MM-DD")
    ap.add_argument("--hepan", action="store_true", help="与第二人合盘")
    ap.add_argument("--name2", default="对方")
    ap.add_argument("--gender2", choices=["男", "女"])
    ap.add_argument("--solar2")
    ap.add_argument("--time2", default="12:00")
    ap.add_argument("--lunar-gz2", dest="lunar_gz2")
    ap.add_argument("--month2", type=int)
    ap.add_argument("--day2", type=int)
    ap.add_argument("--hour2")
    ap.add_argument("--leap2", action="store_true")
    ap.add_argument("--out", default="out")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args(argv)
    ch = build_chart(args)
    ln = None
    if args.year:
        age = (ganzhi_index(gz_of_year(args.year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1
        ln = liunian(ch, gz_of_year(args.year), age)
    md = interpret.analyze(ch, ln)
    if args.topic:
        names = ["marriage", "career", "wealth", "health"] if args.topic == "all" else [args.topic]
        for n in names:
            md += "\n\n" + topics.analyze_topic(n, ch, ln)
    if args.liuyue:
        md += "\n\n" + liuyue.liuyue_md(ch, args.liuyue)
    if args.date:
        y, m, d = [int(x) for x in args.date.split("-")]
        ly, lm, lday, _leap = solar_to_lunar(y, m, d)
        md += "\n\n" + liuyue.liuri_md(ch, ly, lm, lday)
    os.makedirs(args.out, exist_ok=True)
    base = os.path.join(args.out, "%s_%s" % (args.name, ch["year_ganzhi"]))
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(md)
    if not args.no_render:
        render.draw_svg(ch, base + ".svg")
        if args.png:
            render.draw_png(ch, base + ".png")
    print("report:", base + ".md")
    if args.hepan:
        if not args.gender2:
            raise SystemExit("合盘需要 --gender2")
        b = build_chart(args, prefix="2")
        hmd = hepan.analyze_hepan(ch, b, args.name, args.name2, args.year or 2026,
                                  year_a=ch.get("birth_year"), year_b=b.get("birth_year"))
        hbase = os.path.join(args.out, "%s_x_%s.md" % (args.name, args.name2))
        with open(hbase, "w", encoding="utf-8") as f:
            f.write(hmd)
        print("hepan:", hbase)
    return 0


if __name__ == "__main__":
    sys.exit(main())
