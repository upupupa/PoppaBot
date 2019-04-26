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
command_prefix = "?"
bot = commands.Bot(command_prefix=command_prefix)

def get_lang(server_id):
    chat = Chatting("get_locale", server_id)
    return chat.getLang()

def get_locale():
    loc = Locales().getLocale()
    return loc

@bot.event
async def on_ready():
    print("[{}][{}]PoppaBot ready!".format(timenow, "LAUNCH"))

@bot.command()
async def add_phrase(ctx, *args):
    if ctx.message.author.guild_permissions.administrator:
        locale = get_locale()
        lang = get_lang(ctx.guild.id)
        async with ctx.typing():
            if len(args) != 2:
                answer = locale[lang]['add_phrase']['failure'].format(command_prefix)
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
                answer = locale[lang]['add_phrase']['success'].format(args[0])
                await ctx.send(answer)
                return

@bot.command()
async def list_phrases(ctx):
    server_id = ctx.guild.id
    lang = get_lang(server_id)
    locale = get_locale()
    chat = Chatting("list", server_id)
    entry = chat.getResponseEntry()
    if entry is None:
        answer = locale[lang]['list_phrases']['entryIsEmpty'].format(command_prefix)
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
            text += locale[lang]['list_phrases']['pair'].format(i+1, request_entry[i], response[i])
        await ctx.send(text)

@bot.command()
async def setlocale(ctx, lang):
    localesList = Locales().getlocalesList()
    if lang in localesList:
        server_id = ctx.guild.id
        chat = Chatting("setlocale", server_id)
        chat.setLang(lang)
        locale = get_locale()
        answer = locale[lang]['setlocale']['success']
    else:
        answer = locale[lang]['setlocale']['failure']
    await ctx.send(answer)

@bot.event
async def on_message(message):
    #Pass bot's messages
    if message.author == bot.user:
        pass
    #Process commands
    elif message.content[:1] == command_prefix:
        print("[{}][{}:{}]This is command".format(timenow, message.channel, message.author))
        await bot.process_commands(message)
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
            await bot.process_commands(message)
        else:
            await message.channel.send(random.choice(response))

@bot.command()
async def remove_phrase(ctx, *request):
    if ctx.message.author.guild_permissions.administrator:
        server_id = ctx.guild.id
        lang = get_lang(server_id)
        locale = get_locale()
        chat = Chatting("remove", server_id)
        entry = chat.getResponseEntry()
        request_entry = []
        response = []
        ids = []
        async with ctx.typing():
            if request:
                if entry is None:
                    answer = locale[lang]['remove_phrase']['entryIsEmpty'].format(command_prefix)
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
                    answer = locale[lang]['remove_phrase']['noSuchPhrase']
                    await ctx.send(answer)
                elif len(response) == 1:
                    chat.removeResponseEntry(ids[flag])
                    answer = locale[lang]['remove_phrase']['success'].format(request_entry[flag], response[flag])
                    await ctx.send(answer)
                try:
                    if len(response) > 1 and request[1] is not None:
                        flag = int(request[1])-1
                        if flag == 0 and flag < len(response):
                            chat.removeResponseEntry(ids[flag])
                            answer = locale[lang]['remove_phrase']['success'].format(request_entry[flag], response[flag])
                            await ctx.send(answer)
                        else:
                            answer = locale[lang]['remove_phrase']['failure'].format(command_prefix)
                            await ctx.send(answer)
                except IndexError:
                    if len(response) > 1:
                        text = ""
                        for i in range(0, len(response)):
                            text += locale[lang]['remove_phrase']['pair'].format(i+1, request_entry[i], response[i])
                        answer = locale[lang]['remove_phrase']['choosePair'].format(text, command_prefix)
                        await ctx.send(answer)
            else:
                answer = locale[lang]['remove_phrase']['failure'].format(command_prefix)
                await ctx.send(answer)            
    pass

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
    try:
        config.readConfigFile()
    except Exception as e:
        print(e)
        config.setDefaults()
        config.readConfigFile()
    dtoken = config.getDiscordToken()
    if dtoken.startswith("insert "):
        dtoken = input("Input your Discord TOKEN:\n")
        config.writeConfigFile("discord_token", dtoken)
        osutoken = input("Input your Osu API TOKEN:\n")
        config.writeConfigFile("osu_token", osutoken)
    command_prefix = config.getDefaultPrefix()
    locale = config.getLocale()
    try:
        bot.run(dtoken)
    except KeyboardInterrupt:
        print("[{}][{}]Shutting down...".format(timenow, "via console"))
        time.sleep(1)
        quit()
    pass
