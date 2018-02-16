from __future__ import division, print_function

import os, sys, csv
import subprocess
import time

import pyomo.contrib.mindtpy.MindtPy
from pyomo.environ import SolverFactory, value
from cStringIO import StringIO

codefiles = ['fac1.py'
,'portfol_buyin.py'
,'portfol_card.py'
,'batch0812.py'
,'clay0203h.py'
,'clay0205h.py'
,'clay0303h.py'
,'clay0305h.py'
,'flay06h.py'
,'flay06m.py'
,'gams01.py']
skipexisting = 1
timetable = [['Instance', 'Time Elapsed']]
errortable = [['Instance', 'Error']]
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDir = os.path.join(fileDir, '../py')
os.chdir(fileDir)
sys.path.append(os.getcwd())
solvername = 'oa'
for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + '_'+solvername+'.txt'
        if os.path.exists('../'+solvername+'results/'+newname) and skipexisting == 1:
            pass
        else:
            f = open(newname, "w+")
            f.write(filename + '\n')
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            filename1 = __import__(name)
            start = time.time()
            try:
                SolverFactory('mindtpy').solve(filename1.m, strategy='OA')
                end = time.time()
                sys.stdout = old_stdout
                f.write(mystdout.getvalue())
                f.write("\nTime elapsed: {}".format(end-start))
                f.close()
                timetable.append([filename, end-start])
                subprocess.call(['mv '+ newname + ' ../'+solvername+'results'],shell=True)
            except Exception as inst:
                errortable.append([filename, inst])
                continue


with open('1-instancetable'+solvername+'.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]

with open('2-errortable'+solvername+'.csv', 'w+') as errors:
    writer2 = csv.writer(errors)
    [writer2.writerow(r) for r in errortable]


subprocess.call(['mv 1-instancetable'+solvername+'.csv ../'+solvername+'results'],shell=True)
subprocess.call(['mv 2-errortable'+solvername+'.csv ../'+solvername+'results'],shell=True)