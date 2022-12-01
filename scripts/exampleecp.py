from __future__ import division, print_function

import os, sys, csv
import subprocess
import time, datetime

import pyomo.contrib.mindtpy.MindtPy
from pyomo.environ import SolverFactory, value
from io import StringIO

problemfiles = ['ex1223.py',
                'ex1223b.py',
                'fac1.py',
                'fac2.py',
                'fac3.py',
                'gams01.py',
                'meanvarx.py',
                'netmod_dol1.py',
                'netmod_dol2.py',
                'netmod_kar1.py',
                'netmod_kar2.py',
                'portfol_buyin.py',
                'portfol_card.py',
                'portfol_classical050_1.py',
                'portfol_classical200_2.py',
                'procurement2mot.py',
                'rsyn0805m03h.py',
                'rsyn0810m03h.py',
                'rsyn0810m04h.py',
                'rsyn0815m02h.py',
                'rsyn0815m04h.py',
                'rsyn0820h.py',
                'rsyn0820m02h.py',
                'rsyn0820m03h.py',
                'rsyn0820m04h.py',
                'squfl010-025.py',
                'squfl010-040.py',
                'squfl010-080.py',
                'squfl015-060.py',
                'squfl015-080.py',
                'squfl020-040.py',
                'squfl020-050.py',
                'squfl020-150.py',
                'squfl025-025.py',
                'squfl025-030.py',
                'squfl025-040.py',
                'squfl030-100.py',
                'squfl030-150.py',
                'squfl040-080.py',
                'st_e14.py',
                'syn15m02h.py',
                'syn15m03h.py',
                'syn20m02h.py',
                'syn20m03h.py',
                'syn20m04h.py',
                'syn30h.py',
                'syn30m02h.py',
                'syn40m02h.py',
                'unitcommit1.py'
               ]
#skipexisting = 1
timetable = [['Instance', 'Time Elapsed']]
errortable = [['Instance', 'Error']]
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDir = os.path.join(fileDir, '../py')
os.chdir(fileDir)
sys.path.append(os.getcwd())
solvername = 'ecp'
for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in problemfiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + '_'+solvername+'.txt'
        #if os.path.exists('../'+solvername+'results/'+newname) and skipexisting == 1:
        #    pass
        #else:
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        dt = datetime.date
        start = time.time()
        #try:
        SolverFactory('mindtpy').solve(filename1.m, strategy='ECP', iteration_limit=15)
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
