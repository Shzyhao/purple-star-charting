# Purple Star Astrology Charting（紫微斗数排盘）

一个用于**紫微斗数排盘与白话解读**的开源工具：既可当作命令行工具使用，也可作为 DSH Agent Skill 安装。

> 本项目属**传统术数文献与玄学文化学习工具**，仅供研究与学习参考，不构成任何决策依据。请先阅读 [DISCLAIMER.md](DISCLAIMER.md)。

## 功能

- 排盘：命宫 / 身宫 / 五行局 / 紫微天府 / 十四主星 / 辅星 / 四化
- 大限、小限、流年（含大限四化与流年四化落宫）
- 命盘图：SVG（默认，无字体依赖），PNG（可选）
- 白话解读：星性、宫位、格局初筛、四化含义
- 星曜强弱：五行生克法（不依赖版本庙旺表），可选自备庙旺表加载（--miaowang）
- 流年诸星与流年完整十二宫
- 宫干四化（飞星）
- 格局扩充至 28 类
- 流派开关（四化表 / 火铃起法 / 大限起宫）
- 真太阳时校正（--city / --lon）
- JSON 输出（--json-out）与批量排盘（--batch）
- 合盘增强：姻缘窗口交集、大限同步度
- 专题扩充至 10 类（学业/子女/父母/迁移/合伙/官非等）
- 择时参考（--timing，按流日打分）
- 运势曲线（--fortune 年份区间）
- 专题：姻缘 / 事业 / 财运 / 健康（不涉寿命）
- 合盘：双盘互看、四化互落、大限节奏、年龄差与相处建议
- 流月 / 流日：按斗君起月，标注可靠性

## 安装

    pip install -r requirements.txt

仅需 Python 3.9+ 与 lunardate；生成 PNG 另需 Pillow 与中文字体。

## 使用

公历输入：

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --out out

农历输入：

    python -m purple_star --gender 女 --lunar-gz 辛未 --month 12 --day 13 --hour 酉 --year 2026

输出：out/命主_庚午.md 与 out/命主_庚午.svg（加 --png 另出位图）。

专题、流月、流日、合盘：

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --topic all --liuyue 2026 --out out
    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --date 2026-12-06 --out out
    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --hepan --gender2 女 --solar2 1988-03-02 --time2 09:00 --name A --name2 B --out out

## 作为 DSH Skill 使用

把 skills/purple-star-charting 目录复制到 DSH 的 skills 目录，即可在对话中触发（详见 skills/purple-star-charting/SKILL.md）。

## 数据与规则来源

- 排盘规则（五虎遁、五行局、紫微定位、十四主星、辅星、四化、大限、小限）依据传统紫微斗数通行排盘法整理；
- 四化表采用常见口诀所载之通行版本，不同流派存在差异，详见 references/interpretation.md；
- 本仓库**不含任何古籍原文、扫描件或逐字整理稿**，解读文字均为项目自撰白话，引用只到页码（见 docs/copyright.md）。

## 已知局限

- 庙旺强弱表暂未内置（整理与核对中）；
- 火铃、四化、大限起宫等存在流派差异，本工具采用一种通行方案；
- 时辰边界（真太阳时、晚子时）需使用者自行确认；
- 流月/流日的推法在古籍中较简略，结果仅供参考。

详见 docs/limitations.md。

完整参数与输出说明见 [docs/usage.md](docs/usage.md)，版本记录见 [CHANGELOG.md](CHANGELOG.md)。

## 免责声明与使用范围

- 仅供民间传统知识、玄学与古籍文化学习研究；
- 不预测寿命、不替代医疗/投资/法律/婚姻等专业建议；
- 生辰数据仅在本地处理，不上传；
- 不鼓励迷信，不用于诱导消费或付费占卜。

## 测试

    python -m unittest discover -s tests -v
    python scripts/copyright_scan.py . --deep

## 许可

- 代码：MIT（见 LICENSE）
- 文档与文字：CC BY-NC-SA 4.0（见 LICENSE-docs）

## 贡献

欢迎提交 issue 与 PR；新增规则请附上依据与测试用例，并确保不引入任何原文或第三方文本。
