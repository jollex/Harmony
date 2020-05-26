import asyncio

import discord
from raspledstrip.ledstrip import LEDStrip

import config


class User(object):
    def __init__(self, light, loop, username, password, color):
        self.light = light
        self.client = discord.Client(loop=loop)
        loop.run_until_complete(self.client.login(username, password))
        self.color = color

    async def run(self):
        @self.client.event
        async def on_ready():
            print('Logged in as ' + self.client.user.name)

        @self.client.event
        async def on_voice_state_update(before, after):
            if self.is_voice_change(before, after):
                in_channel = after.voice.voice_channel is not None
                muted = after.voice.self_mute
                light_on = in_channel and not muted
                self.light.change_color(self.color, light_on)

        await self.client.connect()

    def is_voice_change(self, before, after):
        return after.id == self.client.user.id \
               and (before.voice.voice_channel != after.voice.voice_channel
                    or before.voice.self_mute != after.voice.self_mute)


class Light(object):
    def __init__(self):
        self.led_strip = LEDStrip(config.LED_COUNT)
        self.led_strip.set_master_brightness(0.9)
        self.led_strip.all_off()
        self.colors = {user['color']: False for user in config.USERS}

    def change_color(self, color, on):
        self.colors[color] = on
        self.update_light()

    def update_light(self):
        on_colors = [color for color, on in self.colors.items() if on]
        if len(on_colors) > 0:
            color = tuple(int(sum(x) / len(x)) for x in zip(*on_colors))
            self.led_strip.fill_rgb(*color)
        else:
            self.led_strip.fill_off()
        self.led_strip.update()


if __name__ == "__main__":
    light = Light()
    loop = asyncio.get_event_loop()
    tasks = []
    for user in config.USERS:
        tasks.append(asyncio.ensure_future(User(light, loop, **user).run()))
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
