import configparser
import re
import os
import sys
sys.path.append(os.path)

class Locales:
    def __init__(self):
        self.localesDict = {}
        localeslist = []
        if os.name == "nt":
            self.path = os.path.normpath(os.getcwd() + "\\locales\\") + "\\"
        else:
            self.path = os.path.normpath(os.getcwd() + "/locales/") + "/"
        filelist = os.listdir(self.path)
        regexp = r"^[a-z]."
        for i in filelist:
            key = re.findall(regexp, i)
            localeslist.append((key[0], i))
        self.localesDict = dict(localeslist)

    def getLocale(self, lang):
        locale = configparser.ConfigParser()
        #Remember that it is possible to get exception, try/catch in main class
        locale.read(self.localesDict[lang])
        return locale

if __name__ == "__main__":
    loc = Locales()
    pass