
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



class ClientAuth(requests.auth.AuthBase):
    def __call__(self,r):
      r.headers['Client-ID'] = twitchSess.clientID
      return r


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
    logging.debug(self.video)
    return '[video:%s, bandwidth:%s, resolution:%s, codecs:%s, url:%s]' % (self.video,self.bandwidth, self.resolution, self.codecs, self.url)  


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
  def __str__(self):
    returned_string = ""
    for stream in self.streams :      
      returned_string += str(stream)+"\n"
    return returned_string
    
    
  def parse_Playlist(self, debug=False):
    #do things
    logging.info('starting playlist extraction!')
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
                logging.debug('BANDWIDTH value: %s' % (dataObject[0].split('=')[1]))
              elif 'RESOLUTION' in dataSubstring[dataIndex]:                
                resolution = (dataObject[0].split('=')[1])
                logging.debug('RESOLUTION value: %s' % (dataObject[0].split('=')[1]))
              elif 'CODECS' in dataSubstring[dataIndex] :            
                codecs = (dataObject[0].split('=')[1])
                logging.debug('CODECS value: %s' % (dataObject[0].split('=')[1]))
              elif 'VIDEO' in dataSubstring[dataIndex]:             
                video = (dataObject[0].split('=')[1])
                logging.debug('VIDEO value: %s' % (dataObject[0].split('=')[1]))
                break
             
              elif( 'http://' in str(lines[lineIndex+self.urlOffset])):
                logging.debug('Grabbing url part: %s' % lines[lineIndex+self.urlOffset])
                url = lines[lineIndex+self.urlOffset]
                       
            logging.debug("<< Video: ",video,' Bandwidth: ',bandwidth,' Resolution: ',resolution,' Codecs: ',codecs,' Url: ',url,' >>')
            new_Stream = streamObject(video,bandwidth,resolution,codecs,url)
            self.streams[videoNamesIndex] = new_Stream

            logging.info('Video stream <%s> has been grabbed!' % (self.videoNames[videoNamesIndex]))
            #video,bandwidth,resolution,codecs,url
            '''new_stream.video = video
              new_stream.bandwidth = bandwidth
              new_stream.resolution = resolution
              new_stream.codecs = codecs
              new_stream.url = url
            '''
          
          if videoNamesIndex < len(self.videoNames)-1:
            videoNamesIndex = videoNamesIndex+1
          logging.debug('videoNamesIndex index is now %d' % videoNamesIndex)    
    logging.debug(self.streams[1])

class user_Meta(object):
  def __init__(self, user_Metadata ):
    #Takes jason user meta data object and extracts values
    self.user_id =  user_Metadata["id"]
    self.login_name = user_Metadata["login"]
    self.display_name = user_Metadata["display_name"]
    self.type = user_Metadata["type"]
    self.broadcaster_type = user_Metadata["broadcaster_type"]
    self.description = user_Metadata["description"]
    self.profile_image_url = user_Metadata["profile_image_url"]
    self.offline_image_url = user_Metadata["offline_image_url"]
    self.view_count = user_Metadata["view_count"]
    self.email = user_Metadata["email"]

class live_stream_Meta(object):
  def __init__(self, live_Metadata ):
    #Takes jason live steam meta data object and extracts values
    self.stream_id =  live_Metadata["id"]
    self.user_id = live_Metadata["user_id"]
    self.game_id = live_Metadata["game_id"]
    self.type = live_Metadata["type"]
    self.title = live_Metadata["title"]
    self.viewer_count = live_Metadata["viewer_count"]
    self.started_at = live_Metadata["started_at"]
    self.lang = live_Metadata["language"]
    self.thumbnail_url = live_Metadata["thumbnail_url"]

class stream_Meta(object):
  def __init__(self, stream_Metadata ):
    #Takes jason steam meta data object and extracts values
    self.stream_id =  stream_Metadata["_id"]
    self.game = stream_Metadata["game"]
    self.viewers = stream_Metadata["viewers"]
    self.video_height = stream_Metadata["video_height"]
    self.average_fps = stream_Metadata["average_fps"]
    self.delay = stream_Metadata["delay"]
    self.created_at = stream_Metadata["created_at"]
    self.is_playlist = stream_Metadata["is_playlist"]
    self.stream_type = stream_Metadata["stream_type"]
    self.sml_preview = stream_Metadata["preview"]["small"]
    self.med_preview = stream_Metadata["preview"]["medium"]
    self.lrg_preview = stream_Metadata["preview"]["large"]
    self.tmp_preview = stream_Metadata["preview"]["template"]

    self.channel = stream_Metadata["channel"]


