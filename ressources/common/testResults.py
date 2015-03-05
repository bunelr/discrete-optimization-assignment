#!/usr/bin/python

import os
import sys


groundTruth = [value.split(" ") for value in open("groundTruth.txt").read().split("\n")[:-1]]

fwresult = [value.split(" ") for value in open("fw.txt").read().split("\n")[:-1]]

bfresult = [open("bf"+str(i)+".txt").read().split("\n")[-2].split(" ") for i in range(0,304)]

dijresult = [open("dijkstra"+str(i)+".txt").read().split("\n")[-2].split(" ") for i in range(0,304)]

if not bfresult == groundTruth:
        return 1
if not fwresult == groundTruth:
        return 1
if not dijresult == groundTruth:
        return 1
