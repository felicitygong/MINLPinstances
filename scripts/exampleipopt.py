from __future__ import division, print_function

import os, sys, csv
import time

import pyomo.environ
from pyomo.opt import SolverFactory
from cStringIO import StringIO

codefiles = ['convert.py', 'examplegbd.py', 'exampleoa.py', 'examplepsc.py', 'examplebaron.py', 'APSEHW6gbd.py', 'exampleipopt.py', 'portfol_buyin.py', 'portfol_card.py']
timetable = [['Instance', 'Time Elapsed']]
errortable = [['Instance', 'Error']]

for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name)
        try:
            newname = name + 'ipopt.txt'
            f = open(newname, "w+")
            f.write(filename + '\n')
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            filename1 = __import__(name)
            start = time.time()
            opt = SolverFactory('ipopt')
            opt.solve(filename1.m, timelimit=900, tee=True)
            end = time.time()
            sys.stdout = old_stdout
            f.write(mystdout.getvalue())
            f.write("\nTime elapsed: {}".format(end-start))
            f.close()
            timetable.append([filename, end-start])
        except Exception as inst:
            errortable.append([filename, inst])
            continue

with open('instancetableipopt.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]


with open('errortableipopt.csv', 'w+') as errors:
    writer2 = csv.writer(errors)
    [writer2.writerow(r) for r in errortable]