#!/usr/bin/env python3
"""
FoundryOS Logo Generator — creates PNG assets from vector spec.
Uses Pillow only. Run: python3 scripts/generate_logo.py
"""
import os, sys
from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
APP = ROOT / "app"
BRANDING = APP / "assets" / "branding"
ICON_DIR = APP / "assets" / "icon"

INDIGO_LIGHT = (79, 70, 229)
INDIGO_MID = (99, 102, 241)
INDIGO_DARK = (124, 116, 255)
WHITE = (255, 255, 255)
BG_LIGHT = (255, 255, 255)
BG_DARK = (0, 0, 0)

def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def gradient_image(size, c1=INDIGO_LIGHT, c2=INDIGO_DARK):
    w, h = size
    img = Image.new("RGB", size, c1)
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h)
            if t < 0.5:
                col = lerp(c1, INDIGO_MID, t*2)
            else:
                col = lerp(INDIGO_MID, c2, (t-0.5)*2)
            img.putpixel((x, y), col)
    return img

def squircle_mask(size, radius_factor=0.273):
    w, h = size
    r = int(min(w, h) * radius_factor * 1.2)
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, w, h], radius=r, fill=255)
    return mask

def draw_f_monogram(draw, bbox, thickness_ratio=0.18):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0
    th = int(w * thickness_ratio)
    stem_w = th
    top_h = th
    mid_w = int(w * 0.68)
    mid_h = int(th * 0.88)
    radius = max(4, th // 5)
    # vertical stem
    draw.rounded_rectangle([x0, y0, x0+stem_w, y0+h], radius=radius, fill=WHITE)
    # top bar
    draw.rounded_rectangle([x0, y0, x0+w, y0+top_h], radius=radius, fill=WHITE)
    # middle bar
    mid_y = y0 + int(h * 0.32)
    draw.rounded_rectangle([x0, mid_y, x0+mid_w, mid_y+mid_h], radius=radius, fill=WHITE)

def draw_sparkle(draw, center, size=22):
    x, y = center
    s = size
    for r, alpha in [(36, 56), (28, 36)]:
        # simulate glow via ellipse
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255,255,255, alpha))
    pts = [(x, y-s), (x+s*0.25, y-s*0.25), (x+s, y), (x+s*0.25, y+s*0.25), (x, y+s), (x-s*0.25, y+s*0.25), (x-s, y), (x-s*0.25, y-s*0.25)]
    draw.polygon(pts, fill=WHITE)
    draw.ellipse([x-6, y-6, x+6, y+6], fill=WHITE)

def create_app_icon(size=1024):
    img = gradient_image((size, size))
    highlight = Image.new("RGBA", (size, size), (0,0,0,0))
    hd = ImageDraw.Draw(highlight, "RGBA")
    for y in range(size):
        alpha = int(46 * (1 - y/size) * 0.5)
        if alpha>0:
            hd.line([(0, y), (size, y)], fill=(255,255,255, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), highlight)
    mask = squircle_mask((size, size))
    img.putalpha(mask)
    draw = ImageDraw.Draw(img, "RGBA")
    fw = int(size * 0.48)
    fh = int(size * 0.52)
    fx = (size - fw)//2
    fy = (size - fh)//2
    draw_f_monogram(draw, (fx, fy, fx+fw, fy+fh), thickness_ratio=0.18)
    sx = int(size * 0.78)
    sy = int(size * 0.22)
    sparkle_size = int(size * 0.035)
    draw_sparkle(draw, (sx, sy), size=sparkle_size)
    border = Image.new("RGBA", (size, size), (0,0,0,0))
    bd = ImageDraw.Draw(border)
    r = int(size * 0.273 *1.2)
    bd.rounded_rectangle([0,0,size-1,size-1], radius=r, outline=(255,255,255,30), width=1)
    img = Image.alpha_composite(img, border)
    return img

