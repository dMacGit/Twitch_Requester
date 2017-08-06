
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
# Adding logging to help toggle debug info
import logging, sys


class streamObject(object):

  def __init__(self, video, bandwidth, resolution, codecs, url):
    self.video = video
    self.bandwidth = bandwidth
    self.resolution = resolution
    self.codecs = codecs
    self.url = url
    
  def __repr__(self):
    return 'streamObject( %s, %s, %s, %s, %s' % (self.video,self.bandwidth, self.resolution, self.codecs, self.url)
  
  def __str__(self):
      return 'video:%s, bandwidth:%s, resolution:%s, codecs:%s, url:%s' % (self.video,self.bandwidth, self.resolution, self.codecs, self.url)  


class m3u8_playlist(streamObject):

  def __init__(self,data):
    self.streamOffset = 1
    self.urlOffset = 1
    
    self.videoNames = [ 'chunked', 'high_720p60', 'high_720p30', 'med_480p30' , 'low_360p30', 'mob_160p30', 'audio_only' ]

    self.baseData = data
   
    self.chunked = None
    self.high_720p60 = None
    self.high_720p30 = None
    self.med_480p30 = None
    self.low_360p30 = None
    self.mob_160p30 = None
    self.audio_only = None
    
    self.streams = [ self.chunked, self.high_720p60, self.high_720p30, self.med_480p30, self.low_360p30, self.mob_160p30, self.audio_only ]
    
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
    '''
    
    
  def parse_Playlist(self, debug=False):
    #do things
    if debug:
      print('starting playlist extraction!')
    #Grab all lines and hold in a list
    lines = self.baseData.split('\n')
    '''
    Go through and scan each line for data
    '''
    videoNamesIndex = 0
    line_loop_count = 0
    for lineIndex in range(len(lines)):
      tempValue = lines[lineIndex].split(',')
      line_loop_count += 1
      #The lines are now split
        
      if ('#EXT-X-MEDIA:TYPE=VIDEO' in str(lines[lineIndex])):
        #ignore first linesplitData[lineIndex]):
        #Grab the next 3 lines as one.
        nameValue = lines[lineIndex].split(',')[1]
        nameString = nameValue[nameValue.find('"')+1:len(nameValue)-1]
        if('_' in str(self.videoNames[videoNamesIndex]) ):
          #No perfect match so split
          if( 'audio_only' in str(self.videoNames[videoNamesIndex])):
              check_string = self.videoNames[videoNamesIndex]
          else:
              check_string = self.videoNames[videoNamesIndex].split('_')[1]
        else:
          check_string = self.videoNames[videoNamesIndex]
        if( check_string in str(lines[lineIndex])):
          lineIndex = lineIndex+self.streamOffset
          if('#EXT-X-STREAM-INF:PROGRAM-ID=1' in str(lines[lineIndex])):
            #Extract the data
            dataSubstring = lines[lineIndex].split(',')
            bandwidth, resolution, codecs, video, url = '','','','',''
            for dataIndex in range(len(dataSubstring)):
              dataObject = dataSubstring[dataIndex].split(':')            
              line_loop_count += 1
              if 'BANDWIDTH' in dataSubstring[dataIndex] :
                bandwidth = dataObject[0].split('=')[1]
                if debug:
                  print('BANDWIDTH value: %s' % (dataObject[0].split('=')[1]))
              elif 'RESOLUTION' in dataSubstring[dataIndex]:                
                resolution = (dataObject[0].split('=')[1])
                if debug:
                  print('RESOLUTION value: %s' % (dataObject[0].split('=')[1]))
              elif 'CODECS' in dataSubstring[dataIndex] :            
                codecs = (dataObject[0].split('=')[1])
                if debug:
                  print('CODECS value: %s' % (dataObject[0].split('=')[1]))
              elif 'VIDEO' in dataSubstring[dataIndex]:             
                video = (dataObject[0].split('=')[1])
                if debug:
                  print('VIDEO value: %s' % (dataObject[0].split('=')[1]))
                break
             
              elif( 'http://' in str(lines[lineIndex+self.urlOffset])):
                if debug:
                  print('Grabbing url part: %s' % lines[lineIndex+self.urlOffset])
                url = lines[lineIndex+self.urlOffset]
                
            if debug:       
              print("<< Video: ",video,' Bandwidth: ',bandwidth,' Resolution: ',resolution,' Codecs: ',codecs,' Url: ',url,' >>')
            new_Stream = streamObject(video,bandwidth,resolution,codecs,url)
            self.streams[videoNamesIndex] = new_Stream
            if debug:
              print('Video stream <%s> has been grabbed!' % (self.videoNames[videoNamesIndex]))
            #video,bandwidth,resolution,codecs,url
            '''new_stream.video = video
              new_stream.bandwidth = bandwidth
              new_stream.resolution = resolution
              new_stream.codecs = codecs
              new_stream.url = url
            '''
          
          if videoNamesIndex < len(self.videoNames)-1:
            videoNamesIndex = videoNamesIndex+1
            if debug:
              print('videoNamesIndex index is now %d' % videoNamesIndex)
    if debug:    
      print(self.streams[1])

class twitch_session(object):
  
  def __init__(self, clientID, resultsLimit):
    self.last_call = ''
    self.time_limit = 60 #The min time between calls to reload list
    self.game_list = [None] * resultsLimit
    self.stream_list = [None] * resultsLimit
    self.clientID = clientID
    self.resultsLimit = resultsLimit
    self.token = None
    self.sig = None
    self.token_valid = False
    self.sig_valid = False
    self.m3u8_playlist = None

  def request_From_Twitch(self, debug=False):
    
    
    request_URL = "https://api.twitch.tv/kraken/games/top?limit={}&client_id={}".format(self.resultsLimit, self.clientID )
    if debug:
      print(request_URL)
    response = requests.get(request_URL)
    jsonData = response.json()
    
    for x in range(len(jsonData['top'])):
      number = (x+1)
      game_Name = jsonData['top'][x]['game']['name']
      self.game_list.insert(x,game_Name)
      if debug:
        print('%s is number: %d in the list' % (self.game_list[x],number))
    if debug:
      print('The gamesList holds %d game names' % (len(self.game_list)))

  def request_TopChannels_ByGame(self,gameName,debug=False):
    '''
    Returned json structure:
    -Streams [0 - limit]
     -[0]
      -channel
       -name
    '''
    request_URL = "https://api.twitch.tv/kraken/streams/?game={}&limit={}&client_id={}".format(gameName,self.resultsLimit, self.clientID )
    if debug:
      print(request_URL)
    response = requests.get(request_URL)
    jsonData = response.json()
    
    for x in range(len(jsonData['streams'])):
      number = x+1
      channel = jsonData['streams'][x]['channel']['name']
      self.stream_list.insert(x,channel)
      if debug:
        print('%s is number: %d in the list' % (self.stream_list[x],number)) 


  def request_Channel(self,channelName, debug=False):
    '''
    Example response:
    -Token
     {}
    -Sid
    -Mobile restricted
    '''
    #Example url: http://api.twitch.tv/api/channels/{channel}/access_token
    request_URL = "http://api.twitch.tv/api/channels/{}/access_token?client_id={}".format(channelName,self.clientID)
    if debug:
      print(request_URL)
    response = requests.get(request_URL)
    jsonData = response.json() 
    self.token = jsonData['token']
    self.sig = jsonData['sig']
    if debug:  
      print(jsonData)
      print('token is: %s' % self.token)
      print('sig is: %s' % self.sig)
    
    self.request_m3u8_Playlist(channelName, debug=False)

  def request_m3u8_Playlist(self,channelName, debug=False):
    request_URL = 'http://usher.twitch.tv/api/channel/hls/{}.m3u8?player=twitchweb&token={}&sig={}&allow_audio_only=true&allow_source=true&type=any&p=9333029'.format(channelName,self.token,self.sig)
    response = requests.get(request_URL)
    if debug:  
      print(request_URL)
      print(response.text+'\n=================================')
      
    '''This request returns a m3u8 playlist file with stream link and res info data'''
    data = response.text
    self.playlist = m3u8_playlist(data)
    self.playlist.parse_Playlist(True)
 
'''
Setting up the logging level for the application/dubug session
debug, info, warning, error and critical
=========================
Use: 
logging.debug('some text') As a debug level output

Use:
logging.info('Some info',data) As some info level log output
+++++++++++++++++++++++++

Can toggle using:

level=logging.DEBUG etc
'''
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#Setting the constants and lists

resultsLimit = 10

lastApiCall_time = 0

#Below are the calls to the config file with the app id.

file = open('config.txt')

id = file.readline().split(':')[1]

#Create a new twitch_Session object
twitchSess = twitch_session(id,resultsLimit)
twitchSess.request_From_Twitch(True)

#Example game to grab streams from: top-most game & top-most channel : index[0]
print(twitchSess.request_TopChannels_ByGame(twitchSess.game_list[0], True))
print(twitchSess.request_Channel(twitchSess.stream_list[0],True))


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