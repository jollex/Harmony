# DiscordLight

DiscordLight is a script that turns on an LED strip when you are in a voice
channel and not muted. It does this by logging in to your discord account to
monitor for voice changes using the discord.py library. 

## Setup

You'll need a Raspberry Pi and an LPD8806 LED strip. Install the raspbian-lite
image onto the Raspberry Pi and enable SPI.

Use this guide to connect the LED strip to the GPIO pins:
https://learn.adafruit.com/raspberry-pi-spectrum-analyzer-display-on-rgb-led-strip/led-strip-and-rgb-led-software

Install python3 and pip3 and use pip to install the requirements:
`sudo pip3 install -r requirements.txt`

Next create a file named `config.py` and in it have the following values:
```python
DISCORD_USER = "your_discord_user"
DISCORD_PASSWORD = "your_discord_password"
USER_ID = "your_discord_user_id"
```

You should now be able to run the script with `python3 main.py`

I recommend creating a service to run the script.

## Credit

The driver for the LPD8806 LED strip is using code originally from
https://github.com/adammhaile/RPi-LPD8806 with modifications from
https://github.com/longjos/RPi-LPD8806 and some additional modifications by me
so it runs with python 3.