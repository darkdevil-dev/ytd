import os

class Config(object):
     
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7262630597:AAF4c4raNMqM4HEAAB2nEYoIFFr3yTrTAVo")
    API_ID = int(os.environ.get("API_ID", 21349365))
    API_HASH = os.environ.get("API_HASH", "3cc94b13c23e232d282c2293963c213e")
    #Add your channel id. For force Subscribe.
    CHANNEL = os.environ.get("CHANNEL", "-1002224977262")
    #Skip or add your proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = ''
