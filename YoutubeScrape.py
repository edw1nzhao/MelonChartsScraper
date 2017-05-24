from bs4 import BeautifulSoup as bs
import requests

top100 = []
melonUrl = 'https://www.youtube.com/watch?v=vcXQb3SdpVs&list=PLBSvleni5is2u66UMpc7nLOK6hh7w5OrQ&index=1'


def getTop100():
    r = requests.get(melonUrl)
    page = r.text
    soup = bs(page,'html.parser')
    res = soup.find_all('a', {'class':'playlist-video'})

    count = 0
    for x in res:
        link = x.get("href")
        if "/watch" in link and count != 0 and count != 101:
            top100.append(link)
        count += 1