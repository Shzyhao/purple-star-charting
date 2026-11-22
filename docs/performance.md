# 性能说明

## 基准（本地，Python 3.12，Windows）

    chart        0.08 ms/op
    analyze      0.92 ms/op
    sanfang      0.02 ms/op
    svg_render   0.51 ms/op

运行方式：

    python scripts/bench.py

可用 BENCH_N 环境变量调整迭代次数（默认 200）。

## 已做的优化

1. 排盘结果内置 palace_by_zhi、star_palace 索引，避免解读层反复线性搜索；
2. star_score 加 LRU 缓存（纯函数、输入有限）；
3. 命盘图字体加载与字号对象缓存，PNG 渲染不再重复加载字体；
4. 宫位查找统一走索引，缺失时回退线性搜索（保证兼容）。

## 说明

- 性能瓶颈主要在报告生成与文本渲染，单盘完整报告（含专题/流年/合盘）通常在数十毫秒量级；
- 批量排盘是逐人顺序处理，适合数百人以内；更大规模可按批拆分运行。
