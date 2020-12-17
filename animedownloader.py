'''
The anime downloader downloads anime from 4anime.to....it creates a directory in the local disk c and makes
a log file and stores all the downloaded files in it. All that has to be done is provide the link for the
anime from 4anime.to and you are not just good to go but GREAT to go
Hope this automation makes your life a lot easier
'''

import sys
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import os

print('This is an anime downloader. It downloads all the episodes in the season into')
print('a directory...You are suppossed to provide the link from 4anime.to as mentioned earlier')
url = input("\nPlease provide the link: ")       #Provide the link here

while True:                                      #The loop is made to have no loading problem
    html_txt = requests.get(url).text            #get the website and assign it to html
    soup = BeautifulSoup(html_txt, 'lxml')       #parse it using beautiful soup
    if len(soup) != 2:
        break

title = soup.find('a',id='titleleft').text      #finding the title of the anime
confirm = input(f"\nDo you want to download {title}(y/n)??? ") #confirming if you want to download the anime
if confirm != 'y' and confirm != 'Y':
    print('\nAborting the Mission Boss!!!')
    exit()

filepath = '/mnt/d/Anime/'              #change the path to your choice

path = filepath+title                  #path for the file 
log = path+'/log.txt'                           #path for the log file

try:                                            #to avoid the directory already exists error
    os.makedirs(path)
    with open(log,"w"):
        print("\nDirectory and Log file is created")
except OSError as error:                        #if directory already exits
    print("\nDirectory and Log file exists already")

anime_links=[]                                  #to store all the links to the pages 

episodes = soup.find('ul',class_ = 'episodes range active')     #finding all episode unordered list in the website
epi = episodes.findAll('li')                    #finding all the list elements 

for episode in epi:
    anime_links.append(episode.a['href'])       #extracting all the links to each page

with open(log,"r") as f:
    data=f.read().replace('\n',' ')             #opening the log file and collecting its data

for i in range(len(anime_links)):               #going through each link in anime_links 
    episode_no=anime_links[i].split('/')[-2].split('-')[-1]     #collecting the episode number

    if episode_no in data:                      #if the episode number exists in log file it skips its download
        print(f"\nEpisode-{episode_no} of {title} already downloaded...skipping to the next one")
        continue

    while True:
        down_html = requests.get(anime_links[i]).text   #else goes to the website 
        down_soup = BeautifulSoup(down_html, 'lxml')
        if len(down_soup) != 2:
            break

    dl = down_soup.find('div',class_='mirror-footer cl') #to get the link from a script tag
    dl1 = dl.find('script')                             #I was feeling lazy so I used this scheme to get the link
    lnk = str(dl1)                                      #rather than going for a selenium :)
    beginning = lnk.find('https')
    ending = lnk.find("mp4")
    down_link = lnk[beginning:ending] + "mp4"       #the download link 
    aname = down_link.split('/')[-1]
    down_path = path+'/'+aname                          #getting the name of the episode and updating the path
    print(f"\nDownloading {aname}...")

    filesize = int(requests.head(down_link).headers["Content-Length"])
    chunk_size = 1024

    with requests.get(down_link, stream=True) as r, open(down_path,'wb') as f, tqdm( unit='B', unit_scale=True, unit_divisor=1024, total=filesize, file=sys.stdout ) as progress:
        for chunk in r.iter_content(chunk_size= chunk_size):
            datasize =f.write(chunk)
            progress.update(datasize)
        with open(log,'a') as lg:
            lg.write(f"{episode_no}\n")             #updating the log file 
        print(f"Downloaded Episode{episode_no} of {title}!!!")

print("\nYour download has been completed...go grab some popcorn now ;)")
