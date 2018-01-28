from __future__ import division, print_function

import os, sys, csv
import subprocess
import time

import pyomo.environ
from pyomo.opt import SolverFactory
from cStringIO import StringIO

codefiles = [
    'APSEHW6.py',
    'batchdes.py',
    'batchs101006m.py',
    'batchs121208m.py',
    'batchs151208m.py',
    'batchs201210m.py',
    'clay0203h.py',
    'clay0303h.py',
    'clay0304h.py',
    'clay0305h.py',
    'enpro56pb.py',
    'fac1.py',
    'flay05h.py',
    'flay05m.py',
    'flay06h.py',
    'flay06m.py',
    'fo7.py',
    'fo7_2.py',
    'fo8.py',
    'fo9.py',
    'gams01.py',
    'ibs2.py',
    'o7.py',
    'o7_2.py',
    'ravempb.py',
    'portfol_buyin.py',
    'portfol_card.py',
    'sssd15-04.py']
    #APSEHW6 error different, gurobi
    #works with flays and fos and o7, but takes foever (hours)
timetable = [['Instance', 'Time Elapsed']]

os.chdir('/home/felicitg/MINLPinstances/py')
sys.path.append(os.getcwd())

for filename in sorted(os.listdir('/home/felicitg/MINLPinstances/py')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + 'psc.txt'
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        start = time.time()
        SolverFactory('mindtpy').solve(filename1.m, strategy='PSC')
        end = time.time()
        sys.stdout = old_stdout
        f.write(mystdout.getvalue())
        f.write("\nTime elapsed: {}".format(end-start))
        f.close()
        timetable.append([filename, end-start])
        subprocess.call(['mv '+ newname + ' ../pscresults'],shell=True)

subprocess.call(['cd ../pscresults'])
with open('1-instancetablepsc.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]