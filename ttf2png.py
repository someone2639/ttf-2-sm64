#!/usr/bin/env python3
import sys
import os
import subprocess
import numpy as np

from PIL import Image
from fontTools.ttLib import TTFont

# xd = str(input("Delete texts and images directory? This will clean up the results for you (Y/n): "))
# if xd == 'y' or xd=='Y' or xd=='':
# subprocess.call("rm -rf texts")
# subprocess.call("rm -rf images")

TEXTS_DIR = "texts"
IMAGES_DIR = "images"

if len(sys.argv) == 1:
    print("ttf2png.py (path to TTF file) (font size)")
    exit()

TTF_PATH = sys.argv[1]
FONT_SIZE = sys.argv[2]
TTF_NAME, TTF_EXT = os.path.splitext(os.path.basename(TTF_PATH))

ttf = TTFont(TTF_PATH, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)

for d in [TEXTS_DIR, IMAGES_DIR]:
    if not os.path.isdir(d):
        os.mkdir(d)

for x in ttf["cmap"].tables:
    for y in x.cmap.items():
        char_unicode = unichr(y[0])
        char_utf8 = char_unicode.encode('utf_8')
        char_name = y[1]
        if not char_name[0:3] == 'uni':
            if not char_name[0:4]=='afii':
                f = open(os.path.join(TEXTS_DIR, char_name + '.txt'), 'w')
                f.write(char_utf8)
                f.close()
ttf.close()
testString = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
checkArray = [i for i in testString]
checkArray2=['zero','one','two','three','four','five','six','seven','eight','nine','exclam','period','comma','ampersand','hyphen','questiondown','quotedblleft','quotedblright','percent','tilde',
    'parenleft','parenright','colon','acute']
testArray= checkArray+checkArray2
files = os.listdir(TEXTS_DIR)
for filename in files:
    name, ext = os.path.splitext(filename)
    input_txt = TEXTS_DIR + "/" + filename
    output_png = IMAGES_DIR + "/" + TTF_NAME + "_" + name + "_" + FONT_SIZE + ".png"
    # f = open(output_png,"w+")
    # f.close()
    if name in testArray:
        subprocess.call(["convert", "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba(0,0,0,0)","+antialias", "label:@" + input_txt, output_png])



for filename in files:
    name, ext = os.path.splitext(filename)
    output_png = IMAGES_DIR + "/" + TTF_NAME + "_" + name + "_" + FONT_SIZE + ".png"
    save_png = IMAGES_DIR + "/rotated/" + name  + ".png"
    if name in testArray:
        f = Image.open(output_png)
        f_m = f.transpose(Image.FLIP_LEFT_RIGHT)
        f_r = f_m.rotate(90,expand=1)
        f_r2 = f_r.resize((16,8))
        f_m2 = f_r2.transpose(Image.FLIP_LEFT_RIGHT)
        f = f_m2.transpose(Image.FLIP_TOP_BOTTOM)
        w,h=f.size
        pA = f.load()
        print(save_png)
        for i in range(0,w):
            for j in range(0,h):
                print(pA[i,j])
                if pA[i,j]!=(0,0):
                    pA[i,j]=(252,255)
                    # pA[i,j]=(255-pA[i,j][0],pA[i,j][1])
        f.save(save_png)
        f.close()

# for filename in files:
#     name, ext = os.path.splitext(filename)
#     save_png = IMAGES_DIR + "/rotated/" + name  + ".png"
#     if name in testArray:
#         f = Image.open(save_png)
#         w,h=f.size
#         pA = f.load()
#         print(save_png)
#         for i in range(0,w):
#             for j in range(0,h):
#                 print(pA[i,j])
#                 if pA[i,j]!=(0,0):
#                     pA[i,j]=(252,255)
#                     # pA[i,j]=(255-pA[i,j][0],pA[i,j][1])
#         f.save(save_png)
#         f.close()


print("finished")
