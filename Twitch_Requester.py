
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
    
    '''
    
    Format:
    - #EXTM3U
    - #EXT-X-TWITCH-INFO:NODE [1]
    - #EXT-X-MEDIA:TYPE=VIDEO [1]
    - #EXT-X-STREAM-INF:PROGRAM-ID=1 [1]
    - URL data [1]
    - #EXT-X-TWITCH-INFO:NODE [2]
    - #EXT-X-MEDIA:TYPE=VIDEO [2]
    - #EXT-X-STREAM-INF:PROGRAM-ID=1 [2]
    - URL data [2]
    - ...
    
    
    
    -> check for front of string line:
    #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="medium",NAME="Medium",AUTOSELECT=YES,DEFAULT=YES
    --> check #EXT-X-MEDIA:TYPE=VIDEO part
    
    -> Then grab next line with data
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=992000,RESOLUTION=852x480,CODECS="avc1.77.30,mp4a.40.2",VIDEO="medium"
    --> Craete object with data
    
    -> Then Grab next line as url link
    '''
    
    
  def parse_Playlist(self):
    #do things
    print('starting playlist extraction!')
    #Grab all lines and hold in a list
    splitData = self.baseData.split('\n')
    '''
    Go through and scan each line for data
    '''
    startIndex = 1
    z = 0
    for x in range(len(splitData)):
      print('%d index = \n %s' % (x , splitData[x]))
      tempValue = splitData[x].split(',')
      print(tempValue)
      #The lines are now split
      if('#EXT-X-TWITCH-INFO:NODE=' in str(splitData[x].split(','))):
        #ignore first line
        #print(splitData[x])
        print('#EXT-X-TWITCH-INFO:')
      #for z in range(len(self.videoNames)):
        
      if ('#EXT-X-MEDIA:TYPE=VIDEO' in str(splitData[x])):
        #ignore first linesplitData[x]):
        #Grab the next 3 lines as one.
        dataPart = splitData[x].split(',')[1]
        value = dataPart.find('"',0)
        nameString = dataPart[dataPart.find('"')+1:len(dataPart)-1]
        print('%s -----------> %s' % (dataPart, nameString) )
        if(self.videoNames[z] in str(splitData[x])):
          
          print('%s is in this line %s' % (self.videoNames[z], splitData[x]))
          if('#EXT-X-STREAM-INF:PROGRAM-ID=1' in str(splitData[z])):
            resData = splitData[z].split(',')
            for y in range(len(resData)):
              if('BANDWIDTH' in str(resData[y])):
                tempSplit = resData[y].split(':')
                print('tempSplit %s' % tempSplit)
                self.streams[z]['bandwidth'] = (tempSplit[0].split('=')[1])
              if('RESOLUTION' in str(resData[y])):                
                tempSplit = resData[y].split(':')
                print('tempSplit %s' % tempSplit)              
                self.streams[z]['resolution'] = (tempSplit[0].split('=')[1])
              if('CODECS' in str(resData[y])):            
                tempSplit = resData[y].split(':')
                print('tempSplit %s' % tempSplit)                
                self.streams[z]['codecs'] = (tempSplit[0].split('=')[1])
              if('VIDEO' in str(resData[y])):
                tempSplit = resData[y].split(':')
                print('tempSplit %s' % tempSplit)                
                self.streams[z]['video'] = (tempSplit[0].split('=')[1])
            
          '''else:
            print("Error: Not expected m3u8 line! \n"+splitData[x+self.resOffset])'''
        if z < len(self.videoNames)-1:
          z = z+1
        print('Z index is now %d' % z)
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
    print(self.streams[0]['video'])
    print(self.streams[0]['resolution'])
    
    print(self.streams[2]['video'])
    print(self.streams[2]['resolution'])    

class m3u8_Parser():
  '''
  This class handles the extraction of data from lines
  of the m3u8 file.
  '''
  
  def media_Extractor(lines, index, names):
    if ('#EXT-X-MEDIA:TYPE=VIDEO' in str(lines[index])):
      returnedValue = lines[index].split(',')[0].split(':')
    return returnedValue.preppend('The resolution is: ')


