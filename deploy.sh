#!/usr/bin/env bash

USER_HOST=pi@192.168.0.12

ssh pi@192.168.0.12 "sudo systemctl stop discord-light.service"
rsync --exclude=.idea --exclude=.git -av . ${USER_HOST}:~/DiscordLight/
ssh pi@192.168.0.12 "sudo systemctl start discord-light.service"