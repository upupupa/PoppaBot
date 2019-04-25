import json
import os
import sys
sys.path.append(os.path)

class Cfgparser:

    def __init__(self):  
        if os.name == "nt":
            self.path = os.path.normpath(os.getcwd()) + "\\"
        else:
            self.path = os.path.normpath(os.getcwd()) + "/"
        self.config = {'DEFAULT': {}}

    def writeConfigFile(self, key, data):
        self.config['DEFAULT'][key] = data
        with open(self.path + 'config.json', 'w') as configfile:
            configfile.write(self.config)
            configfile.close()

    def readConfigFile(self):
        with open(self.path + "config.json", "r") as configfile:
            self.config = json.load(configfile)
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
        self.config = json.dumps({'DEFAULT': {'discord_token': 'insert your discord token',
                                    'osu_token': 'insert your osu token',
                                    'mongoDB': ["localhost", 27017],
                                    'default_command_prefix': '?',
                                    'default_locale': 'en'}}, indent=2)
        with open(self.path + 'config.json', 'w') as configfile:
            configfile.write(self.config)
            configfile.close()