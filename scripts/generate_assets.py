#!/usr/bin/env python3
"""FoundryOS asset generator — part 2: lockups & splash."""
from generate_logo import *
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
APP = Path(__file__).parent.parent / "app"
BRANDING = APP / "assets" / "branding"
ICON_DIR = APP / "assets" / "icon"
INDIGO_LIGHT = (79,70,229)
INDIGO_DARK = (124,116,255)
BG_LIGHT = (255,255,255)
BG_DARK = (0,0,0)

def create_lockup(width=1024, height=320, dark=False):
    bg = BG_DARK if dark else BG_LIGHT
    img = Image.new("RGBA", (width, height), bg+(255,))
    draw = ImageDraw.Draw(img)
    icon = create_app_icon(160)
    img.alpha_composite(icon, (32, (height-160)//2))
    try:
        f_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        f_reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 64)
        f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        f_bold=ImageFont.load_default(); f_reg=f_bold; f_small=f_bold
    tx, ty = 220, 100
    text_col = (245,245,247) if dark else (29,29,31)
    accent = INDIGO_DARK if dark else INDIGO_LIGHT
    draw.text((tx, ty), "Foundry", font=f_bold, fill=text_col)
    fw = draw.textlength("Foundry", font=f_bold)
    draw.text((tx+fw, ty), "OS", font=f_reg, fill=accent)
    tag_col = (154,154,160) if dark else (110,110,115)
    draw.text((tx, ty+70), "COMPANY OPERATING SYSTEM", font=f_small, fill=tag_col)
    return img

def create_splash(w=1284, h=2778, dark=False):
    bg = BG_DARK if dark else BG_LIGHT
    img = Image.new("RGBA", (w, h), bg+(255,))
    icon = create_app_icon(240)
    img.alpha_composite(icon, ((w-240)//2, (h-240)//2 -120))
    draw = ImageDraw.Draw(img)
    try:
        f_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        f_bold=ImageFont.load_default(); f_small=f_bold
    text_col = (245,245,247) if dark else (29,29,31)
    label="FoundryOS"; tw=draw.textlength(label, font=f_bold)
    draw.text(((w-tw)//2, (h//2)+40), label, font=f_bold, fill=text_col)
    tag="Company Operating System"; tw2=draw.textlength(tag, font=f_small)
    draw.text(((w-tw2)//2, (h//2)+80), tag, font=f_small, fill=(110,110,115))
    return img
