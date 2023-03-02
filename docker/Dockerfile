FROM alpine:3.17.2

# Install python/pip
ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 git bash && ln -sf python3 /usr/bin/python \
    && adduser -D discordbot

USER discordbot
RUN cd /home/discordbot && export PATH=/home/discordbot/.local/bin:$PATH \
    && python3 -m ensurepip \
    && git clone https://github.com/deathtouch013/MemeGenerator.git \
    && cd MemeGenerator \
    && pip3 install --no-cache-dir --upgrade pip\
    && pip3 install --no-cache-dir --upgrade -r requirements.txt \
    && git remote add upstream https://github.com/deathtouch013/MemeGenerator.git
    && cp -p docker/hot_reload.sh ./hot_reload.sh

WORKDIR /home/discordbot/MemeGenerator

COPY .env .env
COPY admin.json admin.json
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD discordhealthcheck || exit 1
ENTRYPOINT ["/bin/bash","./hot_reload.sh"]