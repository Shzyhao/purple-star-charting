# Changelog

## 0.8.0

### 质量与性能
- 覆盖率门槛：50% -> 70%；新增 17 个测试（总测试数 76）
- 新增本地覆盖率脚本 scripts/coverage_local.py（纯标准库）
- 性能优化：排盘结果内置宫位索引、star_score LRU 缓存、字体缓存
- 新增基准脚本 scripts/bench.py 与 docs/performance.md
- lint 忽略项收敛（UP009/scripts E402），代码统一格式化

## 0.7.1

### 工程
- lint 套件：ruff check（E/F/W/I/UP/B）+ ruff format 检查
- mypy 基础类型检查（advisory）
- coverage 覆盖率报告（门槛 50%）
- actionlint（workflows）、shellcheck（scripts）、markdownlint（docs）
- 代码按 ruff format 统一格式化

## 0.7.0

### 新增
- 流昌、流曲：按流年/大限天干查传统通行十干表（docs/rules-liuchangqu.md）
- 大限运曜：运昌、运曲、运魁、运钺、运禄、运羊、运陀（流年报告中附带）
- README 增加命盘 SVG 示例与 HTML 报告示例
- CI 增加 ruff 静态检查与 coverage 覆盖率报告
- 新增测试（总测试数 61）

### 文档
- 规则说明：docs/rules-liuchangqu.md
- limitations 更新流昌流曲说明

## 0.6.0

### 新增
- HTML 报告输出：--html（自包含，可直接打开/打印为 PDF）
- 繁体输出：--traditional（需要可选依赖 opencc）
- PyPI 打包：pyproject.toml + purple-star 命令入口
- DSH skill 安装脚本：scripts/install_skill.ps1 / install_skill.sh
- 文档：快速上手（tutorial）、FAQ、术语表、英文 README
- 社区：CONTRIBUTING、Issue/PR 模板
- 新增 8 个测试（总测试数 61）

## 0.5.0

### 新增
- 合盘增强：姻缘窗口交集（2026-2031）、大限同步度
- 专题扩充：学业、子女、父母、迁移/出国、合伙、官非/合同（共 10 个专题）
- 择时：--timing 事件类型（签约/面试/出行/约会/就医/开业）+ --lunar-month，按流日打分排序
- 运势曲线：--fortune 起止年份，大限分 + 流年分综合评级
- 多专题支持：--topic study,legal（逗号分隔）
- 新增 12 个测试（总测试数 56）

## 0.4.0

### 新增
- 流年诸星：流禄、流羊、流陀、流马、流魁、流钺（流昌曲因流派差异暂不内置）
- 流年完整十二宫排盘（流年命宫起十二宫，叠加本命星曜）
- 宫干四化（飞星）：十二宫宫干各自起四化并列出飞入宫位
- 格局扩充：13 类 -> 28 类
- 流派开关：--school-sihua ben/common、--school-huoling year/hour、--school-daxian guardian/ming
- 真太阳时：--city / --lon，经度差 + 均时差校正
- 闰月模式：--leap-mode next/half
- JSON 输出：--json-out
- 批量排盘：--batch CSV，输出 batch_summary.csv
- 新增 12 个测试（总测试数 44）

## 0.3.0

### 新增
- 星曜强弱：五行生克法（宫生星/比和/星克宫/星生宫/宫克星），输出十二宫强弱与三方四正综合
- 报告新增强弱与三方四正章节，十二宫表增加强弱列
- 支持自备庙旺表加载（--miaowang，格式见 docs/data/miaowang-schema.md）
- 新增 12 个强弱相关测试（总测试数 32）

### 说明
- 仓库不附带任何版本的庙旺表：传统表存在版本差异与整理版权问题，强弱用自撰五行生克规则实现

## 0.2.0（M1 + M2 + M3）

### 新增
- 合盘模块：双盘互看、夫妻宫互看、四化互落、大限节奏、年龄差与相处建议
- 专题：姻缘 / 事业 / 财运 / 健康（不涉寿命，均带免责）
- 流月 / 流日：斗君起月、流日顺行，标注可靠性
- CLI 全面支持上述功能（--topic/--liuyue/--date/--hepan）
- 单元测试：25 个（排盘、四化、大限、流年、闰月、斗君、渲染、解读、合盘、专题、流月、CLI、版权扫描）
- CI：Python 3.10-3.12 测试 + 版权深度扫描

### 文档
- README、docs/usage.md、docs/copyright.md、docs/design.md、docs/limitations.md、docs/roadmap.md
- Skill 定义与 references（输入指南、解读参考、引用策略、合盘指南、示例）

### 安全
- 版权扫描：禁止目录/文件/扩展名、中文引号引文、超文本、特征句哈希比对

## 0.1.0

- 初始仓库骨架与排盘核心
