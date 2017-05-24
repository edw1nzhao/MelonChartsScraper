from bs4 import BeautifulSoup as bs
import requests

top100 = []
loadedList = []
youtubeUrl = 'https://www.youtube.com'
melonUrl = youtubeUrl + '/watch?v=vcXQb3SdpVs&list=PLBSvleni5is2u66UMpc7nLOK6hh7w5OrQ&index=1'
fileName = 'downloadedSongs.txt'

######################################################
######################################################

def loadList():
    try:
        with open(fileName, 'r') as f:
            loadedList = [line[:-1] for line in f]

            print('There were previously: ' + str(len(loadedList)) \
                + ' songs saved.')
    except Exception as error:
        print('There was no previous file saved.')

def writeList():
    with open(fileName, 'w+') as f:
        for x in top100:
            f.write(x)
            f.write('\n')
        for x in loadedList:
            f.write(x)
            f.write('\n')

def updateList():
    loadList()
    for i in top100[:]:
        if i[:18] in loadedList:
            top100.remove(i)
    num = len(top100)
    print('There are ' + str(num) + ' new songs.')
    writeList()

def getTop100():
    r = requests.get(melonUrl)
    page = r.text
    soup = bs(page,'html.parser')
    res = soup.find_all('a', {'class':'playlist-video'})

    count = 0
    for x in res:
        link = x.get('href')
        if '/watch' in link and count != 0 and count != 101:
            top100.append(link)
        count += 1

######################################################
######################################################

getTop100()
updateList()