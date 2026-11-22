# 贡献指南

感谢参与！请遵守以下规则：

## 内容红线

1. 不提交任何古籍原文、扫描件、逐字整理稿或第三方电子文本；
2. 引用只到卷篇与页码，不复制句子；
3. 不提交真实个人命盘数据（示例请用合成数据）；
4. 新增规则请注明依据与流派差异，不把一家之说写成唯一真理。

## 代码规范

- Python 3.9+，保持零第三方依赖（lunardate 必需，Pillow/opencc 为可选）；
- 新增功能请补单元测试；
- 提交前运行：

    python -m unittest discover -s tests -v
    python scripts/copyright_scan.py . --deep

- CI 会跑 Python 3.10/3.11/3.12 与版权深度扫描，扫描不过不能合并。

## 提交信息

使用 conventional commits，例如 feat: ... / fix: ... / docs: ...

## 免责

命理内容属传统术数文化，不构成医疗、投资、法律、婚姻等任何建议。
