from bibliopixel.drivers.SPI import SPI
from bibliopixel.layout import Strip
from bibliopixel.drivers.channel_order import ChannelOrder

driver = SPI(ledtype='LPD8806', num=24, c_order=ChannelOrder.GRB)
led = Strip(driver)

print('Loaded')

while True:
    led.fill((209, 36, 44))
    print('Filled')
