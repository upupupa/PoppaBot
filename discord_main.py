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

command_prefix = "?"
timenow = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
bot = commands.Bot(command_prefix=command_prefix)

def set_def_params(*args):
    global command_prefix
    command_prefix = args[0]

@bot.event
async def on_ready():
    print("[{}][{}]PoppaBot ready!".format(timenow, "LAUNCH"))

@bot.command()
async def add_phrase(ctx, *args):
    if ctx.message.author.guild_permissions.administrator:
        async with ctx.typing():
            if len(args) != 2:
                answer = "Incorrect input, use {}add_phrase 'request_str' 'response_str'".format(command_prefix)
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
                await ctx.send("Added new response for {}".format(args[0]))
                return

@bot.command()
async def list_phrases(ctx):
    server_id = ctx.guild.id
    chat = Chatting("list", server_id)
    entry = chat.getResponseEntry()
    if entry is None:
        await ctx.send("First add something with {}add_phrase command!".format(command_prefix))
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
            text += "{}. Pair {} - {}\n".format(i+1, request_entry[i], response[i])
        await ctx.send(text)

@bot.command()
async def shutdown(ctx):
    if ctx.message.author.server_permissions.administrator:
        print("[{}][{}:{}]Shutting down...".format(timenow, ctx.channel, ctx.author))
        async with ctx.typing():
            await ctx.send("Shutting down...")
        quit()

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
                    await ctx.send("You still dont have anything to remove!?\nFirst add something with {}add_phrase command!".format(command_prefix))
                else:
                    for i in entry:
                        if request[0] == i[2]:
                            request_entry.append(i[2])
                            response.append(i[3])
                            ids.append(i[0])
                        continue
                flag = 0
                if not response:
                    await ctx.send("No such phrase.")
                elif len(response) == 1:
                    chat.removeResponseEntry(ids[flag])
                    await ctx.send("Successfully removed pair {} - {}".format(request_entry[flag], response[flag]))
                try:
                    if len(response) > 1 and request[1] is not None:
                        flag = int(request[1])-1
                        if flag == 0 and flag < len(response):
                            chat.removeResponseEntry(ids[flag])
                            await ctx.send("Successfully removed pair {} - {}".format(request_entry[flag], response[flag]))
                        else:
                            await ctx.send("Incorrect input!")
                except IndexError:
                    if len(response) > 1:
                        text = ""
                        for i in range(0, len(response)):
                            text += "{}. Pair {} - {}\n".format(i+1, request_entry[i], response[i])
                        message = "Choose which pair to delete:\n{}Type '{}remove phrase number' to delete".format(text, command_prefix)
                        await ctx.send(message)
            else:
                message = "Incorrect use. {}remove_phrase 'phrase-to-remove' <number(optional)>".format(command_prefix)
                await ctx.send(message)            
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
    dtoken = config.getDiscordToken()
    command_prefix = config.getDefaultPrefix()
    try:
        set_def_params(command_prefix)
        bot.run(dtoken)
    except KeyboardInterrupt:
        print("[{}][{}]Shutting down...".format(timenow, "via console"))
        time.sleep(1)
        quit()
    pass
