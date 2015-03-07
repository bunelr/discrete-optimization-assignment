#!/usr/bin/python

import os
import sys

groundTruth = []
for line in  open("groundTruth.txt").read().strip().split("\n"):
    groundTruth.append([float(val) for val in line.split()])

fwresult = []
for line in  open("fw.txt").read().strip().split("\n"):
    fwresult.append([float(val) for val in line.split()])

bfresult = []
for i in range(304):
    bfresult.append([float(val) for val in open("bf"+str(i)+".txt").read().strip().split("\n")[-1].split()])

dijresult = []
for i in range(304):
    dijresult.append([float(val) for val in open("dijkstra"+str(i)+".txt").read().strip().split("\n")[-1].split() ])

if not (bfresult == groundTruth):
    print "[ERROR]: Your Bellman-Ford results are incorrect"
    sys.exit(1)
if not (fwresult == groundTruth):
    print "[ERROR]: Your Floyd-Warshall results are incorrect"
    sys.exit(1)
if not (dijresult == groundTruth):
    print "[ERROR]: Your Dijkstra results are incorrect"
    sys.exit(1)
