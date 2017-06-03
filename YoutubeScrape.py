from bs4 import BeautifulSoup as bs
from twilio.rest import Client

import os
import shutil
import requests
import youtube_dl


######################################################
######################################################

noFile = True
authCode = '01892c169626b397acca0b7f1d68dbc3'
accSID = 'AC9f95cae35e07f7b38ea9069c6f74c39a'
tempSongs = []
newSongs = []
loadedSongs = []

youtubeUrl = 'https://www.youtube.com'
melonUrl = youtubeUrl + '/watch?v=vcXQb3SdpVs&list=PLBSvleni5is2u66UMpc7nLOK6hh7w5OrQ&index=1'
fileName = 'downloadedSongs.txt'

sourcePath = '/Users/voltageShift/repository/MelonChartsScraper/'
source = os.listdir(sourcePath)
destPath = '/Users/voltageShift/repository/MelonChartsScraper/Downloaded'

ydl_opts = {
    'format': 'bestaudio/best',
    'verbose': True,
    'noplaylist':True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
######################################################
######################################################

def loadTwilio():
    global client
    client = Client(accSID, authCode)

def loadList():
    global loadedSongs
    global noFile

    try:
        with open(fileName, 'r') as f:
            loadedSongs = [line[:-1].strip() for line in f]
            if len(loadedSongs) is not 0:
                noFile = False
            print('There were previously: ' + str(len(loadedSongs)) \
                + ' songs saved.')
    except Exception as error:
        print('There was no previous file saved.')

def getnewSongs():
    global newSongs

    r = requests.get(melonUrl)
    page = r.text
    soup = bs(page,'html.parser')
    res = soup.find_all('a', {'class':'playlist-video'})

    count = 0
    for x in res:
        link = x.get('href')
        if '/watch' in link and count != 0 and count != 101:
            newSongs.append(link.strip())
        count += 1

def updateList():
    global loadedSongs
    global newSongs
    global tempSongs
    global noFile
    # print("prev load" + str(len(loadedSongs)))
    # print("prev news" + str(len(newSongs)))
    # print("prev temp" + str(len(tempSongs)))

    for i in newSongs:
        # print(i in loadedSongs);
        if i not in loadedSongs:
            tempSongs.append(i)

    # print("post load" + str(len(loadedSongs)))
    # print("post news" + str(len(newSongs)))
    # print("post temp" + str(len(tempSongs)))

    writeList()

def writeList():
    global tempSongs
    global noFile
    # print(str(len(tempSongs)) + "hi")
    with open(fileName, 'a') as f:
        for x in tempSongs:
            f.write(x)
            f.write('\n')

def downloadSongs():
    global newSongs
    global source

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with ydl:
        for x in newSongs:
            ydl.download([youtubeUrl + x])

    for files in source:
        if files.endswith('.mp3'):
            shutil.move(os.path.join(sourcePath,files), os.path.join(destPath,files))

def sendText(num):
    global client
    if num is not 0:
        client.messages.create(to="+13522224358",
                               from_="+8613162355703",
                               body="There are " + str(num) + " new songs added.")
######################################################
######################################################

loadTwilio()
loadList()
getnewSongs()
updateList()
#downloadSongs()