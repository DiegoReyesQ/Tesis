import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 0b00
spi.bits_per_word = 8

try:
    while True:
        #rasp = spi.readbytes([0x00])
        resp=spi.xfer([0x07])
        print "Enviando:",0x07
        print "Respuesta:",resp
        time.sleep(5)
except KeyboardInterrupt:
    spi.close()
