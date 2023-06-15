# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:45:10 2023

@author: slluka

Generating schotter art based on couple parameters and outputting gcode text file.

"""

import math
import random

import numpy as np
import cv2
import gcode

#Img Size
#img = np.zeros((2340, 1080, 1), np.uint8)
img = np.zeros((2340, 1080, 1), np.uint8)
#Img color?
img[:, :] = 255
squares = 13
squares_color = 0

write_gcode = True

def draw_angled_rec(x0, y0, width, height, angle, img, color, line_w):
    _angle = angle * math.pi / 180.0
    b = math.cos(_angle) * 0.5
    a = math.sin(_angle) * 0.5
    pt0 = (int(x0 - a * height - b * width),
           int(y0 + b * height - a * width))
    pt1 = (int(x0 + a * height - b * width),
           int(y0 - b * height - a * width))
    pt2 = (int(2 * x0 - pt0[0]), int(2 * y0 - pt0[1]))
    pt3 = (int(2 * x0 - pt1[0]), int(2 * y0 - pt1[1]))

    cv2.line(img, pt0, pt1, squares_color, line_w)
    cv2.line(img, pt1, pt2, squares_color, line_w)
    cv2.line(img, pt2, pt3, squares_color, line_w)
    cv2.line(img, pt3, pt0, squares_color, line_w)

    if write_gcode:
        gcode.write_G0(f, x=pt0[0]/10,y=pt0[1]/10)
        #Drop pen
        gcode.pen(f, 1)
        #Move
        gcode.write_G1(f, x=pt1[0]/10,y=pt1[1]/10,feedrate=500)
        gcode.write_G1(f, x=pt2[0]/10,y=pt2[1]/10,feedrate=500)
        gcode.write_G1(f, x=pt3[0]/10,y=pt3[1]/10,feedrate=500)
        gcode.write_G1(f, x=pt0[0]/10,y=pt0[1]/10,feedrate=500)
        #Lift Pen
        gcode.pen(f, 0)
        
    return img

f = gcode.start('novi_Test.txt', 'tu nekej napišem in bo v opombah')

lado_q = img.shape[1] / (squares+1)

emb = 0
for y in range(int(lado_q//2), img.shape[0]-int(lado_q), int(lado_q)):
    for x in range(int(lado_q//2), img.shape[1]-int(lado_q), int(lado_q)):
        img = draw_angled_rec(random.randint((x + lado_q // 2) - emb, (x + lado_q // 2) + emb),
                              random.randint((y + lado_q // 2) - emb, (y + lado_q // 2) + emb),
                              lado_q, lado_q,
                              random.uniform(float(f"-{emb}"), emb),
                              img, 0, 2)
    emb += random.randint(0, 3)

gcode.end(f)
# f.close()

cv2.imwrite("Lindomar Rodrigues, Schotter.png", img)