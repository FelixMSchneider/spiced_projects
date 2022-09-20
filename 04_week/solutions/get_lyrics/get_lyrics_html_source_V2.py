import bs4 as bs
import os
import re
import requests

Band="Queen"
#Band="The-Rolling-Stones"



if not os.path.isfile("Lyrics_home_"+Band+".html"):

    r = requests.get('https://www.lyrics.com/artist/'+Band)

    print(r.status_code)
    with open("Lyrics_home_"+Band+".html", "w") as f: 
        f.write(r.text)
    html_doc=r.text
else:
    with open("Lyrics_home_"+Band+".html", "r") as f:
         html_doc=f.read() 



soup = bs.BeautifulSoup(html_doc, 'html.parser')


lyrics = {}

for link in soup.find_all('a'):
    if link['href'].startswith('/lyric'):  # only use links of lyrics
        lyrics[link.text] = "https://www.lyrics.com" + link['href']






songlist=list(lyrics.keys())


html_folder="./songs_html_"+Band+"/"
if not os.path.isdir(html_folder):
    os.system("mkdir -p "+html_folder)


import time

for i,title in enumerate(songlist):
    print(i, "/", len(songlist))
    ftitle=title
    for char in [' ', '/', '\\', ',', '.', '!', '?']:
        ftitle = ftitle.replace(char, '')

    html_file=html_folder + ftitle + '.html'


    if os.path.isfile(html_file):
        print(html_file, "already exists")
        continue

    time.sleep(1)
    print("get lyrics for song", title)
    print("access: "+lyrics[title])
    response = requests.get(lyrics[title])

    with open(html_file, 'w') as response_file:
        response_file.write(response.text)


#    lyric_soup=bs.BeautifulSoup(response.text,"html.parser")
#    songtext=lyric_soup.find('pre', {'id': 'lyric-body-text'}).text
#    with open(title + '.txt', 'w') as ofile:
#        ofile.write(songtext)
         


