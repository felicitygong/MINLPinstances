from __future__ import division, print_function

import os, sys, csv
import subprocess
import time, datetime

import pyomo.contrib.mindtpy.MindtPy
from pyomo.environ import SolverFactory, value
from io import StringIO

problemfiles = ['clay0204h.py',
                'clay0205h.py',
                'clay0305h.py',
                'fac1.py',
                'portfol_buyin.py',
                'portfol_card.py',
		'batch0812.py',
		'ibs2.py',
                'watercontamination0202.py',
                'watercontamination0202r.py',
                'watercontamination0303.py',
                'watercontamination0303.py',
		'squfl020-150'
                ]
#skipexisting = 1
timetable = [['Instance', 'Time Elapsed']]
errortable = [['Instance', 'Error']]
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDir = os.path.join(fileDir, '../py')
os.chdir(fileDir)
sys.path.append(os.getcwd())
solvername = 'oa'
for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in problemfiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + '_'+solvername+'.txt'
        #if os.path.exists('../'+solvername+'results/'+newname) and skipexisting == 1:
            #pass
        #else:
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        dt = datetime.date
        start = time.time()
        #try:
        SolverFactory('mindtpy').solve(filename1.m, strategy='OA', iteration_limit=10)
        end = time.time()
        sys.stdout = old_stdout
        f.write(mystdout.getvalue())
        deltat = end-start
        f.write("\nTime elapsed: {}".format(dt))
        f.close()
        timetable.append([filename, end-start])
        subprocess.call(['mv '+ newname + ' ../'+solvername+'results'],shell=True)
        trcdata  = filename+', MindtPy, IPOPT, Gurobi'+ str(dt) + ', 0, eqnum?, varnum?, dvarnum?, nznum?, nlnz?, 0, modelstatus?, solvestatus?,'+str(value(filename1.m.obj)) +', objest?,'+str(deltat)+ ', 5, domviolations, numnodes,' + 'user'   
        trcname = name + '_' + solvername + '.trc'
        with open(trcname, "w+") as trace:
            trace.write(trcdata)
        subprocess.call(['mv '+ trcname + ' ../'+solvername+'results'],shell=True)
        #except Exception as inst:
        #    errortable.append([filename, inst])
        #    continue


with open('1-instancetable'+solvername+'.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]

with open('2-errortable'+solvername+'.csv', 'w+') as errors:
    writer2 = csv.writer(errors)
    [writer2.writerow(r) for r in errortable]


subprocess.call(['mv 1-instancetable'+solvername+'.csv ../'+solvername+'results'],shell=True)
subprocess.call(['mv 2-errortable'+solvername+'.csv ../'+solvername+'results'],shell=True)
#value(filename1.m.obj)
