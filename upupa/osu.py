import datetime
import json

import pyosu
from upupa.config import Cfgparser

def mainUserInfo(fn):
    def wrapped(self, **kwargs):
        full_info = fn(kwargs)
        answer = "Player: {}\nCountry: {}\nPP's: {}\nGlobal rank: {}\nCountry rank: {}".format(full_info['username'], full_info['country'], full_info['pp_raw'], full_info['pp_rank'], full_info['pp_country_rank'])
        return answer
    return wrapped

class Osu:
    def __init__(self):
        config = Cfgparser()
        config.readConfigFile()
        self.token = config.getOsuToken()
        self.osu = pyosu.Api(apikey=self.token)

    @mainUserInfo
    def get_user(self, **kwargs):
        try:
            userid = kwargs['id']
            user = pyosu.User(userid=userid)
        except KeyError:
            username = kwargs['name']
            user = pyosu.User(name=username)
        return self.osu.get_user(user=user)

if __name__ == "__main__":
    osu = Osu()
    answer = osu.get_user(name='upupa')
    print(answer)
    pass