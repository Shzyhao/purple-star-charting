# -*- coding: utf-8 -*-
"""版权合规扫描（默认快速模式；--deep 启用特征句哈希比对）。

检查项：
1. 禁止目录/文件/扩展名（扫描件、校勘稿、第三方文本、PDF、大图）；
2. 文本中的中文引号引文（「」）；
3. 超大文本文件提示；
4. --deep：按句哈希比对内置特征句（只存哈希，仓库无原文）。
用法：python scripts/copyright_scan.py [repo_root] [--deep]
退出码：0 通过，1 有问题
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
DEEP = "--deep" in sys.argv
FORBIDDEN_DIRS = ("_pages", "_ocr", "校勘", "参考txt", "reference_texts")
FORBIDDEN_FILES = ("chunks.jsonl",)
FORBIDDEN_EXT = (".pdf", ".docx", ".doc", ".jpg", ".jpeg")
QUOTE_RE = re.compile(r"「[^」]{6,200}」")
MAX_TEXT = 2 * 1024 * 1024
SELF = os.path.abspath(__file__)
HASH_FILE = os.path.join(os.path.dirname(__file__), "phrase_hashes.json")


def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: int(v) for k, v in raw.items()}


def norm(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def scan():
    problems = []
    hashes = load_hashes() if DEEP else {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        for d in list(dirnames):
            if d in FORBIDDEN_DIRS:
                problems.append(("DIR", os.path.join(rel_dir, d), "禁止目录"))
                dirnames.remove(d)
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            low = fn.lower()
            if os.path.abspath(full) == SELF:
                continue
            if low in FORBIDDEN_FILES:
                problems.append(("FILE", rel, "禁止文件"))
                continue
            if low.endswith(FORBIDDEN_EXT):
                problems.append(("EXT", rel, "禁止扩展名"))
                continue
            if os.path.getsize(full) > MAX_TEXT:
                problems.append(("SIZE", rel, "文本过大，需人工确认"))
            try:
                text = open(full, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for q in QUOTE_RE.findall(text):
                problems.append(("QUOTE", rel, "出现中文引号引文"))
            if hashes:
                for seg in re.split(r"[。；！？\n]", text):
                    n = norm(seg)
                    if len(n) < 6:
                        continue
                    for length in set(hashes.values()):
                        if len(n) < length:
                            continue
                        for i in range(0, len(n) - length + 1):
                            h = hashlib.sha256(n[i:i + length].encode()).hexdigest()
                            if h in hashes:
                                problems.append(("PHRASE", rel, "命中原文特征句哈希"))
    return problems


def main():
    problems = scan()
    if not problems:
        print("PASS: no copyright-risk content detected.")
        return 0
    print("FAIL: %d issue(s)" % len(problems))
    for kind, rel, msg in problems[:80]:
        print("  [%s] %s -> %s" % (kind, rel, msg))
    return 1


if __name__ == "__main__":
    sys.exit(main())
