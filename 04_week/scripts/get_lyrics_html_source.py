import bs4 as bs
import os
import re

Band="Queen"
Band="The-Rolling-Stones"



if not os.path.isfile("Lyrics_home_"+Band+".html"):
    import requests

    r = requests.get('https://www.lyrics.com/artist/'+Band)

    print(r.status_code)
    with open("Lyrics_home_"+Band+".html", "w") as f: 
        f.write(r.text)
    html_doc=r.text
else:
    with open("Lyrics_home_"+Band+".html", "r") as f:
         html_doc=f.read() 



soup = bs.BeautifulSoup(html_doc, 'html.parser')
prettysoup=soup.prettify()


urllist=[]

reBand=re.sub("-", ".", Band)



for line in prettysoup.splitlines():
    if re.search(reBand, line, re.IGNORECASE) and re.search('<a href="/lyric/', line):
        wholeline=line
        url= "https://www.lyrics.com"+ wholeline.split("href=")[1].split('"')[1]
        urllist.append(url)



f=open("urllist_" + Band + ".txt", "w")
for url in urllist:
    print(url, file=f)
f.close()

