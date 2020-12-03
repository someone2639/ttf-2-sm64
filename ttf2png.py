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

testArray= nums+checkArray+checkArray2
files = os.listdir(TEXTS_DIR)
ctr = 0
files2 = files
for filename in files2:
    name, ext = os.path.splitext(filename)
    input_txt = TEXTS_DIR + "/" + filename

    if name in testArray:
        ch = filename.split('.')[0]
        output_png = IMAGES_DIR + "/" + str(testArray.index(ch)) + ".png"
        os.system(' '.join(["convert", "-interline-spacing 0", "-size 32x32", "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "rgba\(0,0,0,0\)","+antialias", "label:$(cat " + input_txt+")", output_png]))
        ctr+=1
    # else:
    #     files.remove(filename)

# ctr = 0
# for filename in files:
#     name, ext = os.path.splitext(filename)
#     ch = filename.split('.')[0]
#     output_png = IMAGES_DIR + "/" + str(testArray.index(ch)) + ".png"
#     save_png = IMAGES_DIR + "/resized/" + str(testArray.index(ch)) + ".png"
#     if name in testArray:
#         f = Image.open(output_png)
#         f_r2 = f.resize((32,32))
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
