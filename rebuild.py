import os
import filecmp
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path

framepath = "frames.json"

framefile = open(framepath, 'r')
stickdata = json.load(framefile)


def restoreFrame(category, name, filename):
    path = Path('data/categories/'+category+'/anim')
    path.mkdir(parents=True, exist_ok=True)

    framefile2 = open('data/categories.json', 'w')
    json.dump(list(stickdata.keys()), framefile2, sort_keys=True, indent=2)
    
    categoryfile = open('data/categories/'+category+'.json','w')
    json.dump(list(stickdata[category].keys()), categoryfile, sort_keys=True, indent=2)
    
    animfile = open('data/categories/'+category+'/anim/'+name+'.json','w')
    json.dump(stickdata[category][name], animfile, sort_keys=True, indent=2)


for category, anim in stickdata.items():
    print("category", category)
    for animname, items in anim.items():
        print("  animname", animname)
        for filename in items:
            print("    filename", filename) 
            restoreFrame(category, animname, filename)        
