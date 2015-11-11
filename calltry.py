__author__ = 'shridharmanvi'
import pandas as pd
import random
from random import randint
import os
import sys
import subprocess

test_dat = pd.read_csv('mushroom_data.csv')


for i in range(0,4):
    rows = random.sample(test_dat.index, randint(30, 90))
    print len(rows)
    pass_data = test_dat.ix[rows]
    pass_data.to_csv('test_data.csv', index=False)

    dat = test_dat.iloc[i]
    subprocess.call('pwd')
    s2_out = subprocess.check_output([sys.executable, "dtree_final.py", "mushroom_data.csv"])
    #subprocess.call(['./dtree_final.py', 'test_data.csv'])
    #print [s2_out]
    l1=[]
    for j in s2_out:
        if j in ['e','p']:
            l1.append(j)

    print len(l1)
