#!/usr/bin/env python
from .color import Color, ColorHSV


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

    def __init__(self, driver):
        """
        :param driver: :class:`LPD8806.LEDDriver`
        :return:
        """

        self.driver = driver
        self.led_count = driver.get_led_count()

        self.c_order = ChannelOrder.GRB
        self.last_index = self.led_count - 1
        self.master_brightness = 1.0
        self.pixel_buffer = [bytearray(3) for i in range(self.led_count)]

        # Color calculations from
        # http://learn.adafruit.com/light-painting-with-raspberry-pi
        self.gamma = [0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5) for i in range(256)]

    def update(self):
        self.driver.update(self.pixel_buffer)

    def set_channel_order(self, order):
        """
        Allows for easily using LED strands with different channel orders
        :param order: :class:`ChannelOrder`
        :return:
        """
        self.c_order = order
    
    def set_master_brightness(self, bright):
        """
        Set the master brightness for the LEDs 0.0 - 1.0
        :param bright:
        :return:
        """
        if bright > 1.0 or bright < 0.0:
            raise ValueError('Brightness must be between 0.0 and 1.0')
        self.master_brightness = bright
        
    def fill(self, color, start=0, end=0):
        """
        Fill the strand (or a subset) with a single color using a Color object
        :param color:
        :param start:
        :param end:
        :return:
        """
        if start < 0:
            start = 0
        if end == 0 or end > self.last_index:
            end = self.last_index
        for led in range(start, end + 1):  # since 0-index include end in range
            self.__set_internal(led, color)

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
        self.fill(Color(r, g, b), start, end)
        
    def fill_hsv(self, h, s, v, start=0, end=0):
        """
        Fill the strand (or a subset) with a single color using HSV values
        :param h:
        :param s:
        :param v:
        :param start:
        :param end:
        :return:
        """
        self.fill(ColorHSV(h, s, v).get_color_rgb(), start, end)

    def fill_hue(self, hue, start=0, end=0):
        """
        #Fill the strand (or a subset) with a single color using a Hue value.
        #Saturation and Value components of HSV are set to max.
        :param hue:
        :param start:
        :param end:
        :return:
        """

        self.fill(ColorHSV(hue).get_color_rgb(), start, end)
        
    def fill_off(self, start=0, end=0):
        """
        Turn off the entire strand (or a subset)
        :param start:
        :param end:
        :return:
        """
        self.fill_rgb(0, 0, 0, start, end)

    def __set_internal(self, pixel, color):
        """
        internal use only. sets pixel color
        :param pixel:
        :param color:
        :return:
        """
        if pixel < 0 or pixel > self.last_index:
            return  # don't go out of bounds

        self.pixel_buffer[pixel][self.c_order[0]] = self.gamma[int(color.r * self.master_brightness)]
        self.pixel_buffer[pixel][self.c_order[1]] = self.gamma[int(color.g * self.master_brightness)]
        self.pixel_buffer[pixel][self.c_order[2]] = self.gamma[int(color.b * self.master_brightness)]

    def set(self, pixel, color):
        """
        Set single pixel to Color value
        :param pixel:
        :param color:
        :return:
        """
        self.__set_internal(pixel, color)

    def set_rgb(self, pixel, r, g, b):
        """
        Set single pixel to RGB value
        :param pixel:
        :param r:
        :param g:
        :param b:
        :return:
        """
        color = Color(r, g, b)
        self.set(pixel, color)
        
    def set_hsv(self, pixel, h, s, v):
        """
        Set single pixel to HSV value
        :param pixel:
        :param h:
        :param s:
        :param v:
        :return:
        """
        self.set(pixel, ColorHSV(h, s, v).get_color_rgb())

    def set_hue(self, pixel, hue):
        """
        Set single pixel to Hue value.
        Saturation and Value components of HSV are set to max.
        :param pixel:
        :param hue:
        :return:
        """
        self.set(pixel, ColorHSV(hue).get_color_rgb())
        
    def set_off(self, pixel):
        """
        turns off the desired pixel
        :param pixel:
        :return:
        """
        self.set_rgb(pixel, 0, 0, 0)

    def all_off(self):
        """
        Turn all LEDs off.
        :return:
        """
        self.fill_off()
        self.update()
        self.fill_off()
        self.update()

