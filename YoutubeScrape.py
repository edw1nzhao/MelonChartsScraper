from bs4 import BeautifulSoup as bs
from twilio.rest import Client
import requests

authCode = '01892c169626b397acca0b7f1d68dbc3'
accSID = 'AC9f95cae35e07f7b38ea9069c6f74c39a'
newList = []
loadedList = []
youtubeUrl = 'https://www.youtube.com'
melonUrl = youtubeUrl + '/watch?v=vcXQb3SdpVs&list=PLBSvleni5is2u66UMpc7nLOK6hh7w5OrQ&index=1'
fileName = 'downloadedSongs.txt'

######################################################
######################################################

def loadTwilio():
    global client
    client = Client(accSID, authCode)

def loadList():
    global loadedList
    try:
        with open(fileName, 'r') as f:
            loadedList = [line[:-1] for line in f]
            print('There were previously: ' + str(len(loadedList)) \
                + ' songs saved.')
    except Exception as error:
        print('There was no previous file saved.')

def sendText(num):
    global client
    if num is not 0:
        client.messages.create(to="+8613162355703",
                               from_="+8613162355703",
                               body="There were " + str(num) + " new songs.")

def writeList():
    global newList

    with open(fileName, 'a') as f:
        for x in newList:
            f.write(x)
            f.write('\n')

def updateList():
    global loadedList
    global newList

    loadList()

    num = len(newList)
    sendText(num)
    writeList()

def getNewList():
    r = requests.get(melonUrl)
    page = r.text
    soup = bs(page,'html.parser')
    res = soup.find_all('a', {'class':'playlist-video'})

    count = 0
    for x in res:
        link = x.get('href')
        if '/watch' in link and count != 0 and count != 101:
            newList.append(link)
        count += 1

######################################################
######################################################

loadTwilio()
getNewList()
updateList()
