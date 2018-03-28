from __future__ import division, print_function

import os, sys, csv
import subprocess
import time, datetime

import pyomo.contrib.mindtpy.MindtPy
from pyomo.environ import SolverFactory, value
from cStringIO import StringIO

okfiles = ['APSEHW6.py',
           'anECPex.py'
           ]
problemfiles = ['alan.py',
                'batch.py',
                'batch0812.py',
                'batchdes.py'
                ]
skipexisting = 1
timetable = [['Instance', 'Time Elapsed']]
errortable = [['Instance', 'Error']]
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDir = os.path.join(fileDir, '../py')
os.chdir(fileDir)
sys.path.append(os.getcwd())
solvername = 'psc'
for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in problemfiles and filename not in okfiles:
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
            dt = datetime.date
            try:
                SolverFactory('mindtpy').solve(filename1.m, strategy='PSC')
                end = time.time()
                sys.stdout = old_stdout
                f.write(mystdout.getvalue())
                f.write("\nTime elapsed: {}".format(end-start))
                f.close()
                timetable.append([filename, end-start])
                subprocess.call(['mv '+ newname + ' ../'+solvername+'results'],shell=True)
                trcdata  = filename+', MindtPy, IPOPT, Gurobi'+ str(dt) + ', 0, eqnum?, varnum?, dvarnum?, nznum?, nlnz?, 0, modelstatus?, solvestatus?,'+str(value(filename1.m.obj)) +', objest?,'+str(end-start)+ ', 5, domviolations, numnodes,' + 'user'   
                trcname = name + '_' + solvername + '.trc'
                with open(trcname, "w+") as trace:
                    trace.write(trcdata)
                subprocess.call(['mv '+ trcname + ' ../'+solvername+'results'],shell=True)
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