import discord
from raspledstrip.color import Color
from raspledstrip.ledstrip import LEDStrip
from raspledstrip.LPD8806 import LPD8806SPI

import secrets


client = discord.Client()

led_strip = LEDStrip(LPD8806SPI(32))
led_strip.set_master_brightness(0.9)
led_strip.all_off()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('-----')


@client.event
async def on_voice_state_update(before, after):
    print('Voice state update')
    if is_voice_change(before, after):
        in_channel = after.voice.voice_channel is not None
        muted = after.voice.self_mute

        light_on = in_channel and not muted

        toggle_light(light_on)


def is_voice_change(before, after):
    return before.voice.voice_channel != after.voice.voice_channel\
           or before.voice.self_mute != after.voice.self_mute


def toggle_light(light_on):
    if light_on:
        led_strip.fill(Color(209, 36, 44))
    else:
        led_strip.fill(Color(0, 0, 0))
    led_strip.update()


client.run(secrets.user, secrets.pw)
