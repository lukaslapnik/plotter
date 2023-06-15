# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 11:58:11 2023

@author: slluka
"""

import numpy as np
import cv2
import random
import gcode

#Mere v 0.1mm
size_x = 2930
size_y = 2100
offset_x = 265
offset_y = 250
nr_points_x = 20 #Zlomov linij
nr_points_y = 16 #Setov linij
nr_lines = 12 #Linij v vsakem setu
width = 3
rand = 1.0
write_feedrate = 600
generate_visual = False #Shoudl the script generate a jpg of what the art looks like

px_x = size_x-2*offset_x
px_y = size_y-2*offset_y
randrange_x = px_x/nr_points_x*rand
randrange_y = px_y/nr_points_y*rand


#Create image
img = np.zeros((size_y, size_x, 1), np.uint8)
img[:, :] = 255

img_detailed = np.zeros((size_y, size_x, 1), np.uint8)
img_detailed[:, :] = 255

points_x=np.linspace(0,0,nr_points_x*nr_points_y,dtype=int)
points_x.shape = (nr_points_y,nr_points_x)
points_y=np.linspace(0,0,nr_points_x*nr_points_y,dtype=int)
points_y.shape = (nr_points_y,nr_points_x)

for x in range(nr_points_x):
    for y in range(nr_points_y):
        points_x[y][x] = x*(px_x/(nr_points_x-1))+random.randint(-randrange_x, randrange_x) + offset_x
        points_y[y][x] = y*(px_y/(nr_points_y-1))+random.randint(-randrange_y, randrange_y) + offset_y
        center_coords = (points_x[y][x],points_y[y][x])
        cv2.circle(img, center_coords, 1, 0, 5)

nr_points_subx = nr_points_x
nr_points_suby = (nr_points_y-1)*nr_lines+1

points_subx=np.linspace(0,0,nr_points_subx*nr_points_suby,dtype=int)
points_subx.shape = (nr_points_suby,nr_points_subx)
points_suby=np.linspace(0,0,nr_points_subx*nr_points_suby,dtype=int)
points_suby.shape = (nr_points_suby,nr_points_subx)

f = gcode.start('novi_Test.txt', 'tu nekej napišem in bo v opombah')

# flag = False

for x in range(nr_points_x):
    for y in range(nr_points_y-1):
        dx = (points_x[y+1][x]-points_x[y][x])/nr_lines
        dy = (points_y[y+1][x]-points_y[y][x])/nr_lines
        for line in range(nr_lines):
            points_subx[y*nr_lines+line][x] = points_x[y][x] + dx*line
            points_suby[y*nr_lines+line][x] = points_y[y][x] + dy*line

            center_coords = (points_subx[y*nr_lines+line][x], points_suby[y*nr_lines+line][x])
            cv2.circle(img, center_coords, 1, 0, 1)
     
    #Add the last line
    points_subx[(nr_points_y-1)*nr_lines][x] = points_x[nr_points_y-1][x]
    points_suby[(nr_points_y-1)*nr_lines][x] = points_y[nr_points_y-1][x]

#Generate visual example in script directory

if generate_visual:
    for y in range(points_subx.shape[0]-1):
        for x in range(points_subx.shape[1]-1):
            print(x,y)
            pt1 = (points_subx[y][x], points_suby[y][x])
            pt2 = (points_subx[y][x+1], points_suby[y][x+1])
            cv2.line(img_detailed, pt1, pt2, 0, width)

for y in range(points_subx.shape[0]):
    line_start = True
    for x in range(points_subx.shape[1]):
        if line_start:
            gcode.write_G0(f, x=points_subx[y][x], y=points_suby[y][x])
            gcode.pen(f, 1)
            line_start = False
        else:
            gcode.write_G1(f, x=points_subx[y][x], y=points_suby[y][x], feedrate=write_feedrate)
    gcode.pen(f, 0)
        
gcode.end(f)

cv2.imwrite("ART.png", img) 
cv2.imwrite("ART_detailed.png", img_detailed)