
# coding: utf-8

# In[20]:

# EchoNest song data scraper  
# python 3.5 using pyechonest  found at https://github.com/vrangasayee/pyechonest/tree/python3 

# David Reinke
# Ricky Reyes
# Dimitri Dimov

# ENTER YOUR ECHONEST API KEY BELOW FOR THIS TO WORK! IN QUOTES LIKE 'Q35ASDFGVWE56'
from pyechonest import config
config.ECHO_NEST_API_KEY=<YOUR ECHO NEST API KEY HERE>

import json
from pyechonest import track
from pyechonest import song


# In[21]:

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


# In[22]:

# writes the song results data into a file in the format:
# artist_name, title, acousticness, danceability, duration, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence
def writeData(data):
    fo = open('songdata.txt', 'a', encoding="utf8")
    for d in data:
        fo.write(d.artist_name + ',' + 
                 d.title +','+        # TITLE GAVE US PROBLEMS LATER BECAUSE OF THE ','s CAN COMMENT BUT GETS FIXED LATER
                 str(d.audio_summary['acousticness'])+','+
                 str(d.audio_summary['danceability'])+','+
                 str(d.audio_summary['duration'])+','+
                 str(d.audio_summary['energy'])+','+
                 str(d.audio_summary['instrumentalness'])+','+ 
                 str(d.audio_summary['key'])+','+
                 str(d.audio_summary['liveness'])+','+
                 str(d.audio_summary['loudness'])+','+
                 str(d.audio_summary['mode'])+','+
                 str(d.audio_summary['speechiness'])+','+
                 str(d.audio_summary['tempo'])+','+
                 str(d.audio_summary['time_signature'])+','+ 
                 str(d.audio_summary['valence']) + '\n')
    fo.close()


# In[23]:

# reads from a list of artists in a text file and scrapes the artist data
# then writes (appends) the scraped artist song data into a file
# there is a query limit for free developer api key so added a delay in order to not get cut off! 
# NOTE : THIS TAKES A REALLY LONG TIME! depends on how big of an artist list in artist file
import time
def buildDataSet(artistList):
    for art in artistList:
        try:
            results = song.search(artist=art, results=40, buckets=['audio_summary'])
            writeData(results)
        except:
             print('error on: ' + art)
        time.sleep(20) # delays for 20 seconds due to the Eco Nest query limitation


# In[24]:

# Read the artist file
#artistfile = open('myartists.txt', 'rt')
artists = []
with open('myartists.txt') as f:
    artists = [x.strip('\n') for x in f.readlines()]


# In[25]:

buildDataSet(artists)


# In[265]:

# can manually get a single artist here 
# a = "Michael Jackson'
# results = song.search(artist=a, results=50, buckets=['audio_summary'], rank_type='familiarity' )
# writeData(results)


# In[247]:




# In[ ]:



