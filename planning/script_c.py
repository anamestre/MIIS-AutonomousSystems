#!/usr/bin/env python3

import os


for level in range(1, 51):
    print("\n ------------------------------------------ LEVEL: " + str(level) + "\n")
    cmd= "python3 sokoban.py -i "+ "benchmarks/sasquatch/level"+ str(level)+".sok"
    os.system(cmd)
    #cmd2= "FD/fast-downward.py --plan-file myplan_" + str(level) + ".txt --overall-time-limit 60  sokoban_domain.pddl output.pddl"
    #os.system(cmd2)