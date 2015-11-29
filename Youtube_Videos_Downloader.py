import requests
import os 
from easygui import *
import time
from random import randint
from bs4 import BeautifulSoup


if __name__ == '__main__':
	
	song_list_position=fileopenbox(msg="Provide the Songs list File", title="Song List File", default="~/")
	output_dir=diropenbox(msg="Output Directory",title="Provide the path for Downloading",default="~/Videos")	
	uncompleted_song_list=open(output_dir+'/uncompleted.txt','a')
	songs_list=open(song_list_position,'r')
	
	songs=songs_list.readlines()
	songs_list.close()

	for song in songs:
		print '---------------------------------------------------------------'
		
		print'Sending request to youtube for '+ song
		
		response=requests.get("https://www.youtube.com/results?search_query="+song)
		soup=BeautifulSoup(response.text,'html.parser')
		soup=soup.body.find('div', attrs={'id':'results'})
		ol_tag_main=soup.find_all('ol')[1]
		div3=ol_tag_main.find_all('div')[4]
		
		title=div3.a['title']
		url="https://www.youtube.com"+div3.a['href']
		
		print 'Information is given below....'
		print 'Youtube url is : '+ url
		print 'Song title is: '+ title
		
		print "\nDownloading starts....."
		fname=output_dir+ '/' + title.split(' ')[0]
		cmd='youtube-dl -o '+ fname + ' '+url
		os.system(cmd)
		
		result=os.path.isfile(fname)

		if result==True:
			print '\nSong ' + song +" is downloaded successfully"
		else:
			print "\nSong "+ song + " is not downloaded"
			uncompleted_song_list.write(song)

		time.sleep(randint(10,20))

	uncompleted_song_list.close()