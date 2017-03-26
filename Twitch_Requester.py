
'''This currently does not work!
The api requires authentication login via twitch.
-------------------------------------------------
As a result, throws 404 error on calling url request.
- Can either try a different http library
- Or use authentication login. :(
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
  ##print(jsonData['top'][1]['game']['name'])

lastApiCall_time = 0
file = open('config.txt')


id = file.readline().split(':')[1]
request_From_Twitch(lastApiCall_time,id)