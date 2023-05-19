###########################
# Control program example #
# 06.05.2021 Irene Woyna  #
###########################

import math
import os.path

timeCurrent = 0.0
timePrevious = 0.0
fluxPrevious = 0.0
fluxCurrent = 0.0
dFlux_dTime = 0.0

if os.path.exists("solution.ctl"):
    sln = open("solution.ctl", "r")
    find1 = False
    find2 = False
    for line in sln.readlines():
        tokens = line.split()
        if len(tokens) >= 2:
            if tokens[0] == 'time':
                find1 = True
                timeCurrent = float(tokens[1])
            elif tokens[0] == 'windingFlx':
                find2 = True
                fluxCurrent = float(tokens[2])
        if find1 and find2:
            break

if os.path.exists("previous.ctl"):
    prv = open("previous.ctl", "r")
    find1 = False
    find2 = False
    for line in prv.readlines():
        tokens = line.split()
        if len(tokens) >= 2:
            if tokens[0] == 'time':
                find1 = True
                timePrevious = float(tokens[1])
            elif tokens[0] == 'windingFlx':
                find2 = True
                fluxPrevious = float(tokens[2])
        if find1 and find2:
            break

dFlux = fluxCurrent - fluxPrevious
dTime = timeCurrent - timePrevious

if dTime > 0.0:
    dFlux_dTime = abs(dFlux)/abs(dTime)

ctl = open("user.ctl", "w")
ctl.write("begin_data\n")
ctl.write("windingSrc ")
voltage = 0.0
if timeCurrent > 5e-3:
    voltage = 10.0
ctl.write("Winding1 %e\n" % voltage)
ctl.write("timeStep ")
timeStep = 1e-3
if dFlux_dTime > 1.0e-6:
    timeStep = 1e-4
ctl.write("%e\n" % timeStep)
ctl.write("exportFieldAtMeshNodeOnAllObjects\n")
ctl.write("end_data\n")
ctl.close()
