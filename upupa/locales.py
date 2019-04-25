import json
import re
import os
import sys
sys.path.append(os.path)

class Locales:
    def __init__(self):
        if os.name == "nt":
            self.path = os.path.normpath(os.getcwd() + "\\locales\\") + "\\"
        else:
            self.path = os.path.normpath(os.getcwd() + "/locales/") + "/"
        with open(self.path + "locales.json", encoding="utf-8", mode="r") as localesfile:
            self.locales = json.load(localesfile)
        self.localeslist = self.locales.keys()

    def getlocalesList(self):
        return self.localeslist

    def getLocale(self):
        return self.locales

if __name__ == "__main__":
    loc = Locales()
    pass