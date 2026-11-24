#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check.py — 成品自检：比例 / 尺寸 / 接缝

用法：
    python check.py poster_001.jpg                 # 自动找接缝
    python check.py poster_001.jpg --composed      # 拼接产物：位置已知，只查接缝干不干净
    python check.py poster_001.jpg --ratio 46      # 黏土类
    python check.py a.jpg b.jpg c.jpg              # 批量
    python check.py poster.jpg --debug             # 输出标注图 poster__check.jpg

只做机器能判断的三件事。剩下的（上半区保真、下半区是重构不是滤镜）要靠眼睛，见 08-qa.md。

⚠️ 自动找接缝靠"横向色差最强的一行"，当接缝两侧材质接近（深蓝接深蓝）时会找错行。
   凡是走 compose.py 拼出来的图，一律加 --composed，位置按构造值直接判定。
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("缺少 Pillow：pip install pillow")

TARGET = 4 / 3  # 高/宽
COLS = 240      # 分析用的横向采样列数


def profile(img):
    """逐行分析：(每行平均色, 每行与上一行的平均色差)"""
    small = img.convert("RGB")
    w, h = small.size
    rows = min(h, 900)
    small = small.resize((COLS, rows), Image.BILINEAR)
    px = small.load()

    means, edges = [], []
    prev = None
    for y in range(rows):
        r = g = b = 0
        e = 0.0
        for x in range(COLS):
            pr, pg, pb = px[x, y]
            r += pr; g += pg; b += pb
            if prev is not None:
                e += abs(pr - prev[x][0]) + abs(pg - prev[x][1]) + abs(pb - prev[x][2])
        means.append((r / COLS, g / COLS, b / COLS))
        edges.append(e / (COLS * 3) if prev is not None else 0.0)
        prev = [px[x, y] for x in range(COLS)]
    return means, edges, rows


def detect_seam(edges, rows, expect):
    """在期望位置 ±12% 内找色差最强的一行，返回 (位置百分比, 置信度)"""
    lo = max(2, int(rows * (expect / 100 - 0.12)))
    hi = min(rows - 1, int(rows * (expect / 100 + 0.12)))
    band = edges[lo:hi]
    if not band:
        return None, 0.0
    peak = max(band)
    at = lo + band.index(peak)
    baseline = sorted(edges[1:])[len(edges) // 2] or 1e-6
    return at / rows * 100, peak / baseline


def seam_quality(means, edges, rows, pos):
    """已知接缝位置时，判断接缝状态：两侧色差多大、有没有一条脏的 1px 线"""
    y = int(rows * pos / 100)
    if y < 3 or y > rows - 3:
        return None

    def dist(a, b):
        return sum(abs(x - z) for x, z in zip(a, b)) / 3

    top_prev, top_last = means[y - 2], means[y - 1]
    bot_first, bot_next = means[y], means[y + 1]
    delta = dist(top_last, bot_first)          # 接缝两侧的正常色差
    line = max(dist(top_prev, top_last),       # 脏线：接缝某一侧多出一条 1px 亮/暗行
               dist(bot_first, bot_next))
    return delta, line


def check_one(path, ratio, debug, composed):
    p = Path(path)
    img = Image.open(p)
    w, h = img.size
    lines = [f"\n📄 {p.name}  {w}×{h}"]

    ar = h / w
    dev = abs(ar - TARGET) / TARGET
    if dev <= 0.015:
        lines.append(f"✅ 比例 {ar:.3f} ≈ 3:4")
    else:
        lines.append(f"❌ 比例 {ar:.3f} 偏离 3:4 达 {dev:.1%}（3:4 应为 {TARGET:.3f}）")

    if w < 1080:
        lines.append(f"⚠️  宽度 {w} 偏小，公众号/小红书建议 ≥1080")

    means, edges, rows = profile(img)

    if composed:
        # 位置由构造保证，只校验接缝本身
        px_ratio = ratio
        exact = abs((h * ratio / 100) - round(h * ratio / 100)) < 0.5
        lines.append(f"✅ 拼接产物：中线按构造位于 {px_ratio:.0f}%"
                     f"（上 {round(h * ratio / 100)}px / 下 {h - round(h * ratio / 100)}px"
                     f"{'，像素级等分' if abs(ratio - 50) < 1e-9 and h % 2 == 0 else ''}）")
        q = seam_quality(means, edges, rows, px_ratio)
        if q:
            delta, line = q
            if line > 18 and line > delta * 0.5:
                lines.append(f"❌ 接缝处有一条脏线（1px 跳变 {line:.0f}，接缝本身色差 {delta:.0f}）"
                             f"——下半区顶端有暗角/投影/贴边残留，用 --trim-top 2 重拼")
            elif delta < 4:
                lines.append(f"✅ 接缝几乎看不出（两侧色差 {delta:.0f}），无缝衔接")
            elif delta <= 45:
                lines.append(f"✅ 接缝干净，两侧色差 {delta:.0f}")
            else:
                lines.append(f"✅ 接缝是清晰硬边（两侧色差 {delta:.0f}），符合这套版式"
                             f"——嫌跳就让下半区顶端留白，或 --trim-top 2")
    else:
        seam, conf = detect_seam(edges, rows, ratio)
        if seam is None:
            lines.append("⚠️  没检测到接缝（图太小）")
        elif conf < 2.0:
            lines.append(f"⚠️  接缝对比度太低（{conf:.1f}× 背景），位置不可靠"
                         f"——若这是拼接产物，加 --composed 直接按构造值判定")
        else:
            offset = seam - ratio
            if abs(offset) <= 1.0:
                lines.append(f"✅ 接缝在 {seam:.1f}%，与设定 {ratio:.0f}% 相符")
            else:
                lines.append(f"❌ 接缝在 {seam:.1f}%，设定是 {ratio:.0f}%，差 {offset:+.1f} 个点")

    if debug:
        out = p.with_name(p.stem + "__check.jpg")
        vis = img.convert("RGB").copy()
        d = ImageDraw.Draw(vis)
        y = h * ratio / 100
        d.line([(0, y), (w, y)], fill=(255, 0, 0), width=max(2, w // 500))
        vis.save(out, quality=90)
        lines.append(f"🖼  标注图：{out}（红线=设定中线）")

    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ap = argparse.ArgumentParser(description="成品自检：比例 / 尺寸 / 接缝")
    ap.add_argument("files", nargs="+", help="一个或多个成品图")
    ap.add_argument("--ratio", type=float, default=50.0, help="上半区占比，默认 50")
    ap.add_argument("--composed", action="store_true",
                    help="compose.py 拼接产物：中线位置按构造值直接判定，只查接缝干净度")
    ap.add_argument("--debug", action="store_true", help="输出标注图")
    args = ap.parse_args()

    for f in args.files:
        print(check_one(f, args.ratio, args.debug, args.composed))
    print()


if __name__ == "__main__":
    main()
