#!/usr/bin/env python3

import os


for level in range(1,51):
    cmd= "python3 sokoban.py -i "+ "level"+level+".sok"
    os.system(cmd)
    cmd2= "FD/fast-downward.py --plan-file myplan_" + level + ".txt --overall-time-limit 60  sokoban_domain.pddl output.pddl"
    os.system(cmd2)