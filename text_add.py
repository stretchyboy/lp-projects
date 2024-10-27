# draw_text_default_font.py

from PIL import Image, ImageDraw, ImageFont
import argparse
from stickframe import StickFrame, StickFramePlayer
from pathlib import Path
import json

import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    



parser = argparse.ArgumentParser(
                    prog='Text Add',
                    description='Text Add',
                    epilog='Text at the bottom of help')

parser.add_argument('--text', default="Default", type=str)
parser.add_argument('--font', default="Default", type=str)
parser.add_argument('--height', default=100, type=int)  

args = parser.parse_args()
print("args", args)

def getFont(fontname, fontsize):
    #fonts/Knewave-Regular.ttf
    #fonts/CaveatBrush-Regular.ttf
    #BungeeSpice-Regular.ttf
    try:
        return ImageFont.truetype(f"fonts/{fontname}-Regular.ttf", size=144)
    except Exception:
        return ImageFont.load_default(size=144)

def text(output_path,txt, heightCM, fontname="Default"):
    fontsize = int(StickFrame.height * (heightCM/100))
    print("height", fontsize, "heightCM", heightCM)



    framepath = "frames.json"

    framefile = open(framepath, 'r')
    stickdata = json.load(framefile)
    

    fontname = args.font
    font = getFont(fontname, fontsize)
   


    path = Path('data/categories/Text/anim')
    path.mkdir(parents=True, exist_ok=True)
    category = "Text"
    name = clean_filename(f"{txt}_{fontname}_{fontsize}")


    if category not in stickdata:
        stickdata[category] = {}
    if name not in stickdata[category]:
        stickdata[category][name] = []
    stickdata[category][name] = {
        "name":name,
        "category": category,
        "source": fontname,
        "frames": 1,
        "heightCM": heightCM,
        "direction": "right",
    }
    
    




    #if(fontname != "Default"):
    #    font = ImageFont.load(size=fontsize)
        
    s = font.getbbox(txt)#.getsize(txt, size=fontsize) 
    print("s", s)
    image = Image.new("RGB", size=(s[2], s[3]), color="white")

    draw = ImageDraw.Draw(image)
    draw.text((0,0), txt, font=font, size=(s[2], s[3]), fill="black")

    stick = StickFrame(image, category = "Text", name = name, frame=1, height=fontsize, heightCM=heightCM)
    
    # FIXME : If text is just a catergory make sure everythign get saved in the correct place. 
    #path = Path('data/text/'+txt+'/'+fontname+"/"+str(fontsize))
    path.mkdir(parents=True, exist_ok=True)

    framefile = open(framepath, 'w')
    json.dump(stickdata, framefile, sort_keys=True, indent=2)
    
    framefile2 = open('data/categories.json', 'w')
    json.dump(list(stickdata.keys()), framefile2, sort_keys=True, indent=2)

    framefile2 = open('data/categories.json', 'w')
    json.dump(list(stickdata.keys()), framefile2, sort_keys=True, indent=2)
    
    categoryfile = open('data/categories/Text.json','w')
    json.dump(list(stickdata["Text"].keys()), categoryfile, sort_keys=True, indent=2)
    
    animfile = open('data/categories/Text/anim/'+name+'.json','w')
    json.dump(stickdata["Text"][name], animfile, sort_keys=True, indent=2)



    image.save(output_path)

if __name__ == "__main__":
    heightCM = args.height
    text("text.png", args.text, heightCM)