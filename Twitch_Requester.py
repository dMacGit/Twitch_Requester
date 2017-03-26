
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
  
  test_Url = "https://api.twitch.tv/kraken/games/top?limit={}&client_id={}".format(limit, clientID )
  print(test_Url)
  second_test = "https://api.twitch.tv/kraken/streams?game=League%20of%20Legends"
  response = requests.get(test_Url)
  jsonData = response.json()
  
  for x in range(len(jsonData['top'])):
    number = x+1
    game_Name = jsonData['top'][x]['game']['name']
    print('%s is number: %d in the list' % (game_Name,number))

#Below are the calls to the config file with the app id.
lastApiCall_time = 0
file = open('config.txt')

id = file.readline().split(':')[1]
request_From_Twitch(lastApiCall_time,id)