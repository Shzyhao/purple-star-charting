# -*- coding: utf-8 -*-
"""生成特征句哈希表（只输出哈希，不保存、不打印原文）。

用法：
    python scripts/make_phrase_hashes.py [sentence_file]

sentence_file 为本地私有文件（默认 scripts/phrase_sources.local.txt，已在 .gitignore 中排除），
每行一句。若文件不存在，脚本会提示并退出——这样做是为了让公开仓库不含任何原文句子。
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "phrase_sources.local.txt")
OUT = os.path.join(HERE, "phrase_hashes.json")


def norm(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.exists(src):
        print("缺少本地特征句文件：%s" % src)
        print("请自行准备（每行一句），仓库不会保存该文件。")
        return 1
    data = {}
    with open(src, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            n = norm(s)
            if len(n) < 4:
                continue
            data[hashlib.sha256(n.encode()).hexdigest()] = len(n)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=0, ensure_ascii=False)
    print("written", OUT, len(data), "hashes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
