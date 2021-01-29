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
        char_unicode = chr(y[0])
        char_name = y[1]
        if not char_name[0:3] == 'uni':
            if not char_name[0:4]=='afii':
                f = open(os.path.join(TEXTS_DIR, char_name + '.txt'), 'w')
                f.write(char_unicode)
                f.close()
ttf.close()

nums = ['zero','one','two','three','four','five','six','seven','eight','nine']
testString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
checkArray = [i for i in testString]

# edit this array for a different order of this stuff
checkArray2=['exclam','period','comma','ampersand','hyphen','questiondown','quotedblleft','quotedblright','percent','tilde',
    'parenleft','parenright','colon','acute']

check_char = "00000000000000000\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D>\x3F\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F"

testArray= nums+checkArray+checkArray2
files = os.listdir(TEXTS_DIR)
ctr = 0
files2 = files
# for filename in files2:
#     name, ext = os.path.splitext(filename)
#     input_txt = TEXTS_DIR + "/" + filename

#     if name in testArray:
#         ch = filename.split('.')[0]
#         ctr+=1

my_width = 64
my_height = 64

for i in range(len(check_char)):
    output_png = IMAGES_DIR + "/" + str(i) + ".png"
    from pathlib import Path
    Path(output_png).touch()
    # print(i)
    if i == 32:
        os.system(' '.join(["convert", "-interline-spacing 0", "-size %dx%d" % (my_width, my_height), "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(255,255,255,0\)","+antialias", "label:'\ '", output_png]))
    elif i == 34:
        os.system(' '.join(["convert", "-interline-spacing 0", "-size %dx%d" % (my_width, my_height), "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(255,255,255,0\)","+antialias", "label:'\"'", output_png]))
    elif i in[96]:
        os.system(' '.join(["convert", "-interline-spacing 0", "-size %dx%d" % (my_width, my_height), "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(255,255,255,0\)","+antialias","label:\\" + check_char[i], output_png]))
    elif i in[92]:
        os.system(' '.join(["convert", "-interline-spacing 0", "-size %dx%d" % (my_width, my_height), "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(255,255,255,0\)","+antialias","label:'\\\\'", output_png]))
    else:
        os.system(' '.join(["convert", "-interline-spacing 0", "-size %dx%d" % (my_width, my_height), "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(255,255,255,0\)","+antialias", "label:\"" + check_char[i]+"\"", output_png]))
    # else:
    #     files.remove(filename)

# ctr = 0
print([i for i in os.listdir(IMAGES_DIR) if os.path.isfile(IMAGES_DIR+"/"+i)])
print([i for i in os.listdir(IMAGES_DIR)])
for filename in [i for i in os.listdir(IMAGES_DIR) if os.path.isfile(IMAGES_DIR+"/"+i)]:
    name, ext = os.path.splitext(filename)
    ch = int(filename.split('.')[0])
    output_png = IMAGES_DIR + "/" + str(ch) + ".png"
    save_png = IMAGES_DIR + "/resized/" + str(ch) + ".png"
    print(output_png, save_png)
    # if name in check_char:
    f = Image.open(output_png)
    f_m = f.transpose(Image.FLIP_LEFT_RIGHT)
    f_r = f_m.rotate(90,expand=1)
    f_r2 = f_r.resize((16,8))
    f_m2 = f_r2.transpose(Image.FLIP_LEFT_RIGHT)
    f = f_m2.transpose(Image.FLIP_TOP_BOTTOM)
    # f_r2 = f.resize((32,32))
    w,h=f.size
    pA = f.load()
    # print(save_png)
    for i in range(0,w):
        for j in range(0,h):
            # print(pA[i,j])
            if pA[i,j]!=(0,0):
                pA[i,j]=(252,255)
                # pA[i,j]=(255-pA[i,j][0],pA[i,j][1])
    f.save(save_png)
    f.close()

print("finished")
