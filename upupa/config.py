import configparser
import os
import sys
sys.path.append(os.path)

class Cfgparser:

    def __init__(self):  
        self.path = os.path.normpath(os.getcwd())
        if os.name == "nt":
            self.slash = "\\"
        else:
            self.slash = "/" 
        self.config = configparser.ConfigParser()

    def writeConfigFile(self, key, data):
        self.config['DEFAULT'][key] = data
        with open(self.path + self.slash + 'config.ini', 'w') as configfile:
            self.config.write(configfile)
            configfile.close()

    def readConfigFile(self):
        with open(self.path + self.slash + "config.ini", "r") as configfile:
            self.config.read(configfile)
            configfile.close()

    def getDefaultPrefix(self):
        return self.config['DEFAULT']['default_command_prefix']

    def getDiscordToken(self):
        return self.config['DEFAULT']['discord_token']

    def getOsuToken(self):
        return self.config['DEFAULT']['osu_token']
    
    def getMongoDBadr(self):
        return self.config['DEFAULT']['mongoDB']

    def getLocale(self):
        return self.config['DEFAULT']['default_locale']

    def setDefaults(self):
        self.config['DEFAULT'] = {'discord_token': 'insert your discord token',
                                    'osu_token': 'insert your osu token',
                                    'mongoDB': ["localhost", 27017],
                                    'default_command_prefix': '?',
                                    'default_locale': 'en'}
        with open(self.path + self.slash + 'config.ini', 'w') as configfile:
                self.config.write(configfile)
                configfile.close()