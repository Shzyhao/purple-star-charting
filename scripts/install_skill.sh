#!/usr/bin/env bash
# 将 purple-star-charting 安装到 DSH skills 目录
# 用法：bash scripts/install_skill.sh [目标目录]
set -euo pipefail
TARGET="${1:-$HOME/.dsh/skills}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/skills/purple-star-charting"
if [ ! -d "$SRC" ]; then echo "找不到 skills/purple-star-charting" >&2; exit 1; fi
mkdir -p "$TARGET"
rm -rf "$TARGET/purple-star-charting"
cp -R "$SRC" "$TARGET/purple-star-charting"
echo "已安装到: $TARGET/purple-star-charting"
