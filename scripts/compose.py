#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compose.py — 上下拼接：上半原图 + 下半生成区 → 3:4 海报

模型一次出整张时，上半区经常被重绘。可靠做法是只生成下半区，再和原图程序化拼接。

用法：
    python compose.py --photo IMG_001.jpg --lower lower_001.png --out poster_001.jpg
    python compose.py --photo a.jpg --lower b.png --ratio 46 --out c.jpg     # 黏土类 46:54
    python compose.py --photo a.jpg --lower b.png --mode blur --out c.jpg    # 横图：完整构图 + 模糊延展
    python compose.py --photo a.jpg --lower b.png --trim-top 2 --out c.jpg   # 去掉下半区顶端暗角
    python compose.py --photo a.jpg --lower b.png --dewm --out c.jpg         # 裁掉右下角工具水印

默认 50:50、宽 1440（输出 1440×1920，正好 3:4）。
**50:50 由构造保证**：画布高取偶数，上下各取 H//2，与模型无关。
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageEnhance
except ImportError:
    sys.exit("缺少 Pillow：pip install pillow")


def cover(img, w, h):
    """等比缩放后居中裁切，铺满 w×h。返回 (图, 裁切比例)"""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    cropped = (nw * nh - w * h) / (nw * nh)
    return resized.crop((left, top, left + w, top + h)), cropped


def contain(img, w, h, bg):
    """等比缩放后完整放进 w×h，空白用 bg 补"""
    iw, ih = img.size
    scale = min(w / iw, h / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    resized = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(resized, ((w - nw) // 2, (h - nh) // 2))
    return canvas


def edge_color(img, mode="bottom"):
    """取图片边缘的平均色，用于 contain 模式的补白"""
    w, h = img.size
    strip = img.crop((0, h - 4, w, h)) if mode == "bottom" else img.crop((0, 0, w, 4))
    strip = strip.convert("RGB").resize((1, 1), Image.LANCZOS)
    return strip.getpixel((0, 0))


def blur_extend(img, w, h):
    """原图完整显示，四周用自身放大模糊填充（不留白边，编辑设计常用手法）"""
    bg, _ = cover(img, w, h)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=max(w, h) / 18))
    bg = ImageEnhance.Brightness(bg).enhance(0.82)

    iw, ih = img.size
    scale = min(w / iw, h / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    if nw >= w and nh >= h:
        return bg
    fg = img.resize((nw, nh), Image.LANCZOS)
    canvas = bg.copy()
    canvas.paste(fg, ((w - nw) // 2, (h - nh) // 2))
    return canvas


def trim_corner(img, pct):
    """裁掉右侧与下侧同一比例，用于去掉出图工具固定在右下角的水印。
    两边裁同一比例，宽高比不变。"""
    w, h = img.size
    f = 1 - pct / 100
    return img.crop((0, 0, max(1, round(w * f)), max(1, round(h * f))))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description="上半原图 + 下半生成区 → 3:4 海报")
    p.add_argument("--photo", required=True, help="原始照片")
    p.add_argument("--lower", required=True, help="生成的下半区图（3:2 横版最佳）")
    p.add_argument("--out", required=True, help="输出路径")
    p.add_argument("--ratio", type=float, default=50.0,
                   help="上半区占画面高度的百分比，默认 50（黏土类用 46）")
    p.add_argument("--width", type=int, default=1440, help="输出宽度，默认 1440")
    p.add_argument("--mode", default="cover", choices=["cover", "blur", "contain"],
                   help="上半区适配方式：cover 裁切满幅（默认）/ blur 完整显示+模糊延展 / contain 完整显示+纯色留白")
    p.add_argument("--contain", action="store_true", help="等同于 --mode contain")
    p.add_argument("--bg", default="auto", help="contain 模式的补白色，默认取原图底边色")
    p.add_argument("--trim-top", type=float, default=0,
                   help="裁掉下半区顶部百分之几再接缝，用于去掉暗角/投影/贴边残留，默认 0")
    p.add_argument("--dewm", type=float, nargs="?", const=9.0, default=0,
                   help="裁掉生成图右侧与下侧各百分之几，去掉工具固定在右下角的水印；"
                        "不带数值时默认 9，宽高比不变")
    args = p.parse_args()

    if not 20 <= args.ratio <= 80:
        sys.exit("--ratio 应在 20~80 之间，否则一栏会薄得没法看")

    photo = Image.open(args.photo).convert("RGB")
    lower = Image.open(args.lower).convert("RGB")

    W = args.width
    H = round(W * 4 / 3)
    if H % 2:
        H += 1                      # 画布高取偶数，50:50 才能像素级相等
    if abs(args.ratio - 50) < 1e-9:
        Ht = H // 2                 # 严格二等分：不经过百分比浮点运算
    else:
        Ht = round(H * args.ratio / 100)
    Hb = H - Ht

    if 0 < args.dewm < 30:
        lower = trim_corner(lower, args.dewm)

    if 0 < args.trim_top < 40:
        lw, lh = lower.size
        t = round(lh * args.trim_top / 100)
        lower = lower.crop((0, t, lw, lh))

    mode = "contain" if args.contain else args.mode
    if mode == "contain":
        bg = edge_color(photo, "bottom") if args.bg == "auto" else args.bg
        top = contain(photo, W, Ht, bg)
        warn = "\n💡 纯色留白模式：如果左右白边太宽，换 --mode blur 会更好看。"
    elif mode == "blur":
        top = blur_extend(photo, W, Ht)
        warn = ""
    else:
        top, cut = cover(photo, W, Ht)
        warn = ""
        if cut > 0.15:
            warn = (f"\n⚠️  上半区裁掉了原图约 {cut:.0%} 的画面"
                    f"（原图 {photo.size[0]}×{photo.size[1]} 与 {W}×{Ht} 比例差得多）。\n"
                    f"   不想裁就加 --mode blur，或者把 --ratio 调小一点。")

    bottom, cut2 = cover(lower, W, Hb)
    if cut2 > 0.15:
        warn += (f"\n⚠️  下半区裁掉了生成图约 {cut2:.0%} 的画面。"
                 f"生成下半区时请按 {W}×{Hb}（约 3:{Hb/W*3:.2f}）出图。")

    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    canvas.paste(top, (0, 0))
    canvas.paste(bottom, (0, Ht))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    quality = 92
    if out.suffix.lower() in (".jpg", ".jpeg"):
        canvas.save(out, quality=quality, subsampling=0)
    else:
        canvas.save(out)

    print(f"✅ {out}  {W}×{H}  上 {Ht}px / 下 {Hb}px ({args.ratio:.0f}:{100-args.ratio:.0f})")
    if Ht == Hb:
        print(f"   中线精确在 {Ht / H * 100:.2f}%，上半区为原图像素，未经模型重绘")
    if warn:
        print(warn)


if __name__ == "__main__":
    main()
