from bs4 import BeautifulSoup as bs

import os

Band="Queen"
Band="The-Rolling-Stones"

os.system("mkdir -p ./songs_txt_"+Band)
html_folder="./songs_html_"+Band+"/"


import glob
html_filelist=sorted(glob.glob(html_folder+"*.html"))

for hf in html_filelist:
    print(hf)

    with open(hf, "r") as html_file:
        stext=html_file.read()
    
    soup=bs(stext,"html.parser")
    
    songtext=soup.find('pre', {'id': 'lyric-body-text'})
    if songtext:
        with open(hf.replace("html", "txt"), 'w') as ofile:
            ofile.write(songtext.text)
 
