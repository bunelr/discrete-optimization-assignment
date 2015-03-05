#!/usr/bin/python

import os
import sys

path = ""

fwresult = [value.split(" ") for value in open(path+"fw.txt").read().split("\n")[:-1]]

bfresult = [open(path+"bf"+str(i)+".txt").read().split("\n")[-2].split(" ") for i in range(0,304)]

dijresult = [open(path+"dijkstra"+str(i)+".txt").read().split("\n")[-2].split(" ") for i in range(0,304)]

print "bf == fw"
print bfresult == fwresult
print
print "dijkstra == fw"
print fwresult == dijresult
print
print "bf == dijkstra"
print bfresult == dijresult
print
