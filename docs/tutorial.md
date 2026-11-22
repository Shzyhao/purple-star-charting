# 快速上手指南

## 1. 安装

    git clone https://github.com/Shzyhao/purple-star-charting.git
    cd purple-star-charting
    pip install -r requirements.txt

## 2. 排一张命盘

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --out out

会得到：
- out/命主_庚午.md：完整报告（十二宫、强弱、格局、四化、飞星、大限、流年）
- out/命主_庚午.svg：命盘图

## 3. 加专题与流月

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --topic all --liuyue 2026 --out out

## 4. 合盘

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --hepan --gender2 女 --solar2 1988-03-02 --time2 09:00 --name A --name2 B --out out

## 5. 真太阳时与流派

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --city 淄博 --out out
    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --school-sihua common --out out

## 6. 输出 JSON / HTML / 批量

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --json-out out/a.json --html --out out
    python -m purple_star --batch people.csv --out out/batch

批量 CSV 列：name,gender,solar,time,year。

## 7. 常见问题

见 docs/faq.md 与 docs/limitations.md。命理内容仅供传统术数文化学习参考。
