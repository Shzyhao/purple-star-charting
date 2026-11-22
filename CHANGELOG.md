# Changelog

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
