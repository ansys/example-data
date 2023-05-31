###########################
# Control program example #
# 06.05.2021 Irene Woyna  #
###########################

import math
import os.path

time = 0.0

if os.path.exists("solution.ctl"):
    sln = open("solution.ctl", "r")
    find1 = False
    for line in sln.readlines():
        tokens = line.split()
        if len(tokens) >= 2:
            if tokens[0] == 'time':
                find1 = True
                time = float(tokens[1])
        if find1:
            break

ctl = open("user.ctl", "w")
ctl.write("begin_data\n")
ctl.write("windingSrc ")
voltage = 0.0
if time > 5e-3:
    voltage = 10.0
ctl.write("Winding1 %e\n" % voltage)
ctl.write("end_data\n")
ctl.close()
