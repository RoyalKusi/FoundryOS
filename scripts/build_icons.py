#!/usr/bin/env python3
"""Generate Android + iOS icons."""
from generate_logo import create_app_icon, draw_f_monogram, draw_sparkle
from generate_assets import create_lockup, create_splash
from pathlib import Path
from PIL import Image, ImageDraw
APP = Path(__file__).parent.parent / "app"
BRANDING = APP / "assets" / "branding"
ICON_DIR = APP / "assets" / "icon"
INDIGO_LIGHT=(79,70,229)

def gen():
    BRANDING.mkdir(parents=True, exist_ok=True)
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating 1024...")
    icon1024=create_app_icon(1024)
    icon1024.save(BRANDING/"app_icon.png","PNG")
    icon1024.save(ICON_DIR/"app_icon.png","PNG")
    (APP/"assets"/"icon"/"app_icon.png").parent.mkdir(parents=True, exist_ok=True)
    icon1024.save(APP/"assets"/"icon"/"app_icon.png","PNG")
    print(" lockups...")
    create_lockup(1024,320,False).save(BRANDING/"logo_light.png","PNG")
    create_lockup(1024,320,True).save(BRANDING/"logo_dark.png","PNG")
    print(" splash...")
    create_splash(1284,2778,False).save(BRANDING/"splash.png","PNG")
    create_splash(1284,2778,True).save(BRANDING/"splash_dark.png","PNG")
    print(" mipmap...")
    mipmap={"mipmap-mdpi":48,"mipmap-hdpi":72,"mipmap-xhdpi":96,"mipmap-xxhdpi":144,"mipmap-xxxhdpi":192}
    android_res=APP/"android"/"app"/"src"/"main"/"res"
    for folder,size in mipmap.items():
        out=android_res/folder; out.mkdir(parents=True, exist_ok=True)
        icon=create_app_icon(size)
        icon.save(out/"ic_launcher.png","PNG")
        icon.save(out/"ic_launcher_round.png","PNG")
        bg=Image.new("RGBA",(size,size),INDIGO_LIGHT+(255,))
        bg.save(out/"ic_launcher_background.png","PNG")
        fg=Image.new("RGBA",(size,size),(0,0,0,0))
        d=ImageDraw.Draw(fg,"RGBA")
        fw,fh=int(size*0.55),int(size*0.60)
        fx,fy=(size-fw)//2,(size-fh)//2
        draw_f_monogram(d,(fx,fy,fx+fw,fy+fh),0.18)
        draw_sparkle(d,(int(size*0.78),int(size*0.22)),int(size*0.035))
        fg.save(out/"ic_launcher_foreground.png","PNG")
    create_app_icon(512).save(BRANDING/"playstore_512.png","PNG")
    print(" iOS...")
    ios_iconset=APP/"ios"/"Runner"/"Assets.xcassets"/"AppIcon.appiconset"
    ios_iconset.mkdir(parents=True, exist_ok=True)
    ios_targets={"Icon-App-20x20@1x.png":20,"Icon-App-20x20@2x.png":40,"Icon-App-20x20@3x.png":60,"Icon-App-29x29@1x.png":29,"Icon-App-29x29@2x.png":58,"Icon-App-29x29@3x.png":87,"Icon-App-40x40@1x.png":40,"Icon-App-40x40@2x.png":80,"Icon-App-40x40@3x.png":120,"Icon-App-60x60@2x.png":120,"Icon-App-60x60@3x.png":180,"Icon-App-76x76@1x.png":76,"Icon-App-76x76@2x.png":152,"Icon-App-83.5x83.5@2x.png":167,"Icon-App-1024x1024@1x.png":1024}
    for name,size in ios_targets.items():
        icon=create_app_icon(size)
        bg=Image.new("RGBA",(size,size),(255,255,255,255))
        bg.alpha_composite(icon)
        bg.convert("RGB").save(ios_iconset/name,"PNG")
    (ios_iconset/"Contents.json").write_text('{"images":[{"size":"20x20","idiom":"iphone","filename":"Icon-App-20x20@2x.png","scale":"2x"},{"size":"20x20","idiom":"iphone","filename":"Icon-App-20x20@3x.png","scale":"3x"},{"size":"29x29","idiom":"iphone","filename":"Icon-App-29x29@1x.png","scale":"1x"},{"size":"29x29","idiom":"iphone","filename":"Icon-App-29x29@2x.png","scale":"2x"},{"size":"29x29","idiom":"iphone","filename":"Icon-App-29x29@3x.png","scale":"3x"},{"size":"40x40","idiom":"iphone","filename":"Icon-App-40x40@1x.png","scale":"1x"},{"size":"40x40","idiom":"iphone","filename":"Icon-App-40x40@2x.png","scale":"2x"},{"size":"40x40","idiom":"iphone","filename":"Icon-App-40x40@3x.png","scale":"3x"},{"size":"60x60","idiom":"iphone","filename":"Icon-App-60x60@2x.png","scale":"2x"},{"size":"60x60","idiom":"iphone","filename":"Icon-App-60x60@3x.png","scale":"3x"},{"size":"20x20","idiom":"ipad","filename":"Icon-App-20x20@1x.png","scale":"1x"},{"size":"20x20","idiom":"ipad","filename":"Icon-App-20x20@2x.png","scale":"2x"},{"size":"29x29","idiom":"ipad","filename":"Icon-App-29x29@1x.png","scale":"1x"},{"size":"29x29","idiom":"ipad","filename":"Icon-App-29x29@2x.png","scale":"2x"},{"size":"40x40","idiom":"ipad","filename":"Icon-App-40x40@1x.png","scale":"1x"},{"size":"40x40","idiom":"ipad","filename":"Icon-App-40x40@2x.png","scale":"2x"},{"size":"76x76","idiom":"ipad","filename":"Icon-App-76x76@1x.png","scale":"1x"},{"size":"76x76","idiom":"ipad","filename":"Icon-App-76x76@2x.png","scale":"2x"},{"size":"83.5x83.5","idiom":"ipad","filename":"Icon-App-83.5x83.5@2x.png","scale":"2x"},{"size":"1024x1024","idiom":"ios-marketing","filename":"Icon-App-1024x1024@1x.png","scale":"1x"}],"info":{"author":"xcode","version":1}}')
    print("Done!")

if __name__=="__main__":
    gen()
