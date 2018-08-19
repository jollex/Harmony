try:
    import spidev
except ImportError:
    spidev = False
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
        self.spi.xfer2([item for sublist in pixel_buffer for item in sublist]
                       + [0x00, 0x00, 0x00])