def m3u8_parser_Media_Ext(lines, index):
  
  if ('#EXT-X-MEDIA:TYPE=VIDEO' in str(lines[index])):
    #ignore first linesplitData[x]):
    #Grab the next 3 lines as one.
    print('-----------> %s' % self.videoNames[z])
    print('Checking %s is in this line %s' % (self.videoNames[z], splitData[x]))
    if(self.videoNames[z] in str(splitData[x])):
      print('%s is in this line %s' % (self.videoNames[z], splitData[x]))
      if('#EXT-X-STREAM-INF:PROGRAM-ID=1' in str(splitData[x])):
        resData = splitData[z].split(',')
        for y in range(len(resData)):
          if('BANDWIDTH' in str(resData[y])):
            tempSplit = resData[y].split(':')
            print('tempSplit %s' % tempSplit)
            self.streams[z]['bandwidth'] = (tempSplit[0].split('=')[1])
          if('RESOLUTION' in str(resData[y])):                
            tempSplit = resData[y].split(':')
            print('tempSplit %s' % tempSplit)              
            self.streams[z]['resolution'] = (tempSplit[0].split('=')[1])
          if('CODECS' in str(resData[y])):            
            tempSplit = resData[y].split(':')
            print('tempSplit %s' % tempSplit)                
            self.streams[z]['codecs'] = (tempSplit[0].split('=')[1])
          if('VIDEO' in str(resData[y])):
            tempSplit = resData[y].split(':')
            print('tempSplit %s' % tempSplit)                
            self.streams[z]['video'] = (tempSplit[0].split('=')[1])
        
      else:
        print("Error: Not expected m3u8 line! \n"+splitData[x+self.resOffset])
    if z < len(self.videoNames)-1:
      z = z+1
    print('Z index is now %d' % z)
    #print(splitData[x])
    
    #x+=3
    
  return nextMediaObject

def request_From_Twitch(lastApiCall_time, clientID, gameList, debug):
  
  request_URL = "https://api.twitch.tv/kraken/games/top?limit={}&client_id={}".format(resultsLimit, clientID )
  if debug:
    print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json()
  
  for x in range(len(jsonData['top'])):
    number = (x+1)
    game_Name = jsonData['top'][x]['game']['name']
    gameList.insert(x,game_Name)
    if debug:
      print('%s is number: %d in the list' % (gameList[x],number))
  if debug:
    print('The gamesList holds %d game names' % (len(gameList)))

def request_TopChannels_ByGame(gameName,lastApiCall_time, clientID, debug):
  '''
  Returned json structure:
  -Streams [0 - limit]
   -[0]
    -channel
     -name
  '''
  request_URL = "https://api.twitch.tv/kraken/streams/?game={}&limit={}&client_id={}".format(gameName,resultsLimit, clientID )
  if debug:
    print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json()
  
  for x in range(len(jsonData['streams'])):
    number = x+1
    channel = jsonData['streams'][x]['channel']['name']
    streamList.insert(x,channel)
    if debug:
      print('%s is number: %d in the list' % (streamList[x],number)) 

def request_Channel(channelName,lastApiCall_time, clientID, debug):
  '''
  Example response:
  -Token
   {}
  -Sid
  -Mobile restricted
  '''
  #Example url: http://api.twitch.tv/api/channels/{channel}/access_token
  request_URL = "http://api.twitch.tv/api/channels/{}/access_token?client_id={}".format(channelName,clientID)
  if debug:
    print(request_URL)
  response = requests.get(request_URL)
  jsonData = response.json() 
  token = jsonData['token']
  sig = jsonData['sig']
  if debug:  
    print(jsonData)
    print('token is: %s' % token)
    print('sig is: %s' % sig)
  
  request_m3u8_Playlist(channelName,token,sig,clientID, debug)

def request_m3u8_Playlist(channelName,token,sig,clientID, debug):
  request_URL = 'http://usher.twitch.tv/api/channel/hls/{}.m3u8?player=twitchweb&token={}&sig={}&allow_audio_only=true&allow_source=true&type=any&p=9333029'.format(channelName,token,sig)
  response = requests.get(request_URL)
  if debug:  
    print(request_URL)
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

#Setting the constants and lists

resultsLimit = 10

gameList = [None] * resultsLimit
streamList = [None] * resultsLimit

lastApiCall_time = 0

#Below are the calls to the config file with the app id.

file = open('config.txt')

id = file.readline().split(':')[1]
request_From_Twitch(lastApiCall_time,id, gameList, True)

#Example game to grab streams from: top-most game & top-most channel : index[0]
request_TopChannels_ByGame(gameList[0],lastApiCall_time,id, True)
request_Channel(streamList[0],lastApiCall_time,id,True)

'''TODO:
- Might need to remove call to m3u8 function from within request_Channel function.
- Will need to remove / change testing of fucntions with hardcoded game name and channel.
- Add support for parsing the m3u8 file, and extracting usefull data. (stream links & resolutions etc)
- Will have to look into how to play streams.
- Not sure how to show all of this visually / gui development.


* Need to sort out how m3u8 playlist Object will be built and Accessed.

- Possibly created first as empty object, then access and pass in m3u8 file
- Other accessor methods / functions will return required data / values if 
object has been populated with the file data.

* Not sure if there should be a seperate object holding the stream data
'''