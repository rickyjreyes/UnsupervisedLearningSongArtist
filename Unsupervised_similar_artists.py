
# coding: utf-8

# In[1]:

# unsupervised machine learning by finding similar artist 
# python 3.5 using pyechonest  found at https://github.com/vrangasayee/pyechonest/tree/python3 
# data aquired from Echo Nest

# David Reinke
# Ricky Reyes
# Dimitri Dimov

# NOTE: AN ECHONEST API KEY IS NEEDED IN ORDER FOR THIS TO WORK
# ADD YOUR ECHONEST API KEY BELOW AS A STRING LIKE 'QW4RTSGFWER'
# commented stuff is debugging stuff looking at arrays
import json
from pyechonest import config
from pyechonest import song
config.ECHO_NEST_API_KEY=<ECHONEST API KEY HERE>

import csv
import math
import random
from numpy import *

from scipy import argwhere
from matplotlib.pyplot import *

# Read the file
#cvsfile = open('msd_genre_dataset.txt', encoding="utf8")
datafile = open('songdata.txt', 'rt', encoding="utf8")
lines = csv.reader(datafile)
dataset = list(lines)
array(dataset).shape #verify it's read correctly


# In[2]:

feature = array(dataset[8])
#feature


# In[3]:

# use the whole dataset for our training set we fix this later cause title is still in there
training_set = []
test_set = []
for x in range(9, len(dataset)-1):
    training_set.append(array(dataset[x]))

    


# In[4]:

# to fix my artist/feature set, get rid of the song title 
# and any that have "none" for eature data because we want float values only
fixed_set = []
count = 0
i = -13
for row in training_set:
    r = []
    try:
        r.append(row[0])
        r.append(float(row[-13]))
        r.append(float(row[-12]))
        r.append(float(row[-11]))
        r.append(float(row[-10]))
        r.append(float(row[-9]))
        r.append(float(row[-8]))
        r.append(float(row[-7]))
        r.append(float(row[-6]))
        r.append(float(row[-5]))
        r.append(float(row[-4]))
        r.append(float(row[-3]))
        r.append(float(row[-2]))
        r.append(float(row[-1]))
        fixed_set.append(r)
    except:
        count = count +1
        #print("failed fixing a row ")
print("number of failed song-datas: " + str(count))
        


# In[7]:

fixed_set = array(fixed_set)
#fixed_set.shape


# In[8]:

# so now I have a fixed_set for the artist and features
# [0'%artist_name', 1'acousticness', 2'danceability', 3'duration',
#       4'energy', 5'instrumentalness', 6'key', 7'liveness', 8'loudness', 9'mode',
#       10'speechiness', 11'tempo', 12'time_signature', 13'valence']


# In[9]:

# here is where we choose what features to train our model with
# feature_list = [4, 8] = energy , loudness 

feature_list = [4, 8]
#X is featureset, Y are the labels needed for similar artist output
def Buildfset(my_features, data_set):
    f_set = []
    for s in data_set:
        row = []
        for f in my_features:
            row.append(float(s[f]))
            #row.append(math.pow(float(s[f]), 3))
        f_set.append(row)
    return array(f_set)


# In[10]:

#Buildfset will extract the wanted features in its own 2D array

feature_set = Buildfset(feature_list, fixed_set)   
#feature_set


# In[11]:

# this is where I am training my model 
# the number of clusters is the number of clusters it will try to make
# max_iter is another parameter that may need tweaking, default=300
# there are other parameters we can tweak i think
# NOTE : THIS CAN TAKE A MINUTE OR TWO DEPENDING ON HOW LARGE YOUR DATASET IS

from sklearn import cluster, datasets

k_means = cluster.KMeans(n_clusters = 100, max_iter = 300)
k_means.fit(feature_set)

# i am thinking if we cube the feature_set data it might work better? .. didnt help
# the model is always predicting the same group.. could have sworn it didnt always do this


# In[12]:

# training using k-means will make an array called k_means.labels_  
# this array assigns a cluster number to every row of song features in the feature_set
# this is looking at the first 100

#print(k_means.labels_[::100])


# In[13]:

# this is looking at the cluster n and putting the artists in that cluster in 
# the test50 array 
# note that in the fixed_set[i][0] is the artist name for that song
def getCluster(n):
    test50 = []
    for i in range(len(fixed_set)):
        if k_means.labels_[i] == n:
            test50.append(fixed_set[i][0])
    return array(test50)


# In[14]:

# looking at the artist cluster 55 set(...) will get rid of any dupes
test = getCluster(55)
len(set(test))


# In[15]:

# gets echo nest features for that artist which our model is trained to 
# feature_list is the list of feature indices

def getArtists(a):
    artist_features =[]
    dict = song.search(artist=a, results=1, buckets=['audio_summary']) #, rank_type='familiarity' )
    for d in dict:
        artist_features.append(d.artist_name) 
        artist_features.append(float(d.audio_summary['acousticness']))
        artist_features.append(float(d.audio_summary['danceability']))
        artist_features.append(float(d.audio_summary['duration']))
        artist_features.append(float(d.audio_summary['energy']))
        artist_features.append(float(d.audio_summary['instrumentalness']))
        artist_features.append(float(d.audio_summary['key']))
        artist_features.append(float(d.audio_summary['liveness']))
        artist_features.append(float(d.audio_summary['loudness']))
        artist_features.append(float(d.audio_summary['mode']))
        artist_features.append(float(d.audio_summary['speechiness']))
        artist_features.append(float(d.audio_summary['tempo']))
        artist_features.append(float(d.audio_summary['time_signature']))
        artist_features.append(float(d.audio_summary['valence']))
    #return artist_features
    predictions = getPredictions(artist_features)
    return predictions
        


# In[16]:

def getPredictions(asong):
    X = []
    for f in feature_list:
        X.append(asong[f])
    cNum = k_means.predict(X)
    print(cNum)
    simart = getCluster(cNum)
    from collections import Counter
    simart = [item for items, c in Counter(simart).most_common() for item in [items] * c]
    result = []
    count = 0
    saved = ''
    for a in simart:
        if a != saved and count < 5:
            result.append(a)
            saved = a
            count = count +1
    return result
    


# In[17]:

# here is the GUI after every function is loaded in the kernel
#   

from tkinter import *
master = Tk()
master.wm_title("Music Mob")

label1 = Label(master, width=20, bg="light grey", fg="blue", font= ("times new roman", 12))
label1["text"] = "Who is Your Favorite Artist?:"
label1.pack(side="left", anchor="n", fill="x")

# Entry field and Button is Controller
textbox = Entry(master, width=30, bd=2, bg="white", fg="black")
textbox.pack(side="left", anchor="ne", fill="x" , expand=True)

def callback():
    txt = textbox.get()
    lbox.delete(0, END)
    results = getArtists(txt)
    lbox.insert(1, "SIMILAR ARTISTS")
    lbox.insert(3, "~~~~~~~~~~~~")
    lbox.insert(5, results[0])
    lbox.insert(7, results[1])
    lbox.insert(9, results[2])
    lbox.insert(11, results[3])
    lbox.insert(13, results[4])
    #lbox.insert(1, set(results))   # get the results array and insert 
       
b = Button(master, text="SEARCH", command=callback)
b.pack()

# Listbox is the View
lbox = Listbox(master)
lbox.pack(side="bottom", before=label1, anchor="sw", fill="both", expand=True)
master.geometry('460x300')       
mainloop()


# In[ ]:



