from bs4 import BeautifulSoup as bs
import os
import re
import requests

#Band="Queen"
Band="The-Rolling-Stones"


def check_songtext(hf, inputfile=True):
    from bs4 import BeautifulSoup as bs


    if inputfile:
        with open(hf, "r") as html_file:
            stext=html_file.read()
    else:
        stext=hf
    soup=bs(stext,"html.parser")
    
    songtext=soup.find('pre', {'id': 'lyric-body-text'})
    if songtext: 
        return True
    else:
        return False


if not os.path.isfile("Lyrics_home_"+Band+".html"):

    r = requests.get('https://www.lyrics.com/artist/'+Band)

    print(r.status_code)
    with open("Lyrics_home_"+Band+".html", "w") as f: 
        f.write(r.text)
    html_doc=r.text
else:
    with open("Lyrics_home_"+Band+".html", "r") as f:
         html_doc=f.read() 



soup = bs(html_doc, 'html.parser')


lyrics = {}

for link in soup.find_all('a'):
    if link['href'].startswith('/lyric'):  # only use links of lyrics
        if lyrics.get(link.text):
            lyrics[link.text].append("https://www.lyrics.com" + link['href'])
        else:
            lyrics[link.text] = ["https://www.lyrics.com" + link['href'],]



songlist=sorted(list(lyrics.keys()))


html_folder="./songs_html_"+Band+"/"
if not os.path.isdir(html_folder):
    os.system("mkdir -p "+html_folder)


import time

for i,title in enumerate(songlist):
    j=0
    print(i, "/", len(songlist))

    ftitle=title
    for char in [' ', '/', '\\', ',', '.', '!', '?']:
        ftitle = ftitle.replace(char, '')
    html_file=html_folder + ftitle + '.html'


    if os.path.isfile(html_file):
        if check_songtext(html_file):
            print(html_file, "already exists")
            continue
        else:
            print(html_file, " -------> does not contain lyrics")



    for url in lyrics[title]:
        print(" -------> access url ", url)

        time.sleep(1)
        print("get lyrics for song", title)
        response = requests.get(url)

        new_html_file=response.text

        if check_songtext(new_html_file, inputfile=False):
            with open(html_file, 'w') as response_file:
                response_file.write(new_html_file)
            break
        else:
            print(url, " -------> does not contain lyrics")
            continue 






