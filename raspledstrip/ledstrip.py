#!/usr/bin/env python
from .LPD8806 import LPD8806SPI


class ChannelOrder:
    """
        Not all LPD8806 strands are created equal.
        Some, like Adafruit's use GRB order and the other common order is GRB
        Library defaults to GRB but you can call strand.setChannelOrder(ChannelOrder)
        to set the order your strands use
    """
    RGB = [0, 1, 2]  # Probably not used, here for clarity
    GRB = [1, 0, 2]  # Strands from Adafruit and some others (default)
    BRG = [1, 2, 0]  # Strands from many other manufacturers
        

class LEDStrip:
    def __init__(self, led_count):
        """
        :param driver: :class:`LPD8806.LEDDriver`
        :return:
        """
        self.led_count = led_count
        self.driver = LPD8806SPI(led_count)
        self.c_order = ChannelOrder.GRB
        self.last_index = self.led_count - 1
        self.master_brightness = 1.0
        self.pixel_buffer = [bytearray(3) for _ in range(self.led_count)]

        # Color calculations from
        # http://learn.adafruit.com/light-painting-with-raspberry-pi
        self.gamma = [0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
                      for i in range(256)]

    def set_master_brightness(self, bright):
        """
        Set the master brightness for the LEDs 0.0 - 1.0
        :param bright:
        :return:
        """
        if bright > 1.0 or bright < 0.0:
            raise ValueError('Brightness must be between 0.0 and 1.0')
        self.master_brightness = bright

    def all_off(self):
        """
        Turn all LEDs off.
        :return:
        """
        self.fill_off()
        self.update()
        self.fill_off()
        self.update()

    def fill_off(self, start=0, end=0):
        """
        Turn off the entire strand (or a subset)
        :param start:
        :param end:
        :return:
        """
        self.fill_rgb(0, 0, 0, start, end)
        
    def fill_rgb(self, r, g, b, start=0, end=0):
        """
        Fill the strand (or a subset) with a single color using RGB values
        :param r:
        :param g:
        :param b:
        :param start:
        :param end:
        :return:
        """
        if start < 0:
            start = 0
        if end == 0 or end > self.last_index:
            end = self.last_index
        for led in range(start, end + 1):  # since 0-index include end in range
            self.__set_internal(led, r, g, b)

    def __set_internal(self, pixel, r, g, b):
        """
        internal use only. sets pixel color
        :param pixel:
        :param color:
        :return:
        """
        if pixel < 0 or pixel > self.last_index:
            return  # don't go out of bounds

        for channel, color in zip(self.c_order, [r, g, b]):
            self.pixel_buffer[pixel][channel] = \
                self.gamma[int(color * self.master_brightness)]

    def update(self):
        self.driver.update(self.pixel_buffer)
