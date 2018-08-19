import discord

from raspledstrip.ledstrip import LEDStrip

import config


client = discord.Client()

led_strip = LEDStrip(config.LED_COUNT)
led_strip.set_master_brightness(0.9)
led_strip.all_off()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)


@client.event
async def on_voice_state_update(before, after):
    if is_voice_change(before, after):
        in_channel = after.voice.voice_channel is not None
        muted = after.voice.self_mute
        light_on = in_channel and not muted
        toggle_light(light_on)


def is_voice_change(before, after):
    return after.id == config.USER_ID \
           and (before.voice.voice_channel != after.voice.voice_channel
                or before.voice.self_mute != after.voice.self_mute)


def toggle_light(light_on):
    if light_on:
        led_strip.fill_rgb(*config.RGB)
    else:
        led_strip.fill_off()
    led_strip.update()


client.run(config.DISCORD_USER, config.DISCORD_PASSWORD)
