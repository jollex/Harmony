#!/usr/bin/env bash

USER_HOST=pi@192.168.0.12

rsync --exclude=.idea --exclude=.git -av . ${USER_HOST}:~/DiscordLight/