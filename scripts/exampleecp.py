from __future__ import division, print_function

import os, sys, csv
import subprocess
import time

import pyomo.environ
from pyomo.opt import SolverFactory
from cStringIO import StringIO

codefiles = ['fac1.py','portfol_buyin.py','portfol_card.py','batchs101006m.py','batchs121208m.py']
timetable = [['Instance', 'Time Elapsed']]

os.chdir('/home/felicitg/MINLPinstances/py')
sys.path.append(os.getcwd())

for filename in sorted(os.listdir('.')):
    # Only do things with .py files
    if filename.endswith('.py') and filename not in codefiles:
        name = os.path.splitext(filename)[0]
        print(name)
        newname = name + 'ecp.txt'
        f = open(newname, "w+")
        f.write(filename + '\n')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        filename1 = __import__(name)
        start = time.time()
        SolverFactory('mindtpy').solve(filename1.m, strategy='ECP')
        end = time.time()
        sys.stdout = old_stdout
        f.write(mystdout.getvalue())
        f.write("\nTime elapsed: {}".format(end-start))
        f.close()
        timetable.append([filename, end-start])
        subprocess.call(['mv '+ newname + ' ../ecpresults'],shell=True)

subprocess.call(['cd ../ecpresults'])
with open('1-instancetableecp.csv', 'w+') as table:
    writer = csv.writer(table)
    [writer.writerow(r) for r in timetable]