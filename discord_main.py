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
import upupa.osu as Osu
import discord
from discord.ext import commands

# timenow = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
command_prefix = "?"
bot = commands.Bot(command_prefix=command_prefix)

def timenow():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def get_lang(server_id):
    chat = Chatting("get_locale", server_id)
    return chat.getLang()

def get_locale():
    loc = Locales().getLocale()
    return loc

def check_permissions(ctx):
    chat = Chatting("get_roles", ctx.guild.id)
    roles = chat.getRoles()
    if ctx.message.author.guild_permissions.administrator:
        return True
    elif roles is None:
        return False
    for i in roles:
        for j in ctx.message.author.roles:
            if i == j.name:
                return True
    else:
        return False

@bot.event
async def on_ready():
    print("[{}][{}]PoppaBot ready!".format(timenow(), "LAUNCH"))

@bot.command()
async def add_phrase(ctx, *args):
    if check_permissions(ctx):
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
async def add_role(ctx, *role):
    if check_permissions(ctx):
        locale = get_locale()
        lang = get_lang(ctx.guild.id)
        server_id = ctx.guild.id
        chat = Chatting("add_role", server_id)
        if chat.getRoles():
            if role[0] in chat.getRoles():
                answer = locale[lang]["add_role"]["roleisalready"].format(role[0])
                await ctx.send(answer)
                return
        flag = True
        if len(role) != 1:
            answer = locale[lang]["add_role"]["failure"].format(command_prefix)
            await ctx.send(answer)
            return
        for i in ctx.guild.roles:
            if role[0] == i.name:
                chat.insertRole(role[0])
                answer = locale[lang]["add_role"]["success"].format(role[0])
                flag = False
                break
        if flag:
            answer = locale[lang]["add_role"]["roledoesntexist"].format(role[0])
        await ctx.send(answer)    

@bot.command()
async def remove_role(ctx, *role):
    # TODO
    if check_permissions(ctx):
        locale = get_locale()
        lang = get_lang(ctx.guild.id)
        server_id = ctx.guild.id
        chat = Chatting("remove_role", server_id)
        permRoles = chat.getRoles()
        if len(role) == 0 or len(role) > 1:
            answer = locale[lang]['remove_role']['failure'].format(command_prefix)
            await ctx.send(answer)
            return
        else:
            answer = locale[lang]['remove_role']['nosuchroles'].format(command_prefix)
            for i in range(0, len(permRoles)-1):
                if role[0] == permRoles[i]:
                    permRoles.pop(i)
                    chat.updateRoles(permRoles)
                    answer = locale[lang]['remove_role']['success'].format(role[0])
            await ctx.send(answer)
    pass

@bot.command()
async def list_roles(ctx):
    if check_permissions:
        server_id = ctx.guild.id
        lang = get_lang(server_id)
        locale = get_locale()
        chat = Chatting("list_roles", server_id)
        roles = chat.getRoles()
        if roles is None:
            answer = locale[lang]['list_roles']['entryIsEmpty']
            await ctx.send(answer)
        else:
            answer = locale[lang]['list_roles']['entryisntempty']
            for i in range(0, len(roles)-1):
                answer += "```{}.{}\n```".format(i+1, roles[i])
            await ctx.send(answer)

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
    if check_permissions(ctx):
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
        print("[{}][{}:{}]This is command".format(timenow(), message.channel, message.author))
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
    if check_permissions(ctx):
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


@bot.command()
async def osu(ctx, *args):
    if args[0] == "-p":
        message = "-p"
    elif args[0] == "-add":
        message = "-add"
    else:
        message = "no keywords"
    await ctx.send(message)
    
    
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
        print("[{}][{}]Shutting down...".format(timenow(), "via console"))
        time.sleep(1)
        quit()
    pass
