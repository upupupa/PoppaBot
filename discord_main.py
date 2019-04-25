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
from upupa.locales import Locales
import upupa.osu as osu
import discord
from discord.ext import commands

timenow = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

class DiscordBot:
    def __init__(self, command_prefix):
        self.command_prefix = command_prefix
        self.bot = commands.Bot(command_prefix=self.command_prefix)
    
    def setDefParams(self, *args):
        pass

    def setLocale(self, lang):
        self.locale = Locales().getLocale(lang)
        print(self.locale['setlocale']['success'])

    def setCommandPrefix(self, command_prefix):
        pass

    @commands.event
    async def on_ready(self):
        print("[{}][{}]PoppaBot ready!".format(timenow, "LAUNCH"))

    @commands.command()
    async def add_phrase(self, ctx, *args):
        if ctx.message.author.guild_permissions.administrator:
            async with ctx.typing():
                if len(args) != 2:
                    answer = self.locale['add_phrase']['failure'].format(self.command_prefix)
                    await ctx.send(answer)
                    return
                else:
                    server_id = ctx.guild.id
                    chat = Chatting("add", server_id)
                    try:
                        chat.addResponse_str(*args)
                    except Exception as e:
                        await ctx.send(e)
                        return
                    answer = self.locale['add_phrase']['success'].format(args[0])
                    await ctx.send(answer)
                    return

    @commands.command()
    async def list_phrases(self, ctx):
        server_id = ctx.guild.id
        chat = Chatting("list", server_id)
        entry = chat.getResponseEntry()
        if entry is None:
            answer = self.locale['list_phrases']['entryIsEmpty'].format(self.command_prefix)
            await ctx.send(answer)
        else:
            request_entry = []
            response = []
            ids = []
            text = ""
            for i in entry:
                request_entry.append(i[2])
                response.append(i[3])
                ids.append(i[0])
            for i in range(0, len(response)):
                text += self.locale['list_phrases']['pair'].format(i+1, request_entry[i], response[i])
            await ctx.send(text)

    @commands.event
    async def on_message(self, message):
        #Pass bot's messages
        if message.author == self.bot.user:
            pass
        #Process commands
        elif message.content[:1] == command_prefix:
            print("[{}][{}:{}]This is command".format(timenow, message.channel, message.author))
            await self.bot.process_commands(message)
        #Processing every message from users on server to find match with DB
        #and send output-phrase
        elif message.content[:1] != command_prefix:
            server_id = message.guild.id
            chat = Chatting("message", server_id)
            text = message.content
            entry = chat.getResponseEntry()
            if entry is None:
                pass
            else:
                response = []
                for i in entry:
                    regexp = r"{}".format(i[2])
                    reObj = re.search(regexp, text, re.MULTILINE)
                    if reObj:
                        response.append(i[3])
                    continue
            if not response:
                await self.bot.process_commands(message)
            else:
                await message.channel.send(random.choice(response))
    
    @commands.command()
    async def remove_phrase(self, ctx, *request):
        if ctx.message.author.server_permissions.administrator:
            server_id = ctx.guild.id
            chat = Chatting("remove", server_id)
            entry = chat.getResponseEntry()
            request_entry = []
            response = []
            ids = []
            async with ctx.typing():
                if request:
                    if entry is None:
                        answer = self.locale['remove_phrase']['entryIsEmpty'].format(self.command_prefix)
                        await ctx.send(answer)
                    else:
                        for i in entry:
                            if request[0] == i[2]:
                                request_entry.append(i[2])
                                response.append(i[3])
                                ids.append(i[0])
                            continue
                    flag = 0
                    if not response:
                        answer = self.locale['remove_phrase']['noSuchPhrase']
                        await ctx.send(answer)
                    elif len(response) == 1:
                        chat.removeResponseEntry(ids[flag])
                        answer = self.locale['remove_phrase']['success'].format(request_entry[flag], response[flag])
                        await ctx.send(answer)
                    try:
                        if len(response) > 1 and request[1] is not None:
                            flag = int(request[1])-1
                            if flag == 0 and flag < len(response):
                                chat.removeResponseEntry(ids[flag])
                                answer = self.locale['remove_phrase']['success'].format(request_entry[flag], response[flag])
                                await ctx.send(answer)
                            else:
                                answer = self.locale['remove_phrase']['failure'].format(self.command_prefix)
                                await ctx.send("Incorrect input!")
                    except IndexError:
                        if len(response) > 1:
                            text = ""
                            for i in range(0, len(response)):
                                text += self.locale['remove_phrase']['pair'].format(i+1, request_entry[i], response[i])
                            answer = self.locale['remove_phrase']['choosePair'].format(text, self.command_prefix)
                            await ctx.send(answer)
                else:
                    answer = self.locale['remove_phrase']['failure'].format(self.command_prefix)
                    await ctx.send(answer)            
        pass

    self.bot.add_command(add_phrase)
    self.bot.add_command()


# @bot.command()
# async def osu_add(ctx, *args):
#     if len(args) != 2:
#         answer = "incorrect input, use {}osu_add 'gamemode' 'osu nickname or osu id'".format(command_prefix)
#         await ctx.send(answer)
#         pass
#     gamemode:str = args[0]
#     user = args[1]
#     if gamemode != "0" or gamemode != "1" or gamemode != "2" or gamemode != "3":
#         answer = "incorrect gamemode input, possible params: STD = 0, taiko = 1, mania = 2, catch the beat = 3"
#         await ctx.send(answer)

if __name__ == "__main__":
    config = Cfgparser()
    dtoken = config.getDiscordToken()
    command_prefix = config.getDefaultPrefix()
    locale = config.getLocale()
    try:
        bot = DiscordBot(command_prefix)
        bot.setLocale(locale)
        bot.bot.run(dtoken)
    except KeyboardInterrupt:
        print("[{}][{}]Shutting down...".format(timenow, "via console"))
        time.sleep(1)
        quit()
    pass
