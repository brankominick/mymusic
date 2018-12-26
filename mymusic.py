#analyse the music in a collaborative playlist
from __future__             import print_function
import os
import sys
import json
import pandas               as pd
import spotipy
import spotipy.util         as util
from spotipy.oauth2         import SpotifyClientCredentials
from myconfig               import *

#Make json readable
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))

#########FUNCTION DEFINITIONS###############

#{track_name, artist, date_added, duration_ms, popularity, track_id}
def GetTracks(tracks, trackList):
    for count, item in enumerate(tracks['items']):
        #print(json.dumps(item, sort_keys=True, indent=4))
        track_name = item['track']['name']
        artist = item['track']['artists'][0]['name']
        date = item['added_at'].split('-')
        date_added = date[0] + '-' + date[1] #year and month
        duration_ms = item['track']['duration_ms']
        popularity = item['track']['popularity']
        track_id = item['track']['id']

        result = {'track_name':track_name, 'artist':artist, 'date_added':date_added,
        'duration_ms':duration_ms, 'popularity':popularity, 'track_id':track_id}

        #print result
        trackList.append(result)

#returns list of dicts from GetTracks
def GetPlaylist(username, playlist_id):
    playlist = sp.user_playlist(username,playlist_id)
    tracks = playlist['tracks']#['items']
    trackList = []
    GetTracks(tracks, trackList)
    while tracks['next']:
        tracks = sp.next(tracks)
        GetTracks(tracks, trackList)
    return trackList

#returns list of dicts with features and track ids
def GetFeatures(track_ids):
    features = []
    drop = ('analysis_url', 'track_href', 'type', 'uri')
    while len(track_ids) > 0:
        total = len(track_ids)
        if (total >= 50):
            f = sp.audio_features(track_ids[0:50])
            for item in f:
                for thing in drop:
                    item.pop(thing,None)
                features.append(item)
            del track_ids[0:50]
        else:
            f = sp.audio_features(track_ids[:total])
            for item in f:
                for thing in drop:
                    item.pop(thing,None)
                features.append(item)
            del track_ids[:total]
    return features


##########END DEFINITIOINS########################

ccm = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=ccm)
sp.trace=False

#Let's grab the playlist and all the songs
archived_tracks = GetPlaylist(ARCHIVE_OWNER,ARCHIVES_ID)

archived_tracks = pd.DataFrame(archived_tracks).sort_values('date_added',ascending=True)
archived_tracks = archived_tracks[['track_name', 'artist', 'date_added', 'duration_ms', 'popularity', 'track_id']]


tids = list(archived_tracks['track_id'])
features = GetFeatures(tids)
features = pd.DataFrame(features)
features = features.rename(columns={'id':'track_id'})
archived_tracks = pd.merge(archived_tracks,features, on='track_id')

print(archived_tracks.head(5))

#dataframe now contains songs with identifiers and features
#print(archived_tracks.describe())
#print(archived_tracks['date_added'])

spring_months = ['2018-03','2018-04','2018-05','2018-06']
summer_months = ['2018-06','2018-07','2018-08','2018-09']
fall_months = ['2018-09','2018-10','2018-11','2018-12']

spring = archived_tracks.loc[archived_tracks['date_added'].isin(spring_months)]
summer = archived_tracks.loc[archived_tracks['date_added'].isin(summer_months)]
fall = archived_tracks.loc[archived_tracks['date_added'].isin(fall_months)]

print("spring:\n",spring.describe())
print('summer\n',summer.describe())
print('fall\n',fall.describe())

March = spring.loc[spring['date_added'] == '2018-03']
April = spring.loc[spring['date_added'] == '2018-04']
May = spring.loc[spring['date_added'] == '2018-05']
June = spring.loc[spring['date_added'] == '2018-06']
July = summer.loc[summer['date_added'] == '2018-07']
August = summer.loc[summer['date_added'] == '2018-08']
September = summer.loc[summer['date_added'] == '2018-09']
October = fall.loc[fall['date_added'] == '2018-10']
November = fall.loc[fall['date_added'] == '2018-11']
December = fall.loc[fall['date_added'] == '2018-12']

mths = ['March','April','May','June','July','August','September','October','November','December']
mus = [March,April,May,June,July,August,September,October,November,December]

for i in range(len(mths)):
    print("{} stats: \n{}".format(mths[i],mus[i].describe()))
