from __future__ import division, print_function

import os, sys, csv
import time, subprocess

import pyomo.environ
from pyomo.opt import SolverFactory
from cStringIO import StringIO

codefiles = [
    'fac1.py',
    'portfol_buyin.py',
    'portfol_card.py',
    'APSEHW6.py',
    'batch.py',
    'batch0812.py',
    'batchdes.py',
    'batchs101006m.py',
    'batchs121208m.py',
    'batchs151208m.py',
    'batchs201210m.py',
    'clay0203h.py',
    'clay0203m.py',
    'clay0204h.py',
    'clay0204m.py',
    'clay0205h.py']
timetable = [['Instance', 'Time Elapsed']]

os.chdir('/home/felicitg/MINLPinstances/py')
sys.path.append(os.getcwd())

for filename in sorted(os.listdir('/home/felicitg/MINLPinstances/py')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + 'gbd.txt'
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        start = time.time()
        SolverFactory('mindtpy').solve(filename1.m, strategy='GBD')
        end = time.time()
        sys.stdout = old_stdout
        f.write(mystdout.getvalue())
        f.write("\nTime elapsed: {}".format(end-start))
        f.close()
        timetable.append([filename, end-start])
        subprocess.call(['mv '+ newname + ' ../gbdresults'],shell=True)

subprocess.call(['cd ../gbdresults'])
with open('1-instancetablegbd.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]