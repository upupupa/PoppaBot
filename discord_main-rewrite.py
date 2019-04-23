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
        self.command_prefix = config.getDefaultPrefix()
        self.dToken = config.getDiscordToken()
        self.bot = commands.Bot(self.command_prefix)
        self.timenow = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

if __name__ == "__main__":
    try:
        discBot = DiscordBot()
        discBot.bot.run()
    except KeyboardInterrupt:
        print("[{}][{}]{}")

    pass