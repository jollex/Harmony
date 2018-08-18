try:
    import spidev
except ImportError:
    pass


class LEDDriver(object):
    def __init__(self, led_count):
        self.led_count = led_count

    def get_led_count(self):
        """
        Return the number of LEDs in this device
        :rtype: :class:`int`
        """
        return self.led_count


class LPD8806Native(LEDDriver):
    """Main driver for LPD8806 based LED strips"""
    
    def __init__(self, led_count, dev="/dev/spidev0.0"):
        super(LPD8806Native, self).__init__(led_count)
        self.dev = dev
        self.spi = open(self.dev, "wb")

    #Push new data to strand
    def update(self, pixel_buffer):
        for x in range(self.led_count):
            self.spi.write(pixel_buffer[x])
            self.spi.flush()
        #seems that the more lights we have the more you have to push zeros
        #not 100% sure why this is yet, but it seems to work
        self.spi.write(bytearray(b'\x00\x00\x00')) #zero fill the last to prevent stray colors at the end
        self.spi.flush()
        self.spi.write(bytearray(b'\x00\x00\x00'))
        self.spi.flush()
        self.spi.write(bytearray(b'\x00\x00\x00'))
        self.spi.flush()
        self.spi.write(bytearray(b'\x00\x00\x00'))
        self.spi.flush()


class LPD8806SPI(LEDDriver):
    def __init__(self, led_count):
        super(LPD8806SPI, self).__init__(led_count)
        if not spidev:
            raise Exception("SPI module not available")
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 18000000
        print('py-spidev MHz: %d' % (self.spi.max_speed_hz / 1000000.0))

    def update(self, pixel_buffer):
        self.spi.xfer2([item for sublist in pixel_buffer for item in sublist]+[0x00, 0x00, 0x00])
