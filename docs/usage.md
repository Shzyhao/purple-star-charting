# 使用说明（CLI 参考）

## 安装

    pip install -r requirements.txt

仅需 Python 3.9+；生成 PNG 需 Pillow 与中文字体。

## 基本排盘

公历：

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --out out

农历：

    python -m purple_star --gender 女 --lunar-gz 辛未 --month 12 --day 13 --hour 酉 --out out

## 参数表

| 参数 | 说明 |
|---|---|
| --name | 姓名/标签（输出文件名用） |
| --gender | 男 / 女（必填） |
| --solar | 公历生日 YYYY-MM-DD |
| --time | 出生时间 HH:MM（公历模式） |
| --lunar-gz | 农历年干支（如 庚午） |
| --month / --day | 农历月 / 日 |
| --hour | 时辰（子丑寅卯…亥） |
| --leap | 该农历月为闰月 |
| --late-zi | same / next：晚子时归属 |
| --year | 要分析的流年公历年 |
| --topic | marriage / career / wealth / health / all |
| --liuyue | 输出该年 12 个流月表 |
| --date | 输出某公历日的流月流日 |
| --hepan | 与第二人合盘 |
| --name2 / --gender2 / --solar2 / --time2 / --lunar-gz2 / --month2 / --day2 / --hour2 | 第二人资料 |
| --out | 输出目录（默认 out） |
| --miaowang | 自备庙旺表 JSON 路径（可选，格式见 docs/data/miaowang-schema.md） |
| --png | 额外生成 PNG 命盘图 |
| --no-render | 不生成图 |

## 输出

- 报告：out/名称_年干支.md
- 命盘图：out/名称_年干支.svg（--png 另出 .png）
- 合盘：out/A_x_B.md

## 常见问题

1. 缺 lunardate：pip install -r requirements.txt；
2. 中文显示方块：系统缺 CJK 字体，优先用 SVG；
3. 与别家排盘不同：四化、火铃、大限起宫存在流派差异，见 docs/limitations.md；
4. 时辰边界：程序不做真太阳时校正，请自行确认。

## 退出码

- 0：成功
- 非 0：参数错误或依赖缺失（见错误信息）
