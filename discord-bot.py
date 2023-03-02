#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import os
import dotenv
from MemeGenerator.MemeGenerator import MemeGenerator
import io
import json
import signal
import utils
from pathlib import Path

DESCRIPTION = "Hello! I am a bot."
INTENTS = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    voice_states=True,
    messages=True,
    reactions=True,
    message_content=True,
)

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
BOT = discord.Client(
    command_prefix=None,
    description=DESCRIPTION,
    pm_help=None,
    help_attrs=dict(hidden=True),
    chunk_guilds_at_startup=False,
    heartbeat_timeout=150.0,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True),
    intents=INTENTS,
    enable_debug_events=True,
)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@BOT.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    print("READY!")

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in BOT.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        guild_count = guild_count + 1

    # TODO create logger class   https://github.com/xveiga/beekeeler/blob/main/utils/logging.py
    # tambien es util            https://github.com/xveiga/DawCord

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("This bot is in " + str(guild_count) + " guilds.")

# event listener for a comand.
@BOT.event
async def on_message(message):
    if message.author.bot:
        return
    mensaje = message.content.split()
    if mensaje[0] == "!meme":
        if mensaje[1] == "-h" or mensaje[1] == "--help":
            await message.channel.send(meme.helpDiscord())
            return
        if mensaje[1] == "-r" or mensaje[1] == "--reload":
            if message.author.id in admins:
                meme.reload()
            return
        if mensaje[1] == "--restart":
            if message.author.id in admins:
                if Path('./hot_reload.sh').is_file():
                    argv = ["/bin/bash", "./hot_reload.sh"]
                    os.execv(argv[0],argv)
                else:
                    print("hot_reload.sh not found. Maybe you forgot to create or copy it from hot_reload.sh.def?")
            return
        if mensaje[1] == "info" and len(mensaje) >= 3:
            await message.channel.send(meme.info(mensaje[2]))
            return
        strings = []
        aux = ""
        for i in mensaje[2:]:
            if i == ";":
                strings.append(aux[:-1])
                aux = ""
                continue
            aux = aux + i + " "
        strings.append(aux[:-1])
        try:
            img = meme.makeMeme(mensaje[1],strings)
        except Exception as e:
            await message.channel.send(e)
            return
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
    

if __name__ == "__main__":
    # Register the signal handlers
    signal.signal(signal.SIGINT, utils.sigint_handler)

    # LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
    dotenv.load_dotenv()

    # GRAB THE API TOKEN FROM THE .ENV FILE.
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    meme = MemeGenerator()

    admins = json.load(open('admin.json'))

    # EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
    BOT.run(DISCORD_TOKEN)