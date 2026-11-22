# -*- coding: utf-8 -*-
"""命令行入口：排盘、专题、合盘、流月流日、流年诸星、飞星、JSON、批量。"""
import argparse
import csv
import json
import os
import sys

from .chart import chart, gz_of_year, ganzhi_index, liunian
from . import interpret, render, hepan, topics, liuyue, strength, fly
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


def _school(args):
    return {
        "sihua": getattr(args, "school_sihua", "ben"),
        "huoling": getattr(args, "school_huoling", "year"),
        "daxian": getattr(args, "school_daxian", "guardian"),
    }


def _solar_hour(args, hh, mm, y, m, d):
    """按出生地经度做真太阳时校正；返回 (hh, mm, note)。"""
    city = getattr(args, "city", None)
    lon = getattr(args, "lon", None)
    if not city and lon is None:
        return hh, mm, None
    from . import solartime
    if lon is None:
        lon = solartime.CITY_LON.get(city)
    if lon is None:
        return hh, mm, None
    th, tm = solartime.true_solar(hh, mm, y, m, d, lon)
    return th, tm, "真太阳时校正：经度 %.2f，%02d:%02d -> %02d:%02d" % (lon, hh, mm, th, tm)


def build_chart(args, prefix="", school=None):
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
    notes = []
    if solar:
        y, m, d = [int(x) for x in solar.split("-")]
        ly, lm, lday, leap = solar_to_lunar(y, m, d)
        hh, mm = [int(x) for x in time_s.split(":")]
        th, tm, note = _solar_hour(args, hh, mm, y, m, d)
        if note:
            notes.append(note)
        hidx = hour_index(th)
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
    if leap:
        mode = getattr(args, "leap_mode", "next")
        if mode == "half" and solar:
            if lday > 15:
                lm = lm % 12 + 1
            leap = False
            notes.append("闰月按半月法：%s" % ("下半月按次月" if lday > 15 else "上半月按本月"))
        elif mode == "half":
            notes.append("闰月半月法需要公历模式（需要具体日）")
    ch = chart(gender, ygz, lm, lday, hidx, leap_month=leap, late_zi=late, school=school or {})
    ch["birth_year"] = year
    if notes:
        ch["notes"] = list(ch.get("notes", [])) + notes
    return ch


def _json_payload(ch, ln):
    return {
        "version": "0.4.0",
        "input": ch["input"],
        "ming": {"zhi": ch["ming_zhi"], "gan": ch["ming_gan"], "shen": ch["shen_zhi"],
                 "ju": ch["ju"], "ziwei": ch["ziwei"], "tianfu": ch["tianfu"]},
        "hua": ch["hua"],
        "palaces": {k: {"zhi": v["zhi"], "stars": v["stars"]} for k, v in ch["palaces"].items()},
        "daxian": ch["daxian"],
        "liunian": ln,
        "geju": interpret.detect_geju(ch),
        "strength": {p: strength.palace_strength(ch, p) for p in ch["palaces"]},
        "sanfang": strength.sanfang(ch),
        "feixing": fly.feixing(ch, ch.get("sihua_table")),
    }


def run_one(args, out_dir=None):
    school = _school(args)
    ch = build_chart(args, school=school)
    ln = None
    if getattr(args, "year", None):
        age = (ganzhi_index(gz_of_year(args.year)) - ganzhi_index(ch["year_ganzhi"])) % 60 + 1
        ln = liunian(ch, gz_of_year(args.year), age)
    miaowang = strength.load_miaowang(args.miaowang) if getattr(args, "miaowang", None) else None
    md = interpret.analyze(ch, ln, miaowang=miaowang)
    if getattr(args, "topic", None):
        names = ["marriage", "career", "wealth", "health"] if args.topic == "all" else [args.topic]
        for n in names:
            md += "\n\n" + topics.analyze_topic(n, ch, ln)
    if getattr(args, "liuyue", None):
        md += "\n\n" + liuyue.liuyue_md(ch, args.liuyue)
    if getattr(args, "date", None):
        y, m, d = [int(x) for x in args.date.split("-")]
        ly, lm, lday, _leap = solar_to_lunar(y, m, d)
        md += "\n\n" + liuyue.liuri_md(ch, ly, lm, lday)
    out = out_dir or args.out
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, "%s_%s" % (args.name, ch["year_ganzhi"]))
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(md)
    if not args.no_render:
        render.draw_svg(ch, base + ".svg")
        if args.png:
            render.draw_png(ch, base + ".png")
    if getattr(args, "json_out", None):
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(_json_payload(ch, ln), f, ensure_ascii=False, indent=1)
    return base, ch, ln


