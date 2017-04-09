
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

class m3u8_playlist():
  
  def __init__(self,data):
    self.resOffset = 1
    self.urlOffset = 2
    
    self.videoNames = [ 'chunked', 'high', 'medium', 'low' , 'mobile', 'audio' ]
    #init the objects
    '''
     #EXT-X-TWITCH-INFO:
    
     #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="medium",NAME="Medium",AUTOSELECT=YES,DEFAULT=YES 
     #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=992000,RESOLUTION=852x480,CODECS="avc1.77.30,mp4a.40.2",VIDEO="medium"
     url-link
     
     bandwidth, resolution, codecs, video
     
    '''
    self.baseData = data
    
    
    self.streamResObject = {'video':None,'bandwidth':None,'resolution':None, 'codecs':None, 'url':None}
    
    self.chunked = self.streamResObject
    self.high = self.streamResObject
    self.medium = self.streamResObject
    self.low = self.streamResObject
    self.mobile = self.streamResObject
    self.audio = self.streamResObject
    
    self.streams = [ self.chunked, self.high, self.medium, self.low, self.mobile, self.audio ]
    
    
  def parse_Playlist(self):
    #do things
    print('starting playlist extraction!')
    splitData = self.baseData.split('\n')
    for x in range(len(splitData)):
      print('%d index = \n %s' % (x , splitData[x]))
      if('#EXT-X-TWITCH-INFO:' in str(splitData[x].split(','))):
        #ignore first line
        #print(splitData[x])
        print('#EXT-X-TWITCH-INFO:')
      #for z in range(len(self.videoNames)):
        
        if ('#EXT-X-MEDIA:' in str(splitData[x])):
          #ignore first linesplitData[x]):
          #Grab the next 3 lines as one.
          print('-----------> %s' % self.videoNames[x])
          if(self.videoNames[x] in str(splitData[x])):
            if('#EXT-X-STREAM-INF:' in str(splitData[x+self.resOffset])):
              resData = splitData[x+self.resOffset].split(',')
              for y in range(len(resData)):
                if('BANDWIDTH' in str(resData[y])):
                  tempSplit = resData[y].split(':')
                  print('tempSplit %s' % tempSplit)
                  self.streams[x]['bandwidth'] = (tempSplit[0].split('=')[1])
                if('RESOLUTION' in str(resData[y])):                
                  tempSplit = resData[y].split(':')
                  print('tempSplit %s' % tempSplit)              
                  self.streams[x]['resolution'] = (tempSplit[0].split('=')[1])
                if('CODECS' in str(resData[y])):            
                  tempSplit = resData[y].split(':')
                  print('tempSplit %s' % tempSplit)                
                  self.streams[x]['codecs'] = (tempSplit[0].split('=')[1])
                if('VIDEO' in str(resData[y])):
                  tempSplit = resData[y].split(':')
                  print('tempSplit %s' % tempSplit)                
                  self.streams[x]['video'] = (tempSplit[0].split('=')[1])
            else:
              print("Error: Not expected m3u8 line! \n"+splitData[x+self.resOffset])
          
            
        #print(splitData[x])
        
        #x+=3
      
    
    '''print('######################')
    print(splitData[0])
    print(splitData[1])
    ##EXT-X-TWITCH-INFO:    
    
    
    chuncked['BANDWIDTH'] = 992000
    chuncked['RESOLUTION'] = '852x480'
    chuncked['CODECS'] = 'avc1.77.30,mp4a.40.2'
    chuncked['VIDEO'] = 'medium'''
    print(self.chunked['video'])
    print(self.chunked['resolution'])
    
    print(self.medium['video'])
    print(self.medium['resolution'])    

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
  print(response.text+'\n=================================')
  '''This request returns a m3u8 playlist file with stream link and res info data'''
  data = response.text
  playlist = m3u8_playlist(data)
  playlist.parse_Playlist()
  '''splitData = data.split('\n')
  print('######################')
  print(splitData[0])
  print(splitData[1])
  ##EXT-X-TWITCH-INFO:'''
  #jsonData = response.json()   

#Below are the calls to the config file with the app id.
lastApiCall_time = 0
file = open('config.txt')

id = file.readline().split(':')[1]
request_From_Twitch(lastApiCall_time,id)

#Example game to grab streams from: Overwatch & channel example: esl_overwatch
request_TopChannels_ByGame('Overwatch',lastApiCall_time,id)
request_Channel('esl_overwatch',lastApiCall_time,id)

'''TODO:
- Might need to remove call to m3u8 function from within request_Channel function.
- Will need to remove / change testing of fucntions with hardcoded game name and channel.
- Add support for parsing the m3u8 file, and extracting usefull data. (stream links & resolutions etc)
- Will have to look into how to play streams.
- Not sure how to show all of this visually / gui development.
'''