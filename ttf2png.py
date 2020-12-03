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
testString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprstuvwxyz'
checkArray = [i for i in testString]

# edit this array for a different order of this stuff
checkArray2=['exclam','period','comma','ampersand','hyphen','questiondown','quotedblleft','quotedblright','percent','tilde',
    'parenleft','parenright','colon','acute']

testArray= nums+checkArray+checkArray2
files = os.listdir(TEXTS_DIR)
ctr = 0
for filename in files:
    name, ext = os.path.splitext(filename)
    input_txt = TEXTS_DIR + "/" + filename

    if name in testArray:
        ch = filename.split('.')[0]
        output_png = IMAGES_DIR + "/" + str(testArray.index(ch)) + ".png"
        os.system(' '.join(["convert", "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(0,0,0,0\)","+antialias", "label:$(cat " + input_txt+")", output_png]))
        ctr+=1
ctr = 0
for filename in files:
    name, ext = os.path.splitext(filename)
    output_png = IMAGES_DIR + "/" + TTF_NAME + "_" + name + "_" + FONT_SIZE + ".png"
    save_png = IMAGES_DIR + "/rotated/" + name  + ".png"
    if name in testArray:
        f = Image.open(output_png)
        w,h=f.size
        pA = f.load()
        print(save_png)
        f.save(save_png)
        f.close()

print("finished")