def run_batch(args):
    path = args.batch
    out_root = args.out
    os.makedirs(out_root, exist_ok=True)
    summary = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for i, row in enumerate(rows, 1):
        ns = argparse.Namespace(**vars(args))
        ns.name = row.get("name") or ("person%d" % i)
        ns.gender = row.get("gender") or "男"
        ns.solar = row.get("solar") or None
        ns.time = row.get("time") or "12:00"
        ns.lunar_gz = row.get("lunar_gz") or None
        ns.month = int(row["month"]) if row.get("month") else None
        ns.day = int(row["day"]) if row.get("day") else None
        ns.hour = row.get("hour") or None
        ns.year = int(row["year"]) if row.get("year") else None
        ns.hepan = False
        ns.json_out = None
        try:
            base, ch, ln = run_one(ns, out_root)
            summary.append({"name": ns.name, "status": "ok", "file": os.path.basename(base) + ".md",
                            "ming": ch["ming_zhi"], "ju": ch["ju"]})
        except Exception as e:
            summary.append({"name": ns.name, "status": "error", "error": str(e)[:80]})
    sum_path = os.path.join(out_root, "batch_summary.csv")
    with open(sum_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "status", "file", "ming", "ju", "error"])
        w.writeheader()
        for r in summary:
            w.writerow({k: r.get(k, "") for k in ["name", "status", "file", "ming", "ju", "error"]})
    print("batch done:", len(summary), "->", sum_path)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="紫微斗数排盘与解读（传统术数文化学习工具）")
    ap.add_argument("--name", default="命主")
    ap.add_argument("--gender", choices=["男", "女"])
    ap.add_argument("--solar", help="公历生日 YYYY-MM-DD")
    ap.add_argument("--time", default="12:00")
    ap.add_argument("--lunar-gz", dest="lunar_gz")
    ap.add_argument("--month", type=int)
    ap.add_argument("--day", type=int)
    ap.add_argument("--hour")
    ap.add_argument("--leap", action="store_true")
    ap.add_argument("--leap-mode", dest="leap_mode", choices=["next", "half"], default="next")
    ap.add_argument("--late-zi", dest="late_zi", choices=["same", "next"], default="same")
    ap.add_argument("--city", help="出生城市（用于真太阳时校正，如 淄博）")
    ap.add_argument("--lon", type=float, help="出生地经度（度，东经为正）")
    ap.add_argument("--school-sihua", dest="school_sihua", choices=["ben", "common"], default="ben")
    ap.add_argument("--school-huoling", dest="school_huoling", choices=["year", "hour"], default="year")
    ap.add_argument("--school-daxian", dest="school_daxian", choices=["guardian", "ming"], default="guardian")
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
    ap.add_argument("--miaowang", help="自备庙旺表 JSON 路径（可选）")
    ap.add_argument("--json-out", dest="json_out", help="输出 JSON 到指定路径")
    ap.add_argument("--batch", help="批量排盘 CSV（列：name,gender,solar,time,year）")
    ap.add_argument("--out", default="out")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args(argv)
    if args.batch:
        return run_batch(args)
    if not args.gender:
        raise SystemExit("需要 --gender")
    base, ch, ln = run_one(args)
    print("report:", base + ".md")
    if args.hepan:
        if not args.gender2:
            raise SystemExit("合盘需要 --gender2")
        b = build_chart(args, prefix="2", school=_school(args))
        hmd = hepan.analyze_hepan(ch, b, args.name, args.name2, args.year or 2026,
                                  year_a=ch.get("birth_year"), year_b=b.get("birth_year"))
        hbase = os.path.join(args.out, "%s_x_%s.md" % (args.name, args.name2))
        with open(hbase, "w", encoding="utf-8") as f:
            f.write(hmd)
        print("hepan:", hbase)
    return 0


if __name__ == "__main__":
    sys.exit(main())
