import bs4 as bs
import os
import re

Band="Queen"
Band="The-Rolling-Stones"


urlfile="urllist_"+Band+".txt"

if not os.path.isfile(urlfile):
    print("run first get_lyrics_html_source.py")
    import sys
    sys.exit(-1)
else:
    with open(urlfile, "r") as f:
         urls=f.readlines() 


songs=sorted(list(set([u.split("/")[-1].split("\n")[0].lower() for u in urls])))


for song in songs:
    print(song)



