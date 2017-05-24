from bs4 import BeautifulSoup as bs
import requests

url = 'https://www.youtube.com/watch?v=vcXQb3SdpVs&list=PLBSvleni5is2u66UMpc7nLOK6hh7w5OrQ&index=1'

r = requests.get(url)
page = r.text
soup = bs(page,'html.parser')
res = soup.find_all('a', {'class':'playlist-video'})
print(res)
# for x in res:
#     print x.get("href")