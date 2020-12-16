#our goal would to 
#Define an input stream for the link
#get the name of the series
#make a directory with the name of the series with season
#make sure you get all the links sequentially
#inform of the file being downloaded
#present a status bar
#Put the complete message 
#and end the program with a completion message 

#{
#MUST CREATE A LOG FILE TO KNOW THE FILES THAT MAINTAINS ALL THE DOWNLOADED FILE...
#DOING SO I CAN KNOW WHICH FILES MUST BE DOWNLOADED AND WHICH MUST BE SKIPPED......
#}

import requests_html as req
from bs4 import BeautifulSoup
import requests
import os

print('This is an anime downloader. It downloads all the episodes in the season into')
print('a directory...You are suppossed to provide the link from 4anime.to as mentioned earlier')
url = input("\nPlease provide the link: ")

#html_txt = requests.get(url)
#soup = BeautifulSoup(html_txt,'lxml')
while True:
    html_txt = requests.get(url).text   #get the website and assign it to html
    soup = BeautifulSoup(html_txt, 'lxml')        #parse it using beautiful soup
    if len(soup) != 2:
        break

title = soup.find('a',id='titleleft').text
confirm = input(f"\nDo you want to download {title}(y/n)??? ")
if confirm != 'y' and confirm != 'Y':
    print('\nAborting the Mission Boss!!!')
    exit()

path = '/mnt/d/Anime/'+title
log = path+'/log.txt'
try:
    os.makedirs(path)
    with open(log,"w"):
        print("\nDirectory and Log file is created")
except OSError as error:
    print("\nDirectory and Log file exists already")

anime_links=[]

episodes = soup.find('ul',class_ = 'episodes range active')
epi = episodes.findAll('li')

for episode in epi:
    anime_links.append(episode.a['href'])
#print(anime_links)
with open(log,"r") as f:
    data=f.read().replace('\n',' ')
    #print(data)
for i in range(len(anime_links)):
    episode_no=anime_links[i].split('/')[-2].split('-')[-1]
    if episode_no in data: 
        print(f"\nEpisode-{episode_no} of {title} already downloaded...skipping to the next one")
        continue
    while True:
        down_html = requests.get(anime_links[i]).text   #get the website and assign it to html
        down_soup = BeautifulSoup(down_html, 'lxml')        #parse it using beautiful soup
        if len(down_soup) != 2:
            break
    #print(down_soup)
    dl = down_soup.find('div',class_='mirror-footer cl')
    dl1 = dl.find('script')
    lnk = str(dl1)
    beginning = lnk.find('https')
    ending = lnk.find("mp4")
    down_link = lnk[beginning:ending] + "mp4"
    #print(down_link)
    aname = down_link.split('/')[-1]
    down_path = path+'/'+aname
    print(f"\nDownloading {aname}...")


    session = req.HTMLSession()
    r = session.get(down_link)

#with open('anime_download.mp4', 'wb') as f:
    with open(down_path, 'wb') as f:
        f.write(r.content)
        with open(log,'a') as lg:
            lg.write(f"{episode_no}\n")
        print(f"Downloaded Episode{episode_no} of {title}!!!")

print("\nYour download has been completed...go grab some popcorn now ;)")
