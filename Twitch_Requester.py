
'''
=================================================
This is a test application joining learning python
as well as my love of the twitch platform

The api requires authentication login via twitch.
-------------------------------------------------
If no app id, throws 404 error on calling url request.
--------------------------------------------------

Plans for this application include:
- Reqesting specific top channels of a game type
- Returning the m3u8 playlist data
- Loading up the m3u8 steam and playing it.
'''

import requests
import json


def request_From_Twitch(lastApiCall_time, clientID):

  limit = 10
  
  request_URL = "https://api.twitch.tv/kraken/games/top?limit={}&client_id={}".format(limit, clientID )
  print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json()
  
  for x in range(len(jsonData['top'])):
    number = x+1
    game_Name = jsonData['top'][x]['game']['name']
    print('%s is number: %d in the list' % (game_Name,number))

def request_TopChannels_ByGame(gameName,lastApiCall_time, clientID):
  '''
  Returned json structure:
  -Streams [0 - limit]
   -[0]
    -channel
     -name
  '''
  limit = 10
  request_URL = "https://api.twitch.tv/kraken/streams/?game={}&limit={}&client_id={}".format(gameName,limit, clientID )
  print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json()
  
  for x in range(len(jsonData['streams'])):
    number = x+1
    channel = jsonData['streams'][x]['channel']['name']
    print('%s is number: %d in the list' % (channel,number)) 

def request_Channel(channelName,lastApiCall_time, clientID):
  '''
  Example response:
  -Token
   {}
  -Sid
  -Mobile restricted
  '''
  #Example url: http://api.twitch.tv/api/channels/{channel}/access_token
  request_URL = "http://api.twitch.tv/api/channels/{}/access_token?client_id={}".format(channelName,clientID)
  print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json() 
  token = jsonData['token']
  sig = jsonData['sig']
  print(jsonData)
  print('token is: %s' % token)
  print('sig is: %s' % sig)
  
  request_m3u8_Playlist(channelName,token,sig,clientID)

def request_m3u8_Playlist(channelName,token,sig,clientID):
  request_URL = 'http://usher.twitch.tv/api/channel/hls/{}.m3u8?player=twitchweb&token={}&sig={}&allow_audio_only=true&allow_source=true&type=any&p=9333029'.format(channelName,token,sig)
  print(request_URL)
  response = requests.get(request_URL)
  print(response.text)
  '''This request returns a m3u8 playlist file with stream link and res info data'''
  #jsonData = response.json()   

#Below are the calls to the config file with the app id.
lastApiCall_time = 0
file = open('config.txt')

id = file.readline().split(':')[1]
request_From_Twitch(lastApiCall_time,id)

#Example game to grab streams from: Overwatch & channel example: esl_overwatch
request_TopChannels_ByGame('Overwatch',lastApiCall_time,id)
request_Channel('esl_overwatch',lastApiCall_time,id)