from stickframe import StickFrame, StickFramePlayer
from PIL import Image, ImageDraw
import os
import filecmp
from copy import deepcopy
import argparse
import hashlib
import json

framepath = "frames.json"

# TODO : Add image by url
# TODO : Separate animated gifs
# TODO : Build index json  /frames.json
# TODO : Store on server /store/{hash}.json

framefile = open(framepath, 'r')
stickdata = json.load(framefile)


#stickdata = '''{'Default':[
#    {'name': 'de', 'files':['afghbfgdfsbnjnhtrfngh']},
#    {'name': 'fox', 'files':['jnthbrvcbrve', 'bgvfcdbtgervscdgr']},
#]}'''


# https://i.pinimg.com/originals/5b/19/d3/5b19d355d154388b45e4a8e3d01b16ae.gif


parser = argparse.ArgumentParser(
                    prog='Stick Frame File Add',
                    description='Add image to frames store',
                    epilog='Text at the bottom of help')


parser.add_argument('name')
parser.add_argument('path')
parser.add_argument('category', nargs='?', default="Default")           # positional argument     

args = parser.parse_args()
#print(args)

import shutil
import tempfile
import urllib.request
from urllib.parse import urlparse
import validators
from validators import ValidationError
from pathlib import Path


def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)

    if isinstance(result, ValidationError):
        return False

    return result

def storeFrame(category, name, filename):
    if category not in stickdata:
        stickdata[category] = {}
    if name not in stickdata[category]:
        stickdata[category][name] = []
    stickdata[category][name].append(filename)
    framefile = open(framepath, 'w')
    json.dump(stickdata, framefile, sort_keys=True, indent=2)

    path = Path('data/categories/'+category+'/anim')
    path.mkdir(parents=True, exist_ok=True)

    framefile2 = open('data/categories.json', 'w')
    json.dump(list(stickdata.keys()), framefile2, sort_keys=True, indent=2)
    
    categoryfile = open('data/categories/'+category+'.json','w')
    json.dump(list(stickdata[category].keys()), categoryfile, sort_keys=True, indent=2)
    
    animfile = open('data/categories/'+category+'/anim/'+name+'.json','w')
    json.dump(stickdata[category][name], animfile, sort_keys=True, indent=2)


filepath = None

if(is_string_an_url(args.path)):
    with urllib.request.urlopen(args.path) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
            filepath = tmp_file.name
            urlparts = urlparse(args.path)
            head, tail = os.path.split(urlparts.path)
            name, ext = os.path.splitext(tail)

else:
    filepath = args.path
    head, tail = os.path.split(filepath)
    name, ext = os.path.splitext(tail)

with Image.open(filepath) as im:
    exif = im.getexif()
    print("n_frames", getattr(im, "n_frames", 1))

    for k, v in exif.items():
        print("Tag", k, "Value", v)  

    #print(name)
    #print("im", im)
    framename = args.name
    if  framename == 'name':
        framename = name

    frames = getattr(im, "n_frames", 1)
    i = 1
    while i <= frames:
        stick = StickFrame(im)

        stick.compress()

        hashed_data = hashlib.sha256(stick.dumps().encode())
        stick.name = hashed_data.hexdigest()
        
        stick.dump()
        storeFrame(args.category, framename, stick.filename)    

        if i < frames:
            im.seek(i)
        
        i += 1
        