import asyncio
import discord
import logging
import secrets

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)

@client.event
async def on_voice_state_update(before, after):
    print('Voice state update')
    if is_voice_change(before, after):
        in_channel = after.voice.voice_channel is not None
        muted = after.voice.self_mute

        light_on = in_channel and not muted

        print(light_on)

def is_voice_change(before, after):
    return before.voice.voice_channel != after.voice.voice_channel\
           or before.voice.self_mute != after.voice.self_mute

print('Running...')
client.run(secrets.user, secrets.pw)
