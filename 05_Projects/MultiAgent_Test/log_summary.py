#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""log_summary.py — 读取每日日志，统计最近 7 天的记录天数并提取「今天完成」要点，输出一行周摘要。

用法：
    python log_summary.py

日志目录：D:\\Personal_AI_OS\\13_Growth\\Daily\\（文件名须为 YYYY-MM-DD.md）
仅使用标准库：pathlib, re, datetime, os
"""

import re
import sys
from datetime import date, timedelta
from pathlib import Path

DEFAULT_LOG_DIR = Path(r"D:\Personal_AI_OS\13_Growth\Daily")

# Windows 下 stdout/stderr 默认可能是 GBK 编码，无法输出 📊 等 emoji，统一强制 UTF-8
for stream in (sys.stdout, sys.stderr):
    if stream is not None and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")
DATE_FILE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
COMPLETED_SECTION = re.compile(r"^##\s*今天完成\s*$")
HEADING = re.compile(r"^##")


def get_recent_logs(log_dir, days=7):
    """扫描目录，筛选最近 N 天的日志文件。

    返回 list[tuple[date, str]] — [(日期, 文件完整路径), ...]，按日期降序。
    非 YYYY-MM-DD.md 命名的文件（如 README.md）自动跳过。
    目录不存在时抛出 NotADirectoryError，由调用方处理。
    """
    log_dir = Path(log_dir)
    if not log_dir.is_dir():
        raise NotADirectoryError(f"日志目录不存在: {log_dir}")

    start = date.today() - timedelta(days=days - 1)
    today = date.today()
    recent = []
    for path in log_dir.iterdir():
        match = DATE_FILE_PATTERN.match(path.name)
        if not match or not path.is_file():
            continue
        try:
            file_date = date.fromisoformat(match.group(1))
        except ValueError:
            continue  # 日期非法（如 2026-13-99），跳过
        if start <= file_date <= today:
            recent.append((file_date, str(path)))
    recent.sort(key=lambda item: item[0], reverse=True)
    return recent


def parse_completed_items(file_path):
    """从单个 md 文件中提取「## 今天完成」区块下的要点列表。

    返回 list[str] — 每条要点去掉 "- " 前缀和 **加粗** 标记后的文本。
    无该区块或区块下无要点时返回空列表，不影响其他文件。
    """
    content = _read_text(file_path)
    if content is None:
        return []  # 编码无法识别，已 warn 并跳过

    items = []
    in_section = False
    for line in content.splitlines():
        if COMPLETED_SECTION.match(line):
            in_section = True
            continue
        if in_section and HEADING.match(line):
            break  # 遇到下一个 ## 标题，停止收集
        if in_section and line.startswith("- "):
            text = line[2:].strip().replace("**", "").strip()
            if text:
                items.append(text)
    return items


def build_week_summary(log_dir, days=7):
    """汇总最近 N 天的日志，组装一行周摘要字符串。"""
    recent = get_recent_logs(log_dir, days)
    if not recent:
        return f"最近{days}天无日志记录"

    items = []
    for _, path in recent:
        items.extend(parse_completed_items(path))

    header = f"📊 最近{days}天周摘要（{len(recent)}/{days}天有记录）"
    if not items:
        return header + "：无完成要点。"
    return header + "：" + "；".join(items) + "。"


def _read_text(file_path):
    """按 utf-8 读取，失败回退 gbk；都失败则 warn 并返回 None。"""
    path = Path(file_path)
    for encoding in ("utf-8", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    print(f"[warn] 编码无法识别，跳过文件: {path}", file=sys.stderr)
    return None


def main():
    """入口：调用 build_week_summary 并 print 结果。"""
    try:
        print(build_week_summary(DEFAULT_LOG_DIR))
    except NotADirectoryError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
