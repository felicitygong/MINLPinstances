from __future__ import division, print_function

import os, sys, csv
import subprocess
import time

import pyomo.environ
from pyomo.opt import SolverFactory
from cStringIO import StringIO

codefiles = ['fac1.py','portfol_buyin.py','portfol_card.py']
timetable = [['Instance', 'Time Elapsed']]
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDir = os.path.join(fileDir, '../py')
os.chdir(fileDir)
sys.path.append(os.getcwd())
for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name) 
        newname = name + '_baron.txt'
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        start = time.time()
        opt = SolverFactory('baron')
        # opt.solve(filename1.m, timelimit=900, tee=True)
        end = time.time()
        sys.stdout = old_stdout
        f.write(mystdout.getvalue())
        f.write("\nTime elapsed: {}".format(end-start))
        f.close()
        timetable.append([filename, end-start])
        subprocess.call(['mv '+ newname + ' ../baronresults'],shell=True)

with open('1-instancetablebaron.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]
subprocess.call(['mv 1-instancetablebaron.csv ../baronresults'],shell=True)