#!/usr/local/bin python3.5
# -*- coding: utf-8 -*-

import asyncio
import datetime
import json
import random
import re
import sys
import time
import upupa.const as const
from upupa.chatting import Chatting
from upupa.config import Cfgparser
from upupa.databasesqlite3 import Database
import upupa.osu as osu
import discord
from discord.ext import commands

class DiscordBot:
    def __init__(self):
        print("Getting configuration from config.ini...")
        config = Cfgparser()
        try:    
            config.readConfigFile()
            self.dToken = config.getDiscordToken()
            self.osuToken = config.getOsuToken()
            self.bot = commands.Bot(self.command_prefix)
            print(self.command_prefix + "\n" + self.dToken)
        except Exception as e:
            print(e)
            print("Bad thing happend to config.ini file.. We will send robots to fix it")
            config.setDefaults()
            print("Beep-beep, boop-boop..")
            print("We've rebuilded config.ini")
            self.command_prefix = config.getDefaultPrefix()
            self.dToken = config.getDiscordToken()
            self.osuToken = config.getOsuToken()
            self.bot = commands.Bot(self.command_prefix)
        finally:
            if self.dToken.startswith("insert your") or self.dToken.startswith(""):
                self.dToken = input("Please, input your bot's API token:\n")
                config.readConfigFile()
                config.writeConfigFile("discord_token", self.dToken)
                print("Discord Token updated")
            if self.osuToken.startswith("insert your") or self.osuToken.startswith(""):
                self.osuToken = input("Please, input your osu API token:\n")
                config.readConfigFile()
                config.writeConfigFile("osu_token", self.osuToken)
                
    def 

if __name__ == "__main__":
    try:
        discBot = DiscordBot()
    except KeyboardInterrupt:
        print("[{}][{}]")

    pass