#!/bin/bash
sleep 2 \
&& git pull \
&& /home/discordbot/.local/bin/pip3 install --no-cache-dir --upgrade -r requirements.txt \
&& exec python3 discord-bot.py