class twitch_session(object):
  
  def __init__(self, clientID, resultsLimit):
    self.last_call = ''
    self.time_limit = 60 #The min time between calls to reload list
    self.game_list = {}
    self.stream_list = {}
    self.clientID = clientID
    self.resultsLimit = resultsLimit
    self.token = None
    self.sig = None
    self.token_valid = False
    self.sig_valid = False
    self.m3u8_playlist = None

  def v6_request_From_Twitch(self, debug=False):

    v6_request_URL_Base = "https://api.twitch.tv/helix/"

    Top_Games = "/games/top"
    defined_URL = v6_request_URL_Base+Top_Games
    logging.debug(defined_URL)
    response = requests.get(defined_URL, auth=ClientAuth())
    jsonData = response.json()
    print(jsonData)
    print("Size is "+str(len(jsonData['data'])))
    list_count = 0
    for item in jsonData['data']:
      #Example format is:

      ""
      {
        'id': '33214',
        'name': 'Fortnite',
        'box_art_url': 'https://static-cdn.jtvnw.net/ttv-boxart/Fortnite-{width}x{height}.jpg'
      }
      ""

      number = list_count + 1
      game_Name = item['name']
      game_ID = item['id']
      self.game_list[game_Name] = game_ID
      logging.info('%s is number: %d in the list' % (game_Name, number))
      logging.info('The gamesList holds %d game names' % (len(self.game_list)))
      list_count +=1


  def request_From_Twitch(self, debug=False):
    
    
    request_URL = "https://api.twitch.tv/kraken/games/top?limit={}&client_id={}".format(self.resultsLimit, self.clientID )
    logging.debug(request_URL)
    response = requests.get(request_URL)
    jsonData = response.json()
    
    for x in range(len(jsonData['top'])):
      number = (x+1)
      game_Name = jsonData['top'][x]['game']['name']
      self.game_list.insert(x,game_Name)
      logging.info('%s is number: %d in the list' % (self.game_list[x],number))
      logging.info('The gamesList holds %d game names' % (len(self.game_list)))

  def request_TopChannels_ByGame(self,gameName,gameID,debug=False):
    '''
    Returned json structure:
    -Streams [0 - limit]
     -[0]
      -channel
       -name
    '''
    request_URL = "https://api.twitch.tv/helix/streams/?game_id={}&limit={}".format(gameID,self.resultsLimit)
    user_data_URL = 'https://api.twitch.tv/helix/users?id='
    logging.debug(request_URL)
    response = requests.get(request_URL, auth=ClientAuth())
    jsonData = response.json()
    print(request_URL)
    print(jsonData)
    for x in range(len(jsonData['data'])):
      number = x+1
      steam_data = jsonData['data'][x]
      steam_id = steam_data["id"]
      user_id = steam_data["user_id"]
      steam_type = steam_data["type"]
      stream_title = steam_data["title"]

      userData_response = requests.get(user_data_URL+user_id, auth=ClientAuth())
      userJsonResponse = userData_response.json()
#      print(userData_response)
      channel_name = userJsonResponse['data'][0]["login"]
      self.stream_list[channel_name] = live_stream_Meta(jsonData['data'][x])
      logging.debug('%s is number: %d in the list' % (channel_name,number))

    count = 0
    lastChannelID = ""
    for item in self.stream_list:
      print(item)
      name = item
      value = self.stream_list.get(name)
      viewers = value.viewer_count
      lastChannelID = self.request_Channel(value.user_id)
      print("Channel {0:20} id: {1:13} has {2:7} views".format(name, value.user_id, viewers))
      #print
      count += 1



  def request_Channel(self,channelID, debug=False):
    '''
    Example response:
    -Token
     {}
    -Sid
    -Mobile restricted
    '''
    #Example url: http://api.twitch.tv/api/channels/{channel}/access_token
    request_URL = "https://api.twitch.tv/kraken/channels/{}/".format(channelID)
    logging.debug(request_URL)
    response = requests.get(request_URL)
    jsonData = response.json()
    print(jsonData)
    """self.token = jsonData['token']
    self.sig = jsonData['sig']
    logging.debug(jsonData)
    logging.info('token is: %s' % self.token)
    logging.info('sig is: %s' % self.sig)
    
    return self.request_m3u8_Playlist(channelName, debug=False)"""

  def request_m3u8_Playlist(self,channelName, debug=False):
    request_URL = 'http://usher.twitch.tv/api/channel/hls/{}.m3u8?player=twitchweb&token={}&sig={}&allow_audio_only=true&allow_source=true&type=any&p=9333029'.format(channelName,self.token,self.sig)
    response = requests.get(request_URL)
    
    logging.debug(request_URL)
    logging.debug(response.text+'\n=================================')
      
    '''This request returns a m3u8 playlist file with stream link and res info data'''
    data = response.text
    self.playlist = m3u8_playlist(data)
    self.playlist.parse_Playlist(True)
    return self.playlist
 
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
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

#Setting the constants and lists

resultsLimit = 10 #This is the max number of returned objects

lastApiCall_time = 0

#Below are the calls to the config file with the app id.

try:

  file = open('config.txt')
except IOError:
  print("IOError on file: {}".format(file.name))


#resultsLimit = 20

id = file.readline().split(':')[1]

#Create a new twitch_Session object
twitchSess = twitch_session(id,resultsLimit)
#twitchSess.request_From_Twitch(True)

#Example game to grab streams from: top-most game & top-most channel : index[0]
twitchSess.v6_request_From_Twitch()

"""
Testing resulting List for returned data!
"""
gameListCopy = twitchSess.game_list
index = 0
for game in gameListCopy:
  print("Index: %d holds game: %s" % (index, game))
  index += 1

#print ("%r" % gameListCopy)

print("=" * 25)

for key in twitchSess.game_list.keys():
  print("Key: {0} is {1}".format(key,twitchSess.game_list.get(key)))

#Grab first key (Game ID)
first_Game_ID = next(iter(twitchSess.game_list.values()))

twitchSess.request_TopChannels_ByGame(None,first_Game_ID, True)
#print(twitchSess.request_Channel(twitchSess.stream_list[0],True))


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