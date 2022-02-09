#!/usr/bin/env python3

# BRAND NEW
import sys
import os
# os.mkdir("images", exist_ok=True)
os.makedirs("images", exist_ok=True)

from PIL import Image, ImageDraw, ImageChops, ImageFont
from LUT import decompFontLUT

# switch to "Decomp" for S2DEX Text Engine conversion
Mode = "Dialog"
canvW = 8
canvH = 16
resizeW = 8
resizeH = 16


image = Image.new("LA", (canvW, canvH))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(sys.argv[1], int(sys.argv[2]))
charset = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789%~-&!?.,():'“”"


def fixImage(img):
    w, h = img.size
    pA = img.load()
    # print(save_png)
    for i in range(0,w):
        for j in range(0,h):
            # print(pA[i,j])
            if pA[i,j][0] > 127:
                pA[i,j]=(252, 255)

for x in charset:
    draw.text((0, 0), x, font=font, color="white")

    f_m = image.transpose(Image.FLIP_LEFT_RIGHT)
    f_r = f_m.rotate(90,expand=1)
    f_r2 = f_r.resize((resizeH,resizeW))
    f_m2 = f_r2.transpose(Image.FLIP_LEFT_RIGHT)
    f = f_m2.transpose(Image.FLIP_TOP_BOTTOM)

    fixImage(f)

    f.save("images/%s.png" % decompFontLUT[x])

    image = Image.new("LA", (canvW, canvH))
    draw = ImageDraw.Draw(image)
