#!/usr/bin/python

import os
import sys

groundTruth = []
for line in  open("groundTruth.txt").read().split("\n")[:-1]:
    groundTruth.append([float(val) for val in line.split()])

fwresult = []
for line in  open("fw.txt").read().split("\n")[:-1]:
    fwresult.append([float(val) for val in line.split()])

bfresult = []
for i in range(0,304):
    bfresult.append([float(val) for val in open("bf"+str(i)+".txt").read().split("\n")[-2].split()])

dijresult = []
for i in range(0, 304):
    dijresult.append([float(val) for val in open("dijkstra"+str(i)+".txt").read().split("\n")[-2].split() ])

if not (bfresult == groundTruth):
    print "bf error"
    sys.exit(1)
if not (fwresult == groundTruth):
    print "fw error"
    sys.exit(1)
if not (dijresult == groundTruth):
    print "dijresult"
    sys.exit(1)
