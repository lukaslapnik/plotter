# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 07:00:05 2023

@author: slluka

Functions for taking coordinate inputs and generating a text file with G-Code commands. 

"""

def start(filename, notes):
    f = open(filename, 'w').close()
    f = open(filename, "a")
    f.write("; Generated plotter gcode based on script")
    f.write("\n; Pause, let user move to position, wait for click, set XY as 0 and then start")
    if notes: f.write(f"\n; {notes}")
    return f

def end(f):
    f.write("\n; End code")
    f.write("\nM5\nM30")
    f.close()
    return

def write_G0(f, x='',y='',z=''):
    f.write("\n")
    f.write("G0")
    if x: f.write(f" X{x}")
    if y: f.write(f" Y{y}")
    if z: f.write(f" Z{z}")
    return

def write_G1(f, x='',y='',z='',feedrate=''):
    f.write("\n")
    f.write("G1")
    if x: f.write(f" X{x}")
    if y: f.write(f" Y{y}")
    if z: f.write(f" Z{z}")
    if feedrate: f.write(f" F{feedrate}")
    return

def pen(f, val=0):
    f.write("\n")
    if val==0: f.write("PEN UP")
    if val==1: f.write("PEN DOWN")
    return
